from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.db.models.functions import Length

from StudentInfoHandler.models import StudentInfo, ParentInfo
from TeacherInfoHandler.models import TeacherInfo
from .models import ClassInfo, SubjectInfo, LoginKey, Attendance, Terms
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
                student_instance.save()
                
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

class TermView(View):
    def get(self, request):
        current_mid_terms = Terms.objects.filter(term_type="6-11")
        current_high_terms = Terms.objects.filter(term_type="12-13")
        page_context = {
            "current_mid_terms": current_mid_terms,
            "current_high_terms": current_high_terms
        }
        print(page_context)
        return render(request, template_name="terms.html", context=page_context)
    
    def post(self, request):
        data = request.POST
        try:
            term_id = data["finished"]
            term_instance = Terms.objects.get(pk=term_id)
            term_instance.finished = True
            term_instance.save()
            return redirect("TermView")
        except:
            pass
        
        try:        
            new_term_name = data["new_term_name"]
            term_type = data["term_type"]
            
            terms = Terms.objects.filter(term_type = term_type)
            for term in terms:
                if term.finished == False:
                    return HttpResponse("Last term not finished yet")
                    
            term_instance = Terms(
                term = new_term_name,
                term_type = term_type,
                finished = False
            )
            term_instance.save()
            return redirect("TermView")
        except:
            pass
        
        
        return HttpResponse("Invalid Data")

class HomepageView(View):
    def get(self, request):
        with open("EDUInfoHandler/static/news/news1.txt", "r") as fp:
            news1 = fp.read()
        with open("EDUInfoHandler/static/news/news2.txt", "r") as fp:
            news2 = fp.read()
        with open("EDUInfoHandler/static/news/news3.txt", "r") as fp:
            news3 = fp.read()
        
        with open("EDUInfoHandler/static/news/news1t.txt", "r") as fp:
            news1t = fp.read()
        with open("EDUInfoHandler/static/news/news2t.txt", "r") as fp:
            news2t = fp.read()
        with open("EDUInfoHandler/static/news/news3t.txt", "r") as fp:
            news3t = fp.read()
            
        if request.is_mobile:
            return render(request, template_name="P_HOME.html", context={
            "news1": news1,
            "news2": news2,
            "news3": news3,
            "news1t": news1t,
            "news2t": news2t,
            "news3t": news3t
        })
        return render(request, template_name="L_HOME.html", context={
            "news1": news1,
            "news2": news2,
            "news3": news3,
            "news1t": news1t,
            "news2t": news2t,
            "news3t": news3t
        })

class GalleryView(View):
    def get(self, request):
        if request.is_mobile:
            return render(request, template_name="P_Gallery.html")
        return render(request, template_name="L_Galary.html")
        
class ContactView(View):
    def get(self, request):
        if request.is_mobile:
            return render(request, template_name="P_Contact.html")
        return render(request, template_name="L_Contact.html")

class HistoryView(View):
    def get(self, request):
        return render(request, template_name="L_Histry.html")
       
class ResourceView(View):
    def get(self, request):
        if request.is_mobile:
            return render(request, template_name="P_Resources.html")
        return render(request, template_name="L_Resources.html")
        
class SchoolView(View):
    def get(self, request):
        return render(request, template_name="P_School.html")

class NewsView(View):
    def get(self, request):
        with open("EDUInfoHandler/static/news/news1.txt", "r") as fp:
            news1 = fp.read()
        with open("EDUInfoHandler/static/news/news2.txt", "r") as fp:
            news2 = fp.read()
        with open("EDUInfoHandler/static/news/news3.txt", "r") as fp:
            news3 = fp.read()
        
        with open("EDUInfoHandler/static/news/news1t.txt", "r") as fp:
            news1t = fp.read()
        with open("EDUInfoHandler/static/news/news2t.txt", "r") as fp:
            news2t = fp.read()
        with open("EDUInfoHandler/static/news/news3t.txt", "r") as fp:
            news3t = fp.read()
        return render(request, template_name="news_view.html", context={
            "news1": news1,
            "news2": news2,
            "news3": news3,
            "news1t": news1t,
            "news2t": news2t,
            "news3t": news3t
        })
    def post(self, request):
        data = request.POST
        print(data)
        try:
            news1 = data["news1description"]
            news2 = data["news2description"]
            news3 = data["news3description"]
            news1t = data["news1title"]
            news2t = data["news2title"]
            news3t = data["news3title"]
        except:
            return HttpResponse("Invalid data")
            
        try:
            news1i = request.FILES['news1image']
            with open("EDUInfoHandler/static/news/news1.jpg", "wb+") as destination:
                for chunk in news1i.chunks():
                    destination.write(chunk)
        except:
            log_file("news1 image faided to update")
            
        try:
            news2i = request.FILES['news1image']
            with open("EDUInfoHandler/static/news/news1.jpg", "wb+") as destination:
                for chunk in news2i.chunks():
                    destination.write(chunk)
        except:
            log_file("news1 image faided to update")
            
        try:
            news3i = request.FILES['news1image']
            with open("EDUInfoHandler/static/news/news1.jpg", "wb+") as destination:
                for chunk in news3i.chunks():
                    destination.write(chunk)
        except:
            log_file("news1 image faided to update")
            
        with open("EDUInfoHandler/static/news/news1.txt", "w+") as fp:
            fp.write(news1)
        with open("EDUInfoHandler/static/news/news2.txt", "w+") as fp:
            fp.write(news2)
        with open("EDUInfoHandler/static/news/news3.txt", "w+") as fp:
            fp.write(news3)
            
        with open("EDUInfoHandler/static/news/news1t.txt", "w+") as fp:
            fp.write(news1t)
        with open("EDUInfoHandler/static/news/news2t.txt", "w+") as fp:
            fp.write(news2t)
        with open("EDUInfoHandler/static/news/news3t.txt", "w+") as fp:
            fp.write(news3t)
            
        log_file("news updated")
        return redirect("HomepageView")
            
class LoginView(View):
    def get(self, request):
        if request.is_mobile:
            return render(request, template_name="P_Log_in.html")
        return render(request, template_name="L_Log_in.html")
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
                    return render(request, template_name="L_Log_in.html", context={
                        'text': 'Login Credentials Error'
                    })
                try:
                    LoginKey.objects.get(identifier=username).delete()
                    request.session['auth_key'] = ""
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
                return render(request, template_name="L_Log_in.html", context={
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
            return render(request, template_name="L_Log_in.html", context={
                'text': 'Username/Student not found'
            })

class QRView(View):
    def get(self, request):
        response =  render(request, template_name="QR.html")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response