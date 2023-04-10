from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.db.models.functions import Length

from StudentInfoHandler.models import StudentInfo, ParentInfo
from TeacherInfoHandler.models import TeacherInfo
from .models import ClassInfo, SubjectInfo, LoginKeys
from manage import log_file

import uuid
import datetime


class AddMarks(View):
    def get(self, request):
        log_file('Rendering adding marks')
        

class ClassView(View):
    def get(self, request):
        log_file('Rendering current classes')
        current_classes = ClassInfo.objects.filter(
            visibility=True).order_by('class_name')

        return render(request, template_name="class_view_and_edit.html", context={
            'current_classes': current_classes
        })

    def post(self, request):
        data = request.POST
        if data.get('new_class_name'):
            new_class_name = data.get('new_class_name')

            if len(data.get('new_class_name')) > 7:
                log_file(f'Too many characters in new class {new_class_name}')
                return HttpResponse("Class Name Too Long Max 5 letters")

            if len(new_class_name) == 1:
                new_class_name = '0' + new_class_name
            log_file(f'Creating new class {new_class_name}')

            visibility = False if data.get('visibility') else True

            class_instance = ClassInfo(
                class_name=new_class_name,
                visibility=visibility
            )

            class_instance.save()
            log_file(f'Created new class {new_class_name}')

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

            log_file("Moved student to alumni class")
            return redirect("ClassView")

        if data.get('update_class_name'):
            if len(data.get('update_class_name')) > 5:
                return HttpResponse("Class Name Too Long Max 5 letters")
            class_instance = get_object_or_404(
                ClassInfo, id=data.get('class_id'))
            class_instance.class_name = data.get('update_class_name')
            class_instance.save()
            return redirect("ClassView")

        return redirect("ClassView")


class SubjectsView(View):
    def get(self, request):
        log_file('Rendering current subjects')
        current_subjects = SubjectInfo.objects.filter(visibility=True)
        return render(request, template_name="subjects_view_and_edit.html", context={
            'current_subjects': current_subjects
        })

    def post(self, request):
        data = request.POST
        if data.get('new_subject_name'):
            new_subject_name = data.get('new_subject_name')

            if len(data.get('new_subject_name')) > 50:
                log_file(
                    f'Too many characters in new subject {new_subject_name}')
                return HttpResponse("Subject Name Too Long Max 50 letters")

            log_file(f'Creating new Subject {new_subject_name}')

            visibility = False if data.get('visibility') else True

            subject_instance = SubjectInfo(
                subject=new_subject_name,
                visibility=visibility
            )

            subject_instance.save()
            log_file(f'Created new Subject {new_subject_name}')

            return redirect("SubjectsView")

        if data.get('update_subject_name'):
            if len(data.get('update_subject_name')) > 50:
                return HttpResponse("Subject Name Too Long Max 50 letters")
            subject_instance = get_object_or_404(
                SubjectInfo, id=data.get('subject_id'))
            subject_instance.subject = data.get('update_subject_name')
            subject_instance.save()
            return redirect("SubjectsView")

        return redirect("SubjectsView")


class HomepageView(View):
    def get(self, request):
        return render(request, template_name="homepage.html")

    def post(self, request):
        data = request.POST
        try:
            username = data["username"]
            password = data["password"]
            if username[0] == 't' or username[0] == 'T':
                username = int(username[1:])
                teacher_instance = TeacherInfo.objects.get(nic=username)
                if not teacher_instance.password != password:
                    log_file(f'Login Credentials Error')
                    return render(request, template_name="homepage.html", context={
                        'text': 'Login Credentials Error'
                    })
                
                auth_key = LoginKeys(key=str(uuid.uuid4()),
                                 date=datetime.datetime.now(), acc_type="s", identifier=username)
                auth_key.save()
                request.session['auth_key'] = auth_key.key
                log_file(f'teacher login successfull {username}')
                return redirect('TeacherView', nic=username)
            
            
            username = int(username)
            parent_instance = ParentInfo.objects.get(
                student_index_number=username)
            if str(parent_instance.mother_nic) != password and str(parent_instance.father_nic) != password:
                log_file(f'Login Credentials Error')
                return render(request, template_name="homepage.html", context={
                    'text': 'Login Credentials Error'
                })
            auth_key = LoginKeys(key=str(uuid.uuid4()),
                                 date=datetime.datetime.now(), acc_type="s", identifier=username)
            auth_key.save()
            request.session['auth_key'] = auth_key.key
            log_file(f'login successfull {username}')
            return redirect('StudentView', student_index_number=username)

        except:
            log_file(f'Username/Student not found')
            return render(request, template_name="homepage.html", context={
                'text': 'Username/Student not found'
            })
