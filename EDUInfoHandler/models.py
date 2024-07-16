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
    
    
class Terms(models.Model):
    term = models.CharField(max_length=100) 
    term_type = models.CharField(max_length=10) 
    finished = models.BooleanField()
    
    def __str__(self) -> str:
        return f'{self.term}'

class ExamInfo(models.Model):
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    student = models.ForeignKey('StudentInfoHandler.StudentInfo', on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE)
    marks = models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.subject} {self.term}'
    

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
    identifier = models.CharField(max_length=25)
    
    def __str__(self) -> str:
        return str(self.identifier)
        
    @staticmethod
    def student_check(index_number, auth_key):
        logged_in = [auth for auth in LoginKey.objects.filter(identifier=index_number)]
        auth_test = auth_key in [auth.key for auth in logged_in]
        if (auth_test or LoginKey.objects.get(key=auth_key).acc_type=="t"):
            return True
        else:
            return False
    
    @staticmethod    
    def teacher_check(nic, auth_key):
        logged_in = [auth for auth in LoginKey.objects.filter(identifier=nic)]
        auth_test = auth_key in [auth.key for auth in logged_in]
        if (auth_test):
            return True
        else:
            return False
            
    def get_user(self, TeacherInfo, StudentInfo):
        if self.acc_type == "t":
            return TeacherInfo.objects.get(nic=self.identifier)
        elif self.acc_type == "s":
            return StudentInfo.objects.get(index_number=self.identifier)