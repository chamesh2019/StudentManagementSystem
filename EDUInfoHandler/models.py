from django.db import models

class ClassInfo(models.Model):
    class_name = models.CharField(max_length=10)  # 8-B, 10-A
    visibility = models.BooleanField(default=True)
    
class SubjectInfo(models.Model):
    subject = models.CharField(max_length=50)  # English
    visibility = models.BooleanField(default=True)
    
class ExamInfo(models.Model):
    exam = models.CharField(max_length=100) 
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    student = models.ForeignKey('StudentInfoHandler.StudentInfo', on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    marks = models.IntegerField()
    

class Attendance(models.Model):
    student = models.ForeignKey('StudentInfoHandler.StudentInfo', on_delete=models.CASCADE)
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

class LoginKeys(models.Model):
    key = models.CharField(max_length=255)
    date = models.CharField(max_length=20)