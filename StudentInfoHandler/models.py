from django.db import models
from GuardianInfoHandler.models import GuardianInfo
from EDUInfoHandler.models import ClassInfo


class StudentInfo(models.Model):
    index_number = models.IntegerField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=255)
    name_with_initials = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=20)
    gender = models.CharField(max_length=1)
    enrolled_date = models.CharField(max_length=20)
    address = models.TextField()
    alumni_status = models.BooleanField(default=False) # For alumni this will become True
    special_notes = models.TextField()
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    RFID_key = models.TextField()
    Guardian = models.ForeignKey(
        GuardianInfo, on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return self.full_name
    
class ParentInfo(models.Model):
    student_index_number = models.OneToOneField(StudentInfo, on_delete=models.CASCADE, primary_key=True)
    mother_name = models.CharField(max_length=255)
    mother_nic = models.CharField(max_length=255)
    mother_status = models.CharField(max_length=10) 
    mother_special_notes = models.TextField()
    father_name = models.CharField(max_length=255)
    father_nic = models.CharField(max_length=255)
    father_status = models.CharField(max_length=10)
    father_special_notes = models.TextField()
    
    def __str__(self) -> str:
        return self.mother_name + ' ' + self.father_name