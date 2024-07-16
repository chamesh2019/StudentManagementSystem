from django.contrib import admin
from .models import ClassInfo, ExamInfo, Attendance, SubjectInfo, LoginKey
# Register your models here.

admin.site.register(ClassInfo)
admin.site.register(ExamInfo)
admin.site.register(Attendance)
admin.site.register(SubjectInfo)
admin.site.register(LoginKey)