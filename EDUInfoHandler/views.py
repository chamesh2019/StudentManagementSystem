from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.db.models.functions import Length

from StudentInfoHandler.models import StudentInfo, ParentInfo
from TeacherInfoHandler.models import TeacherInfo
from .models import ClassInfo, SubjectInfo, LoginKey, Attendance
from manage import log_file

from datetime import datetime
import uuid



class AttendanceMarkerIn(View):
    def get(self, request, id):
        try:
            student_instance = StudentInfo.objects.get(index_number=id)
            if len(Attendance.objects.filter(student=student_instance, date=datetime.now().strftime('%Y-%m-%d'))):
                return HttpResponse("Student Already Marked")
            attendance_instance = Attendance(student=student_instance, intime=datetime.now().strftime('%H:%M:%S'), outtime="-")
            attendance_instance.save()
            return HttpResponse("Attendance Passed")
        except:
            return HttpResponse("Attendance Failed")

class AttendanceMarkerOut(View):
    def get(self, request, id):
        try:
            student_instance = StudentInfo.objects.get(index_number=id)
            attendance_instance = Attendance.objects.filter(student=student_instance, date=datetime.now().strftime('%Y-%m-%d')).reverse()[0]
            attendance_instance.outtime = datetime.now().strftime('%H:%M:%S')
            attendance_instance.save()
            return HttpResponse("Attendance Passed")
            
        except:
            return HttpResponse("Attendance Failed")

class ClassView(View):
    def get(self, request):
        log_file('Rendering current classes')
        current_low_classes = ClassInfo.objects.filter(
            visibility=True, class_type="6-9").order_by('class_name')
        
        current_mid_classes = ClassInfo.objects.filter(
            visibility=True, class_type="10-11").order_by('class_name')
        
        current_high_classes = ClassInfo.objects.filter(
            visibility=True, class_type="12-13").order_by('class_name')
        
        return render(request, template_name="class_view_and_edit.html", context={
            'current_low_classes': current_low_classes,
            'current_mid_classes': current_mid_classes,
            'current_high_classes': current_high_classes
        })

    def post(self, request):
        data = request.POST
        if data.get('new_class_name'):
            new_class_name = data.get('new_class_name')

            if len(data.get('new_class_name')) > 7:
                log_file(f'Too many characters in new class {new_class_name}')
                return HttpResponse("Class Name Too Long Max 5 letters")

            if len(new_class_name) == 1 or len(new_class_name) == 3:
                new_class_name = '0' + new_class_name
            log_file(f'Creating new class {new_class_name}')

            class_type = data.get('class_type')
            visibility = False if data.get('visibility') else True

            class_instance = ClassInfo(
                class_name=new_class_name,
                visibility=visibility,
                class_type=class_type
            )

            class_instance.save()
            log_file(f'Created new class {new_class_name}')

            return redirect("ClassView")


        if data.get('move'):
            class_instance = get_object_or_404(
                ClassInfo, id=data.get('move'))
            class_instance.class_type = "10-11"
            class_instance.save()
            return redirect("ClassView")
        
        if data.get('alumni'):
            class_instance = get_object_or_404(
                ClassInfo, id=data.get('alumni'))
            log_file(f"Got class info of Grade {class_instance.class_name}")
            
            try:
                student_instances = StudentInfo.objects.filter(
                    class_info=class_instance)
                log_file(
                    f"students in Grade {class_instance.class_name} found")
            except:
                log_file(
                    f"No students in Grade {class_instance.class_name} deleting class")
                class_instance.delete()
                return redirect("ClassView")

            alumn_instance = get_object_or_404(ClassInfo, class_name="ALUMNI")
            for student_instance in student_instances:
                student_instance.class_info = alumn_instance
                
            class_instance.delete()
            log_file("Moved student to alumni class")
            return redirect("ClassView")

        if data.get('update_class_name'):
            if len(data.get('update_class_name')) > 5:
                return HttpResponse("Class Name Too Long Max 5 letters")
            class_instance = get_object_or_404(
                ClassInfo, id=data.get('class_id'))
            
            update_class_name = data.get('update_class_name')
            if len(update_class_name) == 1 or len(update_class_name) == 3:
                update_class_name = '0' + update_class_name
            class_instance.class_name = update_class_name
            class_instance.save()
            return redirect("ClassView")

        return redirect("ClassView")


class SubjectsView(View):
    def get(self, request):
        log_file('Rendering current subjects')
        current_subjects = SubjectInfo.objects.filter(bucket=False).order_by('range').reverse
        return render(request, template_name="subjects_view.html", context={
            'current_subjects': current_subjects
        })

class HomepageView(View):
    def get(self, request):
        return render(request, template_name="homepage.html")

    def post(self, request):
        data = request.POST
        try:
            username = data["username"]
            password = data["password"]
            if username[0] == 't' or username[0] == 'T':
                username = username[1:]
                teacher_instance = TeacherInfo.objects.get(nic=username)
                if teacher_instance.password != password:
                    log_file(f'Login Credentials Error')
                    return render(request, template_name="homepage.html", context={
                        'text': 'Login Credentials Error'
                    })
                try:
                    LoginKey.objects.get(identifier=username).delete()
                except:
                    pass
                auth_key = LoginKey(key=str(uuid.uuid4()),
                                 date=datetime.now(), acc_type="t", identifier=username)
                auth_key.save()
                request.session['auth_key'] = auth_key.key
                log_file(f'teacher login successfull {username}')
                return redirect('TeacherView', nic=username)
            
            
            parent_instance = ParentInfo.objects.get(
                student_index_number=username)
            if str(parent_instance.mother_nic) != password and str(parent_instance.father_nic) != password:
                log_file(f'Login Credentials Error')
                return render(request, template_name="homepage.html", context={
                    'text': 'Login Credentials Error'
                })
            try:
                LoginKey.objects.get(identifier=username).delete()
            except:
                pass
            auth_key = LoginKey(key=str(uuid.uuid4()),
                                 date=datetime.now(), acc_type="s", identifier=username)
            auth_key.save()
            request.session['auth_key'] = auth_key.key
            log_file(f'login successfull {username}')
            return redirect('StudentView', student_index_number=username)

        except:
            log_file(f'Username/Student not found')
            return render(request, template_name="homepage.html", context={
                'text': 'Username/Student not found'
            })
