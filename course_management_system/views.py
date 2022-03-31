from django.contrib.auth.models import User, Group
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

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
        return JsonResponse({'message': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

def course_task(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name') # hidden field
        task_name = request.POST.get('task_name')
        task_desc = request.POST.get('task_desc')

        if Course.objects.filter(name = course_name).exists() is True:
            if Task.objects.filter(name = task_name, course = course_name).exists() is False:
                Task.objects.create(
                    course = Course.objects.get(name = course_name).id,
                    name = task_name,
                    description = task_desc,
                )
            else:
                print('Same Task already exists in this course')
        else:
            print('Course does not exist')
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, 'course_task.html', context)

def task_submission(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name') # hidden field
        current_student = request.POST.get('current_student') # hidden field
        submission_file = request.FILES['submission_file']

        if Task.objects.filter(name = task_name).exists() is True:
            if TaskSubmission.objects.filter(task = task_name, student = current_student).exists() is False:
                TaskSubmission.objects.create(
                    task = Task.objects.get(name = task_name),
                    user_student = User.objects.get(username = current_student),
                    file = submission_file,
                )
            else:
                print('You already submitted this task')
        return redirect('task_submission')
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, 'task_submission.html', context)

def evaluate_submission(request):
    if request.method == 'POST':
        TaskSubmission_id = request.POST.get('TaskSubmission_id') # hidden field
        current_faculty = request.POST.get('current_faculty') # hidden field
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')

        task_submission = TaskSubmission.objects.get(id=TaskSubmission_id)
        task_submission.user_faculty = User.objects.get(username = current_faculty)
        task_submission.score = score
        task_submission.feedback = feedback
        task_submission.save()
        return redirect('task_submission')
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, 'task_submission.html', context)

def manage_students(request):
    student_from_db = User.objects.all()
    context = {
        'students': student_from_db,
    }
    return render(request, 'manage_students.html', context)

def manage_faculty(request):
    faculty_from_db = User.objects.all()
    context = {
        'faculty': faculty_from_db,
    }
    return render(request, 'manage_faculty.html', context)

def bulk_upload_faculty(request):
    if request.method == 'POST':
        faculty_from_db = User.objects.all()
        faculty_user=[]
        for i in faculty_from_db:
            faculty_user.append(i.username)
            faculty_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['faculty_file'].file)
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
                group_name = row['Designation']
                my_group = Group.objects.get(name='%s' % str(group_name))
                my_group.user_set.add(newuser)

                faculty = Faculty.objects.bulk_create([
                    Faculty(
                        user_id = newuser.id,
                        course = Course.objects.get(name = row['course_name']),
                    )
                ])
        return redirect('manage_faculty')
    else:
        return redirect('manage_faculty')

def bulk_upload_students(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['student_file'].file)
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
                group_name = row['Designation']
                my_group = Group.objects.get(name='%s' % str(group_name))
                my_group.user_set.add(newuser)

                student = Student.objects.bulk_create([
                    Student(
                        user_id = newuser.id,
                        course = Course.objects.get(name = row['course_name']),
                    )
                ])
        return redirect('manage_students')
    else:
        return redirect('manage_students')