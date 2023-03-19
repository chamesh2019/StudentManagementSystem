from django.urls import path
from .views import StudentView, StudentAdd

urlpatterns = [
    path("add/", StudentAdd.as_view(), name="StudentAdd"),
    path("<int:student_index_number>/", StudentView.as_view(), name="StudentView")
]
