from unicodedata import name
from django.urls import path
from . import views
from .views import (UserLoginView, UserRegisterView, uploadFileToS3)

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('upload/', uploadFileToS3.as_view()),

    path('courses/', views.course_list, name='course_list'),
    path('courses/<uuid:id>/', views.course_detail),

    path('course_task/', views.course_task, name='course_task'),
    path('course_task_submission/', views.course_task_submission, name='course_task_submission'),
    path('evaluate_submission/', views.evaluate_submission, name='evaluate_submission'),
    path('bulk_upload_faculty/', views.bulk_upload_faculty, name='bulk_upload_faculty'),
    path('bulk_upload_students/', views.bulk_upload_students, name='bulk_upload_students'),
]