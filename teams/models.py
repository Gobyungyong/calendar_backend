from django.db import models


# Create your models here.
class Team(models.Model):
    teamname = models.CharField(max_length=20)
    color = models.CharField(max_length=15)

    members = models.ManyToManyField("users.User", null=True)
    team_leader = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="leader",
    )

    def __str__(self) -> str:
        return self.teamname
