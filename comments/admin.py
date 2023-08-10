from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdin(admin.ModelAdmin):

    list_display = ("description", "author", "schedule",)
