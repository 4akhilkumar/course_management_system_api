from django.urls import path
from . import views
from .views import (UserLoginView, UserRegisterView,
                    CourseCreate, CourseView, CourseUpdate, CourseList, CourseDelete,
                    uploadFileToS3)

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),

    path('createCourse/', CourseCreate.as_view()),
    path('viewCourse/<uuid:id>/', CourseView.as_view()),
    path('updateCourse/<uuid:id>/', CourseUpdate.as_view()),
    path('deleteCourse/<uuid:id>/', CourseDelete.as_view()),
    path('allCourses/', CourseList.as_view()),

    path('upload/', uploadFileToS3.as_view()),
]