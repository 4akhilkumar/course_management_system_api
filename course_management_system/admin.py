from django.contrib import admin

from .models import *

admin.site.register(Course)
admin.site.register(Task)
admin.site.register(TaskSubmission)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(FacultyRegCourse)
admin.site.register(StudentRegCourse)