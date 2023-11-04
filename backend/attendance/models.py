from django.db import models

# Create your models here.

#Professors model
class Professor(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    hashed_password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


#Students model
class Student(models.Model):
    student_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)

    def __str__(self):
        return self.student_name
    

#Classes model
class Class(models.Model):
    crn = models.CharField(unique=True, max_length=50)
    course_name = models.CharField(max_length=255)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name
    

#Attendance System Registration model
class AttendanceSystemRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_crn = models.ForeignKey(Class, to_field='crn', on_delete=models.SET_NULL, null=True)
    facial_encoding_file = models.BinaryField()
    qr_code_file = models.BinaryField()
    registered_for_facial = models.BooleanField(default=False)
    registered_for_qr = models.BooleanField(default=False)



#Attendance Log model
class AttendanceLog(models.Model):
    METHOD_CHOICES = [
        ('Facial Recognition', 'Facial Recognition'),
        ('QR Code', 'QR Code')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_email = models.EmailField(max_length=255)
    class_crn = models.ForeignKey(Class, to_field='crn', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    attendance_time = models.TimeField()
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)


