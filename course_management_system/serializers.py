from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    refreshToken = serializers.CharField(max_length=255, read_only=True)
    accessToken = serializers.CharField(max_length=255, read_only=True)
    is_superuser = serializers.BooleanField(required=False)

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            update_last_login(None, user)
            refreshToken = RefreshToken.for_user(user)
            return {
                'username': int(user.id),
                'refreshToken': str(refreshToken),
                'accessToken': str(refreshToken.access_token),
                'is_superuser': user.is_superuser,
            }
        else:
            raise Exception('A user with this metamask_id and password is not found.')

class CourseSerializerID(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']

class TaskSerializer(serializers.ModelSerializer):
    course = serializers.UUIDField()
    class Meta:
        model = Task
        fields = ['name', 'description', 'course']

    def create(self, attrs):
        name = attrs.get('name', None)
        description = attrs.get('description', None)
        course = attrs.get('course', None)

        try:
            course_id = Course.objects.get(id=course)
            task = Task.objects.create(name=name, description=description, course=course_id)
            return {
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'course': task.course.id,
                'course_name': task.course.name,
            }
        except Course.DoesNotExist:
            raise Exception('Course does not exist.')

class TaskSubmissionSerializer(serializers.ModelSerializer):
    task = serializers.UUIDField()
    user_student = serializers.CharField()
    user_faculty = serializers.CharField()
    file = serializers.FileField()
    class Meta:
        model = TaskSubmission
        fields = ['task', 'user_student', 'file', 'user_faculty', 'score', 'feedback']