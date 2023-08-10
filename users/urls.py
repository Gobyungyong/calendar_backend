from django.urls import path
from . import views

urlpatterns = [
    path("newuser/", views.NewUser.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("myinfo/<str:username>/", views.UserInfo.as_view()),
]
