from rest_framework import serializers
from .models import Professor, Student, Class, AttendanceSystemRegistration, AttendanceLog

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'email', 'hashed_password']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_name', 'email']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'crn', 'course_name', 'professor']

class AttendanceSystemRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSystemRegistration
        fields = ['id', 'student', 'class_crn', 'facial_encoding_file', 'qr_code_file', 'registered_for_facial', 'registered_for_qr']

class AttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLog
        fields = ['id', 'student', 'student_email', 'class_crn', 'attendance_date', 'attendance_time', 'method']