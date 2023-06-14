import base64
import io
import qrcode
import json
from qrcode.image.pure import PyPNGImage
import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from EDUInfoHandler.models import ClassInfo, LoginKey, SubjectInfo, Terms, ExamInfo, Attendance

from manage import log_file
from .models import TeacherInfo
from StudentInfoHandler.models import StudentInfo

class TeacherAdd(View):
    '''Render Teacher registration form on GET, validate data and insert into database'''

    def get(self, request):
        log_file("returned Teacher registration form")
        current_classes = ClassInfo.objects.all().order_by('class_name')
        middle_subjects = SubjectInfo.objects.filter(range="6-9")
        o_level_subjects = SubjectInfo.objects.filter(range="10-11")
        a_level_subjects = SubjectInfo.objects.filter(range="12-13")
        print(o_level_subjects)
        page_context={
            'current_classes': current_classes,
            "middle_subjects": middle_subjects,
            "o_level_subjects": o_level_subjects,
            "a_level_subjects": a_level_subjects
        }
        
        if request.is_mobile:
            return render(request, template_name="teacher_form_mobile.html", context=page_context)
        return render(request, template_name="teacher_form_pc.html", context=page_context)

    def post(self, request):
        data = request.POST
        print(data)
        try:
            log_file('Teacher registration')
            full_name = data['full_name']
            name_with_initials = data['name_with_initials']
            date_of_birth = data['date_of_birth']
            nic = data['nic']
            gender = data['gender']
            post = data['post']
            position = data['position']
            special_notes = data['special_notes']
            address = data['address']
            contact_number = data['contact_number']
            enrolled_date = data['enrolled_date']
            started_date = data['started_date']
            class_info = data['class_info']
            teacher_grade = data['teacher_grade']
            subjects = data["selected_subjects"]
        except:
            return HttpResponse("An Error ocurred when getting teacher info")
        try:
            class_info = int(class_info)
        except:
            return HttpResponse('Invalid Class ID')
        try:
            TeacherInfo.objects.get(nic=nic)
            return HttpResponse(f'Teacher Already exits in index number {nic}')
        except:
            pass
        img = qrcode.make(str(nic),
                            image_factory=PyPNGImage)
        buffer = io.BytesIO()
        img.save(buffer)
        
        profile = request.FILES["profile"]
        
        with open(f"TeacherInfoHandler/static/profile/{nic}.jpg", "wb+") as destination:
            for chunk in profile.chunks():
                destination.write(chunk)
        
        class_info = get_object_or_404(
            ClassInfo, id=class_info
            )
        teacher_instance = TeacherInfo(
            full_name=full_name,
            name_with_initials=name_with_initials,
            date_of_birth=date_of_birth,
            gender=gender,
            enrolled_date=enrolled_date,
            started_date=started_date,
            contact_number=contact_number,
            nic=nic,
            address=address,
            post=post[2:],
            position=position,
            special_notes=special_notes,
            class_info=class_info,
            teacher_grade=teacher_grade,
            qr_key=f'data:image/png;base64, {base64.b64encode(buffer.getvalue()).decode("utf-8")}',
            subjects=subjects
        )

        log_file(f'Teacher Instance {teacher_instance} Created')
        teacher_instance.save()

        log_file(
            f'Teacher Instance {teacher_instance} Saved to database')

        log_file('Created teacher Instance')
        return redirect(f"/teachers/add")

class TeacherView(View):
    def get(self, request, nic):
        try:
            auth_key = request.session['auth_key']
        except:
            return redirect("HomepageView")
            
        if not LoginKey.teacher_check(nic, auth_key):
            return redirect("HomepageView")
            
        log_file(f"getting deltails of {nic}")
        teacher_instance = get_object_or_404(TeacherInfo, nic=nic)
        subjects = teacher_instance.get_subjects(SubjectInfo, ClassInfo)
       
        
        print(subjects)
        
        context = {
            "teacher_instance": teacher_instance,
            "subjects": subjects.items(),
            "works": teacher_instance.post.split(",")
        }
        log_file(f"returning deltails of {nic}")
        
        if request.is_mobile:
            return render(request, template_name="teacher_dashboard_mobile.html", context=context)
        
        return render(request, template_name="teacher_dashboard_pc.html", context=context)


class TeacherListView(View):
    def get(self, request):
        log_file('Requested Teacher List')
        data = request.GET
        filter_kwargs = {}
        
        try:
            filter_kwargs['full_name__contains'] = data['name']
        except:
            pass
        
        try:
            filter_kwargs['nic__contains'] = data['nic']
        except:
            pass
        
        teachers_filtered = TeacherInfo.objects.filter(**filter_kwargs)[:100]
        return_data = []
        for teacher in teachers_filtered:
            return_data.append({
                "nic" : teacher.nic,
                "teacher_name" : teacher.full_name,
            })
        
        if data.get('data'):
            log_file(f'Returnng JSON of {return_data}')
            return JsonResponse(return_data, safe=False)
        log_file(f'Returnng rendered {return_data}')
        return render(request, template_name="all_teachers_admin_pc.html", context={
            'teachers': return_data,
            })
            
            
