from django.urls import path
from . import views

urlpatterns = [
    path("newcomment/", views.NewComment.as_view()),
    path("delete/<int:comment_id>/", views.DeleteComment.as_view()),
]
