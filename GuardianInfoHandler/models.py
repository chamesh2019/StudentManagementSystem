from django.db import models

class GuardianInfo(models.Model):
    full_name = models.CharField(max_length=255)
    name_with_initials = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=20)
    nic = models.CharField(max_length=15, primary_key=True)
    gender = models.CharField(max_length=1)
    job = models.CharField(max_length=50)
    relation = models.CharField(max_length=2)
    special_notes = models.TextField()
    
    def __str__(self) -> str:
        return self.full_name