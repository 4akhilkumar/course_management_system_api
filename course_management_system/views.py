from django.contrib.auth.models import User, Group
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from numpy import NaN, require

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *

import boto3
import io
import json
import pandas as pd
import time
import traceback

class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User registered successfully',
            }
        except Exception as e:
            print(str(traceback.format_exc()))
            user.delete()
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': "Something went wrong",
            }
        return Response(response, status=status_code)

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                groupList = None
                user = User.objects.get(username=request.data['username'])
                groupList = ', '.join(map(str, user.groups.all()))
            except User.DoesNotExist:
                user = None
                status_code = status.HTTP_400_BAD_REQUEST
            if user is not None:
                userData = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active,
                    'group': groupList,
                }
            else:
                userData = None
                status_code = status.HTTP_400_BAD_REQUEST
            status_code = status.HTTP_200_OK
            response = {
                'user': userData,
                'success': 'true',
                'status_code': status_code,
                'message': 'User logged in successfully',
                'tokens': {
                    'refreshToken': serializer.data['refreshToken'],
                    'accessToken': serializer.data['accessToken'],
                },
            }
        except Exception as e:
            print(str(traceback.format_exc()))
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status_code': status_code,
                'message': 'Something went wrong',
            }
        return Response(response, status=status_code)

class uploadFileToS3(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            file = request.FILES['file']
            filename = str(int(time.time() * 1000)) + '.pdf'
            s3 = boto3.resource('s3', aws_access_key_id="AKIA4WAVXNSTKLN3QID6",
                                aws_secret_access_key="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")
            bucket = s3.Bucket("190031153")
            bucket.put_object(Key=filename, Body=file)
            s3_url = "https://190031153.s3.ap-south-1.amazonaws.com/" + filename
            status_code = status.HTTP_200_OK
            response = {
                "success": "true",
                'status_code': status_code,
                's3_url': s3_url
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'failed',
                'status_code': status_code,
                'error': str(e)
            }
        return Response(response, status=status_code)

@api_view(['GET', 'POST', 'DELETE'])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        
        id = request.query_params.get('id', None)
        if id is not None:
            courses = Course.filter(id=id)
        
        courses_serializer = CourseSerializerID(courses, many=True)
        return JsonResponse(courses_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        course_data = JSONParser().parse(request)
        courses_serializer = CourseSerializer(data=course_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return JsonResponse(courses_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(courses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Course.objects.all().delete()
        print(count[0], "Courses were deleted successfully!")
        return JsonResponse({'message': '{} Courses were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, id):
    try:
        course = Course.objects.get(id=id) 
    except Course.DoesNotExist: 
        return JsonResponse({'message': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        course_serializer = CourseSerializer(course) 
        return JsonResponse(course_serializer.data) 
 
    elif request.method == 'PUT': 
        course_data = JSONParser().parse(request) 
        course_serializer = CourseSerializer(course, data=course_data) 
        if course_serializer.is_valid(): 
            course_serializer.save() 
            return JsonResponse(course_serializer.data) 
        return JsonResponse(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        course.delete() 
        print("Course deleted successfully!")
        return JsonResponse({'message': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_faculty_registered_courses(request, faculty_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=faculty_id) 
        except User.DoesNotExist: 
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        if user is not None:
            courses = FacultyRegCourse.objects.filter(user = user)
            faculty_course_serializer = FacultyRegCourseSerializer(courses, many = True)
            DRF = faculty_course_serializer.data
            json_data = json.dumps(DRF)
            parsed_json = json.loads(json_data)
            dict = []
            for course in parsed_json:
                eachCourse = course['course']
                dict.append(eachCourse)
            return JsonResponse(dict, safe=False)
        else:
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_student_registered_courses(request, student_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=student_id) 
        except User.DoesNotExist: 
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        if user is not None:
            courses = StudentRegCourse.objects.filter(user = user)
            student_course_serializer = StudentRegCourseSerializer(courses, many = True)
            DRF = student_course_serializer.data
            json_data = json.dumps(DRF)
            parsed_json = json.loads(json_data)
            dict = []
            for course in parsed_json:
                eachCourse = course['course']
                dict.append(eachCourse)
            return JsonResponse(dict, safe=False)
        else:
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def course_task(request):
    if request.method == 'POST':
        course_task_data = JSONParser().parse(request)
        course_task_serializer = TaskSerializer(data = course_task_data)
        if course_task_serializer.is_valid():
            course_task_serializer.save()
            return JsonResponse(course_task_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(course_task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def course_task_submission(request):
    if request.method == 'POST':
        task_id = request.data['task']
        submission_file = request.data['file']
        if Task.objects.filter(id = task_id).exists() is True:
            taskObj = Task.objects.get(id = task_id)
            student_id = int(request.data['user_student'])
            if User.objects.filter(id = student_id).exists() is True:
                current_student = User.objects.get(id = student_id)
                if TaskSubmission.objects.filter(task = taskObj, user_student = current_student).exists() is False:
                    taskSubmissionObj = TaskSubmission.objects.create(
                        task = taskObj,
                        user_student = current_student,
                        file = submission_file,
                    )
                    taskSubmission_serializer = TaskSubmissionSerializer(taskSubmissionObj) 
                    return JsonResponse(taskSubmission_serializer.data)
                else:
                    message = 'You already submitted this task'
            else:
                message = "User does not exist"
        else:
            message = "Task does not exist"
        return JsonResponse({'message': message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def evaluate_submission(request):
    if request.method == 'POST':
        task_submission_id = request.data['task_submission_id']
        score = request.data['score']
        feedback = request.data['feedback']
        if TaskSubmission.objects.filter(id = task_submission_id).exists() is True:
            taskSubObj = TaskSubmission.objects.get(id = task_submission_id)
            faculty_id = request.data['user_faculty']
            if User.objects.filter(id = faculty_id).exists() is True:
                current_faculty = User.objects.get(id = faculty_id)
                if TaskSubmission.objects.filter(id = task_submission_id, user_faculty = current_faculty).exists() is False:
                    taskSubmissionObj = taskSubObj
                    taskSubmissionObj.user_faculty = current_faculty
                    taskSubmissionObj.score = score
                    taskSubmissionObj.feedback = feedback
                    taskSubmissionObj.save()
                    taskSubmission_serializer = TaskSubmissionSerializer(taskSubmissionObj) 
                    return JsonResponse(taskSubmission_serializer.data)
                else:
                    message = 'You already graded this task submission'
            else:
                message = "User does not exist"
        else:
            message = "Task submission does not exist"
        return JsonResponse({'message': message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def bulk_upload_faculty(request):
    if request.method == 'POST':
        faculty_from_db = User.objects.all()
        faculty_user=[]
        for i in faculty_from_db:
            faculty_user.append(i.username)
            faculty_user.append(i.email)

        paramFile = io.TextIOWrapper(request.data['faculty_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in faculty_user and str(row['Email']) not in faculty_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password="AKIRAaccount@21",
                )
                group_name = "Faculty"
                my_group, schema = Group.objects.get_or_create(name='%s' % str(group_name))
                my_group.user_set.add(newuser)
                my_group.save()

                faculty = Faculty.objects.bulk_create([
                    Faculty(
                        user_id = newuser.id,
                        gender = row['gender'],
                    )
                ])
                message = "Faculty uploaded successfully"
                status_code = status.HTTP_200_OK
            else:
                message = "User already exists with this username or email"
                status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse({'message': message}, status=status_code)

@api_view(['POST'])
def bulk_faculty_reg_course(request):
    if request.method == 'POST':
        faculty_from_db = User.objects.all()
        faculty_user=[]
        for i in faculty_from_db:
            faculty_user.append(i.username)
            faculty_user.append(i.email)

        paramFile = io.TextIOWrapper(request.data['faculty_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        messages_dict = {}
        for index, row in data.iterrows():
            if str(row['Username']) in faculty_user or str(row['Email']) in faculty_user:
                current_user = User.objects.get(username = str(row['Username']))
                totalCourses = row['course_name'].split(',')
                for iteration in range(len(totalCourses)):
                    eachCourse = str(totalCourses[iteration]).strip()
                    if Course.objects.filter(name = eachCourse).exists() is True:
                        eachCourseObj = Course.objects.get(name = eachCourse)
                        if FacultyRegCourse.objects.filter(user = current_user, course = eachCourseObj).exists() is True:
                            message = "%s already registered for %s course" % (current_user, eachCourse)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                        elif FacultyRegCourse.objects.filter(user = current_user, course = eachCourseObj).exists() is False:
                            FacultyRegCourse.objects.create(user = current_user, course = eachCourseObj)
                            message = "%s registered for %s course" % (current_user, eachCourse)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                        elif FacultyRegCourse.objects.filter(user = current_user).exists() is False:
                            message = "%s not registered for any course" % (current_user)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                            FacultyRegCourse.objects.create(user = current_user, course = eachCourseObj)
                        status_code = status.HTTP_200_OK
                    else:
                        message = "Course doesn't exists!"
            else:
                if row['Username'] is not NaN:
                    message = "User %s doesn't exists with this username or email" % str(row['Username']).strip()
                    messages_dict["Status"] = message
                    status_code = status.HTTP_400_BAD_REQUEST
                else:
                    status_code = status.HTTP_204_NO_CONTENT
        return JsonResponse(messages_dict, status=status_code)

@api_view(['POST'])
def bulk_upload_students(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.data['student_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password="AKIRAaccount@21",
                )
                group_name = "Student"
                my_group, schema = Group.objects.get_or_create(name='%s' % str(group_name))
                my_group.user_set.add(newuser)
                my_group.save()

                student = Student.objects.bulk_create([
                    Student(
                        user_id = newuser.id,
                        gender = row['gender'],
                    )
                ])
                message = "Students uploaded successfully"
                status_code = status.HTTP_200_OK
            else:
                message = "User already exists with this username or email"
                status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse({'message': message}, status=status_code)

@api_view(['POST'])
def bulk_students_reg_course(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.data['student_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        messages_dict = {}
        for index, row in data.iterrows():
            if str(row['Username']) in student_user or str(row['Email']) in student_user:
                current_user = User.objects.get(username = str(row['Username']))
                totalCourses = row['course_name'].split(',')
                for iteration in range(len(totalCourses)):
                    eachCourse = str(totalCourses[iteration]).strip()
                    if Course.objects.filter(name = eachCourse).exists() is True:
                        eachCourseObj = Course.objects.get(name = eachCourse)
                        if StudentRegCourse.objects.filter(user = current_user, course = eachCourseObj).exists() is True:
                            message = "%s already registered for %s course" % (current_user, eachCourse)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                        elif StudentRegCourse.objects.filter(user = current_user, course = eachCourseObj).exists() is False:
                            StudentRegCourse.objects.create(user = current_user, course = eachCourseObj)
                            message = "%s registered for %s course" % (current_user, eachCourse)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                        elif StudentRegCourse.objects.filter(user = current_user).exists() is False:
                            message = "%s not registered for any course" % (current_user)
                            messages_dict[str(iteration)+":"+str(current_user)] = message
                            StudentRegCourse.objects.create(user = current_user, course = eachCourseObj)
                        status_code = status.HTTP_200_OK
                    else:
                        message = "Course doesn't exists!"
            else:
                if row['Username'] is not NaN:
                    message = "User %s doesn't exists with this username or email" % str(row['Username']).strip()
                    messages_dict["Status"] = message
                    status_code = status.HTTP_400_BAD_REQUEST
                else:
                    status_code = status.HTTP_204_NO_CONTENT
        return JsonResponse(messages_dict, status=status_code)