from django.db import models
from EDUInfoHandler.models import ClassInfo


class TeacherInfo(models.Model):
    full_name = models.CharField(max_length=255)
    name_with_initials = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nic = models.CharField(max_length=15)
    gender = models.CharField(max_length=1)
    post = models.CharField(max_length=50)
    special_notes = models.JSONField()
    address = models.TextField()
    contact_number = models.CharField(max_length=12)
    enrolled_date = models.DateField(auto_now=True)
    started_date = models.DateField(auto_now=True)
    class_info = models.ForeignKey(ClassInfo, on_delete=models.DO_NOTHING)