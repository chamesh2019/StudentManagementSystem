from django.urls import path
from .views import ClassView, SubjectsView, HomepageView, AttendanceMarkerIn, AttendanceMarkerOut

urlpatterns = [
    path('class/', ClassView.as_view(), name="ClassView"),
    path('subjects/', SubjectsView.as_view(), name="SubjectsView"),
    path('', HomepageView.as_view(), name="HomepageView"),
    path('attendance/in/<str:id>', AttendanceMarkerIn.as_view(), name="AttendanceIn"),
    path('attendance/out/<str:id>', AttendanceMarkerOut.as_view(), name="AttendanceOut"),
    ]
