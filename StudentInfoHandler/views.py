from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.utils.html import format_html

import base64
import io
import qrcode
from qrcode.image.pure import PyPNGImage
from manage import log_file

from EDUInfoHandler.models import ClassInfo
from .models import StudentInfo, ParentInfo


class StudentAdd(View):
    '''Render student registration form on GET, validate data and insert into database'''

    def get(self, request):
        log_file("returned student registration form")
        current_classes = ClassInfo.objects.all().order_by('class_name')
        return render(request, template_name="add_student_form.html", context={'current_classes': current_classes})

    def post(self, request):
        data = request.POST
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
        mother_special_notes = data['mother_special_notes']
        father_name = data['father_name']
        father_status = data['father_status']
        father_nic = data['father_nic']
        father_special_notes = data['father_special_notes']

        log_file('Got Student data')

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
            RFID_key=f'data:image/png;base64, {base64.b64encode(buffer.getvalue()).decode("utf-8")}',
        )

        log_file(f'Student Instance {student_instance} Created')
        student_instance.save()

        parent_instance = ParentInfo(
            student_index_number=student_instance,
            mother_name=mother_name,
            mother_nic=mother_nic,
            mother_status=mother_status,
            mother_special_notes=mother_special_notes,
            father_name=father_name,
            father_nic=father_nic,
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
        return redirect(f'{reverse("StudentView", kwargs={"student_index_number":student_index_number})}?added=1')
        
            
class StudentView(View):
    '''Render student info on GET request'''

    def get(self, request, student_index_number):
        log_file(f"getting deltails of {student_index_number}")
        student_instance = get_object_or_404(
            StudentInfo, index_number=student_index_number)
        parent_instance = get_object_or_404(
            ParentInfo, student_index_number=student_index_number)
        context = {
            "student_instance": student_instance,
            "parent_instance": parent_instance,
            "QR": format_html(f"<img src='{student_instance.RFID_key}'></div>")
        }
        try:
            if request.GET['added']:
                context['extra'] = reverse("StudentAdd")
        except:
            pass
        print(student_instance.RFID_key)
        log_file(f"returning deltails of {student_index_number}")
        return render(request, template_name="student_show_info_private.html", context=context)


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
        return render(request, template_name="all_students_admin.html", context={
            'students': return_data,
            'current_classes': ClassInfo.objects.all().order_by('class_name')
            })