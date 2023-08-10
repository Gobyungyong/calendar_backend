from django.contrib import admin
from .models import Team

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = ("teamname", "color",)
    # members가 ManyToMany Field라서 우선 지움
