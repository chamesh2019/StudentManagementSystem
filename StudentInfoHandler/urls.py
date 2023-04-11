from django.urls import path
from .views import StudentView, StudentAdd, StudentListView

urlpatterns = [
    path("add/", StudentAdd.as_view(), name="StudentAdd"),
    path("", StudentListView.as_view(), name="StudentListView"),
    path("<str:student_index_number>/", StudentView.as_view(), name="StudentView")
]
