from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/comments/", include("comments.urls")),
    path("api/v1/nicknames/", include("nicknames.urls")),
    path("api/v1/schedules/", include("schedules.urls")),
    path("api/v1/teams/", include("teams.urls")),
    path("api/v1/users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
        path(
            "docs/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema-json"),
            name="swagger-ui",
        ),
        path(
            "docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema-json"),
            name="redoc",
        ),
    ]
