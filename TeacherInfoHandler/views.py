from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views import View

from .models import TeacherInfo

class TeacherAdd(View):
    '''Render Teacher registration form on GET, validate data and insert into database'''

    def get(self, request):
        log_file("returned Teacher registration form")
        current_classes = ClassInfo.objects.all().order_by('class_name')
        return render(request, template_name="add_teacher_form.html", context={'current_classes': current_classes})

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
            special_notes = data['special_notes']
            address = data['address']
            contact_number = data['contact_number']
            enrolled_date = data['enrolled_date']
            started_date = data['started_date']
            class_info = data['class_info']

            try:
                int(class_info)
            except:
                return HttpResponse('Invalid Class ID')
            try:
                StudentInfo.object.get(index_number=student_index_number)
                return HttpResponse(f'Student Already exits in index number {student_index_number}')
            
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
        except:
            return HttpResponse("An Error ocurred when creating student info")

