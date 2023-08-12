from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/comments/", include("comments.urls")),
    path("api/v1/nicknames/", include("nicknames.urls")),
    # path('api/v1/schedules/', include('schedules.urls')),
    path("api/v1/teams/", include("teams.urls")),
    path("api/v1/users/", include("users.urls")),
]
