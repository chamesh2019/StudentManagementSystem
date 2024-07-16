from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.utils.html import format_html

import base64
import io
import qrcode
import json
from qrcode.image.pure import PyPNGImage
from manage import log_file

from EDUInfoHandler.models import ClassInfo, LoginKey, Attendance, SubjectInfo, ExamInfo, Terms
from .models import StudentInfo, ParentInfo

class StudentAdd(View):
    '''Render student registration form on GET, validate data and insert into database'''

    def get(self, request):
        log_file("returned student registration form")
        current_classes = ClassInfo.objects.all().order_by('class_name')
        
        middle_grade_buckets = []
        o_level_buckets = []
        a_level_subjects = []
        
        middle_grade_buckets_id = []
        o_level_buckets_id = []
        
        for bucket in SubjectInfo.objects.filter(range="6-9", bucket=True):
            subjects = []
            for subject in bucket.bucket_subjects.split(","):
                subject = SubjectInfo.objects.get(pk=int(subject))
                subjects.append((subject.subject, subject.pk))
            middle_grade_buckets.append((bucket.pk, subjects))
            middle_grade_buckets_id.append(str(bucket.pk))
        
        for subject in SubjectInfo.objects.filter(range="10-11", bucket=True):
            subjects = []
            for subject in subject.bucket_subjects.split(","):
                subject = SubjectInfo.objects.get(pk=int(subject))
                subjects.append((subject.subject, subject.pk))
            o_level_buckets.append((subject.pk, subjects))
            o_level_buckets_id.append(str(subject.pk))
        
        for subject in SubjectInfo.objects.filter(range="12-13"):
            a_level_subjects.append((subject.subject, subject.pk))
        
        middle_grade_buckets_id = ",".join(middle_grade_buckets_id)
        o_level_buckets_id = ",".join(o_level_buckets_id)
        
        print(middle_grade_buckets_id)
        
        page_context={
        'current_classes': current_classes,
        "middle_grade_buckets": middle_grade_buckets,
        "o_level_buckets": o_level_buckets,
        "a_level_subjects": a_level_subjects,
        "middle_grade_buckets_id": middle_grade_buckets_id,
        "o_level_buckets_id": o_level_buckets_id
        }
        print(o_level_buckets)
        if request.is_mobile:
            return render(request, template_name="student_form_mobile.html", context=page_context)
        return render(request, template_name="student_form_pc.html", context=page_context)

    def post(self, request):
        data = request.POST
        print(data)
        log_file('Adding Student with already registered guardian registration')
        student_index_number = data['student_index_number']
        student_full_name = data['student_full_name']
        student_name_with_initials = data['student_name_with_initials']
        student_date_of_birth = data['student_date_of_birth']
        student_enrolled_date = data['enrolled_date']
        student_gender = data['student_gender']
        student_class = data['class_info']
        student_address = data['student_address']
        student_special_notes = data['student_special_notes']

        mother_name = data['mother_name']
        mother_status = data['mother_status']
        mother_nic = data['mother_nic']
        mother_dob = data['mother_dob']
        mother_contact_number = data['mother_contact_number']
        mother_job = data['mother_job']
        mother_special_notes = data['mother_special_notes']
        father_name = data['father_name']
        father_status = data['father_status']
        father_nic = data['father_nic']
        father_dob = data['father_dob']
        father_contact_number = data['father_contact_number']
        father_job = data['father_job']
        father_special_notes = data['father_special_notes']

        log_file('Got Student data')
        profile = request.FILES["profile"]
        
        with open(f"StudentInfoHandler/static/profile/{student_index_number}.jpg", "wb+") as destination:
            for chunk in profile.chunks():
                destination.write(chunk)
                
        img = qrcode.make(str(student_index_number),
                            image_factory=PyPNGImage)
        buffer = io.BytesIO()
        img.save(buffer)
        try:
            int(student_class)
        except:
            return HttpResponse('Invalid Class ID')
        try:
            StudentInfo.objects.get(index_number=student_index_number)
            return HttpResponse(f'Student Already exits in index number {student_index_number}')
        except:
            pass

        student_class = get_object_or_404(
            ClassInfo, id=int(student_class)
            )
            
        bucket = StudentInfo.set_subjects(student_class, data)
        
        student_instance = StudentInfo(
            index_number=student_index_number,
            full_name=student_full_name,
            name_with_initials=student_name_with_initials,
            date_of_birth=student_date_of_birth,
            gender=student_gender,
            enrolled_date=student_enrolled_date,
            address=student_address,
            special_notes=student_special_notes,
            class_info=student_class,
            buckets=bucket,
            RFID_key=f'data:image/png;base64, {base64.b64encode(buffer.getvalue()).decode("utf-8")}',
        )

        log_file(f'Student Instance {student_instance} Created')
        student_instance.save()

        parent_instance = ParentInfo(
            student_index_number=student_instance,
            mother_name=mother_name,
            mother_nic=mother_nic,
            mother_dob=mother_dob,
            mother_job=mother_job,
            mother_status=mother_status,
            mother_contact_number=mother_contact_number,
            mother_special_notes=mother_special_notes,
            father_name=father_name,
            father_nic=father_nic,
            father_dob=father_dob,
            father_contact_number=father_contact_number,
            father_job=father_job,
            father_status=father_status,
            father_special_notes=father_special_notes,
        )

        log_file(f'Parent Instance {parent_instance}  Created')
        student_instance.save()
        log_file(
            f'Student Instance {student_instance} Saved to database')
        parent_instance.save()
        log_file(
            f'Parent Instance {parent_instance} saved to database')

        log_file('Created student Instance')
        return redirect("StudentAdd")
        
            
