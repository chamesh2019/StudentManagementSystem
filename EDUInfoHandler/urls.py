from django.urls import path
from .views import ClassView, SubjectsView, HomepageView

urlpatterns = [
    path('class/', ClassView.as_view(), name="ClassView"),
    path('subjects/', SubjectsView.as_view(), name="SubjectsView"),
    path('', HomepageView.as_view(), name="HomepageView")
]
