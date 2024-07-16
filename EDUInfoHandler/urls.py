from django.urls import path
from .views import ClassView, SubjectsView, HomepageView, AttendanceMarkerIn, \
 AttendanceMarkerOut, TermView, LoginView, GalleryView, ContactView, HistoryView, \
 ResourceView, SchoolView, NewsView, QRView

urlpatterns = [
    path('class/', ClassView.as_view(), name="ClassView"),
    path('subjects/', SubjectsView.as_view(), name="SubjectsView"),
    path('', HomepageView.as_view(), name="HomepageView"),
    path('attendance/in/<str:id>', AttendanceMarkerIn.as_view(), name="AttendanceIn"),
    path('attendance/out/<str:id>', AttendanceMarkerOut.as_view(), name="AttendanceOut"),
    path('terms/', TermView.as_view(), name="TermView"),
    path('login/', LoginView.as_view(), name="LoginView"),
    path('gallery/', GalleryView.as_view(), name="GalleryView"),
    path('contact/', ContactView.as_view(), name="ContactView"),
    path('history/', HistoryView.as_view(), name="HistoryView"),
    path('resources/', ResourceView.as_view(), name="ResourceView"),
    path('school/', SchoolView.as_view(), name="SchoolView"),
    path('news/', NewsView.as_view(), name="NewsView"),
    path('qr/', QRView.as_view(), name="QRView"),
    ]
