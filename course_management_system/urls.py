from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('manage_course/', views.manage_course, name='manage_course'),
]