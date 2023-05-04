from django.db import models
import json
from itertools import groupby

class TeacherInfo(models.Model):
    full_name = models.CharField(max_length=255)
    name_with_initials = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nic = models.CharField(max_length=15)
    password = models.CharField(max_length=20, default="0")
    gender = models.CharField(max_length=1)
    position = models.CharField(max_length=256)
    post = models.TextField()
    qr_key = models.TextField()
    special_notes = models.TextField()
    teacher_grade = models.CharField(max_length=50)
    address = models.TextField()
    contact_number = models.CharField(max_length=12)
    enrolled_date = models.DateField(auto_now=False)
    started_date = models.DateField(auto_now=False)
    class_info = models.ForeignKey('EDUInfoHandler.ClassInfo', on_delete=models.DO_NOTHING)
    subjects = models.CharField(max_length=50) 
    
    def get_subjects(self, SubjectInfo, ClassInfo):
        bucket = json.loads(self.subjects)
        temp = {k: [j for j, _ in list(v)] for k, v in groupby(bucket.items(), lambda x: x[1])}
        subjects = {}
        for key, value in temp.items():
            subjects[SubjectInfo.objects.get(pk=key)] = [ClassInfo.objects.get(pk=index) for index in value]
        return subjects
        
    def __str__(self):
        return self.full_name
