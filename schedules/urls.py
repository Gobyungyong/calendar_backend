from django.urls import path
from . import views

urlpatterns = [
    path("", views.Schedules.as_view()),
    path("search/", views.ScheduleSearch.as_view()),
]
