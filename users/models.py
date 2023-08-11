from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=10)
    leader = models.ForeignKey(
        "teams.Team", on_delete=models.SET_NULL, null=True, related_name="leader"
    )
