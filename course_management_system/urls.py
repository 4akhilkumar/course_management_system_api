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

    path('get_faculty_registered_courses/<int:faculty_id>/', views.get_faculty_registered_courses),
    path('get_student_registered_courses/<int:student_id>/', views.get_student_registered_courses),

    path('getTasksbyCourse/<uuid:course_id>/', views.getTasksbyCourse),
    path('getSubmittedTasksbyCourse/<uuid:course_id>/', views.getSubmittedTasksbyCourse),
    path('getSubmissionsbyTaskID/<uuid:task_id>/<int:student_id>/', views.getSubmissionsbyTaskID),
    path('course_task/', views.course_task, name='course_task'),
    path('course_task_submission/', views.course_task_submission, name='course_task_submission'),
    path('evaluate_submission/', views.evaluate_submission, name='evaluate_submission'),

    path('bulk_upload_faculty/', views.bulk_upload_faculty, name='bulk_upload_faculty'),
    path('bulk_upload_students/', views.bulk_upload_students, name='bulk_upload_students'),
    path('bulk_faculty_reg_course/', views.bulk_faculty_reg_course, name='bulk_faculty_reg_course'),
    path('bulk_students_reg_course/', views.bulk_students_reg_course, name='bulk_students_reg_course'),

]