from django.urls import path
from . import views
from .views import (CourseList, CourseDetail, UserLoginView, UserRegisterView)

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('manage_course/', CourseList.as_view(), name='managecourse'),
    path('<uuid:pk>/', CourseDetail.as_view(), name='eachcourse'),
]