class StudentView(View):
    '''Render student info on GET request'''

    def get(self, request, student_index_number):
        try:
            auth_key = request.session['auth_key']
        except:
            return redirect("HomepageView")
            
        if not LoginKey.student_check(student_index_number, auth_key):
            return redirect("HomepageView")
        
        log_file(f"getting deltails of {student_index_number}")
        student_instance = get_object_or_404(
            StudentInfo, index_number=student_index_number)
        parent_instance = get_object_or_404(
            ParentInfo, student_index_number=student_index_number)
        attendance = Attendance.objects.filter()[:5]
        
        selected_subjects = student_instance.get_subjects(SubjectInfo)
        selected_subjects = [subject.subject for subject in selected_subjects]
        
        try:
            all_term_marks = ExamInfo.objects.filter(student=student_instance)
            terms = list(set((marks.term.pk, marks.term.term) for marks in all_term_marks))
            print(terms)
            last_term_id, last_term = terms[0]
            print(last_term_id, last_term)
            last_term_marks = ExamInfo.objects.filter(student=student_instance, term=Terms.objects.get(pk=last_term_id))
        except:
            last_term_marks = []
            last_term = "No Exam Informations"
        
        page_context = {
            "student_instance": student_instance,
            "parent_instance": parent_instance,
            "image": "profile/" + str(student_index_number) + ".jpg",
            "QR": format_html(f"<img src='{student_instance.RFID_key}'></div>"),
            "attendance": attendance,
            "selected_subjects": selected_subjects,
            "last_term_marks": last_term_marks,
            "last_term" : last_term
        }
        
        print(page_context)
        try:
            if request.GET['added']:
                context['extra'] = reverse("StudentAdd")
        except:
            pass
        log_file(f"returning deltails of {student_index_number}")
        if request.is_mobile:
            return render(request, template_name="student_dashboard_mobile.html", context=page_context)
        return render(request, template_name="student_dashboard_pc.html", context=page_context)


class StudentListView(View):
    def get(self, request):
        log_file('Requested Student List')
        data = request.GET
        filter_kwargs = {}
        
        try:
            if data['class'] != 'all':
                filter_kwargs['class_info'] = ClassInfo.objects.get(id=data['class'])
        except:
            pass
        
        try:
            filter_kwargs['full_name__contains'] = data['name']
        except:
            pass
        
        try:
            filter_kwargs['index_number__contains'] = data['index_number']
        except:
            pass
        
        students_filtered = StudentInfo.objects.filter(**filter_kwargs)[:100]
        return_data = []
        for student in students_filtered:
            return_data.append({
                "index_number" : student.index_number,
                "student_name" : student.full_name,
                "class" : 'Grade ' + student.class_info.class_name
            })
        
        if data.get('data'):
            log_file(f'Returnng JSON of {return_data}')
            return JsonResponse(return_data, safe=False)
        log_file(f'Returnng rendered {return_data}')
        return render(request, template_name="all_students_admin_pc.html", context={
            'students': return_data,
            'current_classes': ClassInfo.objects.all().order_by('class_name')
            })

# i dont get it? 
# is cs the machine lea and ANI(AI) one?