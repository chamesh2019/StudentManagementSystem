from django.urls import path

from .views import TeacherAdd, TeacherView, TeacherListView, MarksAdd


urlpatterns = [
    path("add/", TeacherAdd.as_view(), name="TeacherAdd"),
    path("<int:nic>/", TeacherView.as_view(), name="TeacherView"),
    path("", TeacherListView.as_view(), name="TeacherListView"),
    path("addmarks/<int:grade>/<int:subject>", MarksAdd.as_view(), name="AddMarks")
]
