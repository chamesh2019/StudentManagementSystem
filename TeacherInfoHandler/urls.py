from django.urls import path

from .views import TeacherAdd, TeacherView, TeacherListView, MarksAdd, TeacherClass


urlpatterns = [
    path("add/", TeacherAdd.as_view(), name="TeacherAdd"),
    path("", TeacherListView.as_view(), name="TeacherListView"),
    path("addmarks/<int:grade>/<int:subject>", MarksAdd.as_view(), name="AddMarks"),
    path("<str:nic>/", TeacherView.as_view(), name="TeacherView"),
    path("<str:nic>/class/", TeacherClass.as_view(), name="TeacherClass"),
   
]
