import json
from django.db import models


class StudentInfo(models.Model):
    index_number = models.CharField(primary_key=True, unique=True, max_length=8)
    full_name = models.CharField(max_length=255)
    name_with_initials = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    enrolled_date = models.CharField(max_length=20)
    address = models.TextField()
    special_notes = models.TextField()
    class_info = models.ForeignKey('EDUInfoHandler.ClassInfo', on_delete=models.CASCADE)
    buckets = models.CharField(max_length=20, default="")
    RFID_key = models.TextField()
    
    def __str__(self) -> str:
        return self.full_name
        
    def get_subjects(self, SubjectInfo):
        bucket = json.loads(self.buckets)
        if "12-13" in bucket.keys():
            selected_subjects = [SubjectInfo.objects.get(pk=int(id)) for id in bucket["12-13"].split(",")]
        else:
            selected_subjects = [SubjectInfo.objects.get(pk=list(s.values())[0]) for s in bucket["other"]]
        return selected_subjects
    
    @staticmethod
    def set_subjects(student_class, data):
        if student_class.class_type == "12-13":
            bucket = {"12-13" : f"{data['subject1']},{data['subject2']},{data['subject3']}"}
        else:
            bucket_id = data["bucket_id%22"]
            bucket = []
            for id in bucket_id.split(","):
                bucket.append({id : data[id]})
            bucket = {"other": bucket}
            
        return json.dumps(bucket)

class ParentInfo(models.Model):
    student_index_number = models.OneToOneField(StudentInfo, on_delete=models.CASCADE, primary_key=True)
    mother_name = models.CharField(max_length=255)
    mother_nic = models.CharField(max_length=255)
    mother_dob = models.CharField(max_length=255)
    mother_contact_number = models.CharField(max_length=255)
    mother_job = models.CharField(max_length=255)
    mother_status = models.CharField(max_length=10) 
    mother_special_notes = models.TextField()
    father_name = models.CharField(max_length=255)
    father_job = models.CharField(max_length=255)
    father_dob = models.CharField(max_length=255)
    father_contact_number = models.CharField(max_length=255)
    father_nic = models.CharField(max_length=255)
    father_status = models.CharField(max_length=10)
    father_special_notes = models.TextField()
    
    def __str__(self) -> str:
        return self.mother_name + ' ' + self.father_name