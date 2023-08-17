from django.contrib import admin
from .models import Schedule


# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "start_date",
        "end_date",
        "state",
        "repeat",
        "user",
        "team",
    )