class MarksAdd(View):
    def get(self, request, grade, subject):
        try:
            auth_key = request.session['auth_key']
        except:
            return redirect("HomepageView")
        
        teacher_instance = LoginKey.objects.get(key=auth_key).get_user(TeacherInfo, StudentInfo)
        subjects = teacher_instance.get_subjects(SubjectInfo, ClassInfo)
        
        current_subject = SubjectInfo.objects.get(pk=subject)
        current_class = ClassInfo.objects.get(pk=grade)
        
        #if not current_subject in list(subjects.keys()):
        #    return HttpResponse("you don't teach this subject")
        
        #if not current_class in subjects[current_subject]:
        #    return HttpResponse("you don't teach this grade")
        
        students = StudentInfo.objects.filter(class_info=current_class)
        if current_class.class_type == "12-13" or current_subject.bucket==True:
            print(students[0].get_subjects(SubjectInfo))
            students = [student for student in students if current_subject in student.get_subjects(SubjectInfo)]
        
        term_type = "6-11"
        if current_class.class_type == "12-13":
            term_type = "12-13"
        
        terms = Terms.objects.filter(term_type=term_type, finished=False)
        student_list = [student.pk for student in students]
        page_context = {
            "students" : students,
            "subject" : current_subject,
            "grade" : current_class,
            "student_list": json.dumps({"students" : student_list}),
            "terms" : terms
        }
        print(page_context)
        return render(request, template_name="addmarks_pc.html", context=page_context)
        
    def post(self, request,  grade, subject):
        data = request.POST
        try:
            auth_key = request.session['auth_key']
        except:
            return redirect("HomepageView")
        
        teacher_instance = LoginKey.objects.get(key=auth_key).get_user(TeacherInfo, StudentInfo)
        subjects = teacher_instance.get_subjects(SubjectInfo, ClassInfo)
        try:
            term = data["term"]
            term = Terms.objects.get(pk=term)
        except:
            return HttpResponse("Invalid data")
            
        current_subject = SubjectInfo.objects.get(pk=subject)
        current_class = ClassInfo.objects.get(pk=grade)
        
        #if not current_subject in list(subjects.keys()):
        #    return HttpResponse("you don't teach this subject")
        
        #if not current_class in subjects[current_subject]:
        #    return HttpResponse("you don't teach this grade")
        
        
        try:
            students = data["students"]
        except:
            return HttpResponse("No student list")
 
        students = json.loads(students)['students']
        for student in students:
            student_instance = StudentInfo.objects.get(index_number=student)
            
            try:
                exam_instance = ExamInfo.objects.get(subject=current_subject, term=term, student=student_instance,)
                exam_instance.marks = data[student]
                exam_instance.save()
            except:
                exam_instance = ExamInfo(
                    subject=current_subject,
                    term=term,
                    student=student_instance,
                    marks=data[student]
                )
                exam_instance.save()
        return redirect("/teachers/"+teacher_instance.nic)
        
class TeacherClass(View):
    def get(self, request, nic):
        auth_key = request.session['auth_key']
        if not LoginKey.teacher_check(nic, auth_key):
            return HttpResponse("Not Authorized")
        
        user = TeacherInfo.objects.get(nic=nic)
        if user.class_info == ClassInfo.objects.get(pk=18):
            return HttpResponse("You don't have a class listed for you")
        
        students = StudentInfo.objects.filter(class_info=user.class_info)
        
        today = datetime.date.today()
        start_delta = datetime.timedelta(days=today.weekday(), weeks=1)
        startdate = today - start_delta
        attendance = {}
        
        day_delta = datetime.timedelta(days=1, weeks=1)
        for student in students:
            markings = []
            date = startdate
            for _ in range(1, 6):
                try:
                    Attendace.objects.get(student=student, date=date.strftime("%Y-%m-%d"))
                    markings.append("Present")
                except:
                    markings.append("Absent")
            attendance[student] = markings
        
        marks_dict = {}
        c_type = user.class_info.class_type
        if c_type == '6-9' or c_type == '10-11':
            c_type='6-11'
        last_term = list(Terms.objects.filter(term_type=c_type))[-1]
        marks_list = ExamInfo.objects.filter(term=last_term)
        marks_list = [mark for mark in marks_list if mark.student.class_info == user.class_info]
        
        for mark in marks_list:
            try:
                marks_dict[mark.subject.subject].append((mark.marks, mark.student.name_with_initials))
            except:
                marks_dict[mark.subject.subject] = [(mark.marks, mark.student.name_with_initials)]
        
        total_dict = {}
        for student in students:
            S_marks = ExamInfo.objects.filter(term=last_term, student=student)
            for mark in S_marks:
                try:
                    total_dict[student.name_with_initials] += mark.marks
                except:
                    total_dict[student.name_with_initials] = mark.marks
        
        total_dict = {k: v for k, v in sorted(total_dict.items(), key=lambda item: item[1])}
        total_name_list = [key for key in total_dict.keys()]
        total_mark_list = [value for value in total_dict.values()]
        total_name_list.reverse()
        total_mark_list.reverse()
        c_type = user.class_info.class_type
        final_total_list = []
        if c_type == "6-9":
            avg_base = 12
        elif c_type == "10-11":
            avg_base = 10
        else:
            avg_base = 3
            
        for x in range(len(total_mark_list)):
            rank = total_mark_list.index(total_mark_list[x])
            final_total_list.append((total_name_list[x], total_mark_list[x], rank+1, round(total_mark_list[x]/avg_base, 2)))
            
        page_context = {
            "attendance": attendance.items(),
            "marks" : json.dumps(marks_dict),
            "ranks" : final_total_list,
            "avg" : avg_base
        }
        
        return render(request, template_name="teacher_class.html", context=page_context)