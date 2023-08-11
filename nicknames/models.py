from django.db import models


# Create your models here.
class Nickname(models.Model):
    nickname = models.CharField(max_length=15)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
