from django.db import models


# Create your models here.
class Nickname(models.Model):
    nickname = models.CharField(max_length=15)
    description = models.CharField(max_length=150, null=True)  # 소개

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user
