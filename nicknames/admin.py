from django.contrib import admin
from .models import Nickname

# Register your models here.
@admin.register(Nickname)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ("nickname", "description",)
