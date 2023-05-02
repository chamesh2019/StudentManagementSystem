from django.db import models

class ClassInfo(models.Model):
    class_name = models.CharField(max_length=10)  # 8-B, 10-A
    class_type = models.CharField(max_length=10) # 6-9 10-11 12-13
    visibility = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.class_name
    
class SubjectInfo(models.Model):
    subject = models.CharField(max_length=50)  # English
    range = models.CharField(max_length=10) # 6-9 10-11 12-13 other for buckets
    bucket = models.BooleanField()
    vis = models.BooleanField(default=True)
    bucket_subjects = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.subject + " " + self.range
    
class ExamInfo(models.Model):
    exam = models.CharField(max_length=100) 
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    student = models.ForeignKey('StudentInfoHandler.StudentInfo', on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    marks = models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.exam} {self.subject} {self.month} {self.year}'
    

class Attendance(models.Model):
    student = models.ForeignKey('StudentInfoHandler.StudentInfo', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    intime = models.CharField(max_length=50)
    outtime = models.CharField(max_length=50, default=None)
    
    def __str__(self) -> str:
        return f'{self.student} {self.date}'
    

class LoginKey(models.Model):
    key = models.CharField(max_length=255)
    date = models.CharField(max_length=20)
    acc_type = models.CharField(max_length=25)
    identifier = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return str(self.identifier)