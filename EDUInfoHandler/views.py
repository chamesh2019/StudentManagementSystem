from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.db.models.functions import Length

from StudentInfoHandler.models import StudentInfo
from .models import ClassInfo
from manage import log_file

# Create your views here.
class ClassView(View):
    def get(self, request):
        log_file('Rendering current classes')
        current_classes = ClassInfo.objects.filter(visibility=True).order_by('class_name')
        
        return render(request, template_name="class_view_and_edit.html", context={
            'current_classes' : current_classes
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
            
            class_instance = ClassInfo(
                class_name = new_class_name
            )
            
            class_instance.save()
            log_file(f'Created new class {new_class_name}')
            
            return redirect("ClassView")
        
        if data.get('alumni'):
            if data.get('alumni') == str(get_object_or_404(ClassInfo, id=data.get('alumni')).id):
                log_file("Can't Move Alumni Class")
                return HttpResponse('Not Allowed')
            
            class_instance = get_object_or_404(ClassInfo, id=data.get('alumni'))
            log_file(f"Got class info of Grade {class_instance.class_name}")
            
            try:
                student_instances = StudentInfo.objects.get(class_info=class_instance)
                log_file(f"students in Grade {class_instance.class_name} found")
            except:
                log_file(f"No students in Grade {class_instance.class_name} deleting class")
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
            class_instance = get_object_or_404(ClassInfo, id=data.get('class_id'))
            class_instance.class_name = data.get('update_class_name')
            class_instance.save()
            return redirect("ClassView")
        
        return redirect("ClassView")
    
class SubjectsView(View):
    def get(self, request):
        log_file('Rendering current classes')
        current_subjects = ClassInfo.objects.filter(visibility=True).order_by('class_name')
        
        return render(request, template_name="class_view_and_edit.html", context={
            'current_classes' : current_classes
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
                class_name = new_class_name
            )
            
            class_instance.save()
            log_file(f'Created new class {new_class_name}')
            
            return redirect("ClassView")
        
        if data.get('alumni'):
            class_instance = get_object_or_404(ClassInfo, id=data.get('alumni'))
            log_file(f"Got class info of Grade {class_instance.class_name}")
            
            try:
                student_instances = StudentInfo.objects.get(class_info=class_instance)
                log_file(f"students in Grade {class_instance.class_name} found")
            except:
                log_file(f"No students in Grade {class_instance.class_name} deleting class")
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
            class_instance = get_object_or_404(ClassInfo, id=data.get('class_id'))
            class_instance.class_name = data.get('update_class_name')
            class_instance.save()
            return redirect("ClassView")
        
        return redirect("ClassView")