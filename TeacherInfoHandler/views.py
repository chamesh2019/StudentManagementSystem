from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from EDUInfoHandler.models import ClassInfo, LoginKeys

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
            special_notes = data['special_notes']
            address = data['address']
            contact_number = data['contact_number']
            enrolled_date = data['enrolled_date']
            started_date = data['started_date']
            class_info = data['class_info']

            try:
                class_info = int(class_info)
            except:
                return HttpResponse('Invalid Class ID')
            try:
                TeacherInfo.objects.get(nic=nic)
                return HttpResponse(f'Teacher Already exits in index number {nic}')
            except:
                pass
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
                special_notes=special_notes,
                class_info=class_info,
            )

            log_file(f'Teacher Instance {teacher_instance} Created')
            teacher_instance.save()

            log_file(
                f'Teacher Instance {teacher_instance} Saved to database')

            log_file('Created teacher Instance')
            return redirect({reverse("TeacherView", kwargs={"nic":nic})})
        except:
            return HttpResponse("An Error ocurred when creating teacher info")

class TeacherView(View):
    def get(self, request, nic):
        logged_in = [auth for auth in LoginKeys.objects.all()]
        if not request.session['auth_key'] \
            in [auth.key for auth in logged_in if auth.identifier==int(nic)]:
            return redirect("HomepageView")
        log_file(f"getting deltails of {nic}")
        teacher_instance = get_object_or_404(TeacherInfo, nic=nic)
        context = {
            "teacher_instance": teacher_instance,
        }
        log_file(f"returning deltails of {nic}")
        return render(request, template_name="teacher_show_info_private.html", context=context)