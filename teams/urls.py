from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewTeam.as_view()),
    path("<int:team_id>/", views.Teams.as_view()),
]
