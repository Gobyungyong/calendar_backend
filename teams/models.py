from django.db import models


# Create your models here.
class Team(models.Model):
    teamname = models.CharField(max_length=20)
    color = models.CharField(max_length=15)

    members = models.ManyToManyField("users.User")
    nicknames = models.ForeignKey("nicknames.Nickname", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.teamname
