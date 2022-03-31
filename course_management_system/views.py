from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegisterSerializer
import traceback

import io
import pandas as pd

from .models import *

from rest_framework import generics

from .serializers import (CourseSerializer)

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

def manage_course(request):
    courses = Course.objects.all()
    success_msg, error_msg = '', ''
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        course_description = request.POST.get('course_description')
        course_from_db = Course.objects.all()
        course_list=[]
        for i in course_from_db:
            course_list.append(i.name)
            course_list.append(i.code)

        if course_name not in course_list and course_code not in course_list:
            Course.objects.create(
                name = course_name,
                code = course_code,
                description = course_description,
            )
            success_msg = "%s is created successfully" % (course_name)
        else:
            error_msg = 'Course already exists'

    return Response({
        'success_msg': success_msg,
        'error_msg': error_msg,
        # 'courses': data,
    })


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

def logout_user(request):
    logout(request)
    pass

class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        print(request.data)
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
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status_code': status_code,
                'message': 'User logged in successfully',
                'tokens': {
                    'refreshToken': serializer.data['refreshToken'],
                    'accessToken': serializer.data['accessToken'],
                },
                'superuser': serializer.data['is_superuser'],
                'user_id': int(serializer.data['username']),
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

# # Create superadmin
# new_group, created = Group.objects.get_or_create(name ='Administrator')
# new_group, created = Group.objects.get_or_create(name ='Faculty')
# new_group, created = Group.objects.get_or_create(name ='Student')

# if User.objects.filter(username='4akhilkumar').exists() is True:
#     user = User.objects.get(username = '4akhilkumar')
# else:
#     user = User.objects.create_user(username='4akhilkumar')
# user.username = '4akhilkumar'
# user.first_name = 'Sai Akhil Kumar Reddy'
# user.last_name = 'N'
# user.email = '4akhilkumar@gmail.com'
# user.set_password("AKIRAaccount@21")
# user.is_active = True
# user.is_staff = True
# user.is_superuser = True
# user.save()

# group_name = 'Administrator'
# my_group = Group.objects.get(name='%s' % str(group_name))
# my_group.user_set.add(user)
# print("Success")
userList = User.objects.all()
print(userList)