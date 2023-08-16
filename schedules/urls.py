from django.urls import path
from . import views

urlpatterns = [
    path("", views.Schedules.as_view()),
    path("<str:user>", views.ScheduleDetail.as_view()),
]
