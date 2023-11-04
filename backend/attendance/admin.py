from django.contrib import admin
from .models import Professor, Student, Class, AttendanceLog, AttendanceSystemRegistration

# Register your models here.
#By registering your models like this, they will appear on the admin site, allowing you to easily manage records for these models.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(AttendanceSystemRegistration)
admin.site.register(AttendanceLog)