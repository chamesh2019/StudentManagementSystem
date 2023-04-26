import base64
import io
import qrcode
from qrcode.image.pure import PyPNGImage

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from EDUInfoHandler.models import ClassInfo, LoginKey, SubjectInfo

from manage import log_file
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
            position = data['position']
            special_notes = data['special_notes']
            address = data['address']
            contact_number = data['contact_number']
            enrolled_date = data['enrolled_date']
            started_date = data['started_date']
            class_info = data['class_info']
        except:
            return HttpResponse("An Error ocurred when creating teacher info")
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
            post=post,
            position=position,
            special_notes=special_notes,
            class_info=class_info,
            qr_key=f'data:image/png;base64, {base64.b64encode(buffer.getvalue()).decode("utf-8")}'
        )

        log_file(f'Teacher Instance {teacher_instance} Created')
        teacher_instance.save()

        log_file(
            f'Teacher Instance {teacher_instance} Saved to database')

        log_file('Created teacher Instance')
        return redirect(f"/teachers/{nic}")

class TeacherView(View):
    def get(self, request, nic):
        logged_in = [auth for auth in LoginKey.objects.all()]
        if not request.session['auth_key'] \
            in [auth.key for auth in logged_in if auth.identifier==int(nic)]:
            return redirect("HomepageView")
        log_file(f"getting deltails of {nic}")
        teacher_instance = get_object_or_404(TeacherInfo, nic=nic)
        subjects = ""
        for subject in teacher_instance.subjects.split(','):
            subject = SubjectInfo.objects.get(id=int(subject))
            subjects = f"{subjects} {subject}"
        context = {
            "teacher_instance": teacher_instance,
            "subjects": subjects
        }
        log_file(f"returning deltails of {nic}")
        return render(request, template_name="teacher_show_info_private.html", context=context)


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