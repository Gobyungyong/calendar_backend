from django.db import models


# Create your models here.
class Team(models.Model):
    teamname = models.CharField(max_length=20)

    class ColorChoices(models.TextChoices):
        COLOR_1 = ("#F44336", "Red")
        COLOR_2 = ("#E91E63", "Pink")
        COLOR_3 = ("#9C27B0", "Purple")
        COLOR_4 = ("#673AB7", "Deep Purple")
        COLOR_5 = ("#3F51B5", "Indigo")
        COLOR_6 = ("#2196F3", "Blue")
        COLOR_7 = ("#03A9F4", "Light Blue")
        COLOR_8 = ("#00BCD4", "Cyan")
        COLOR_9 = ("#009688", "Teal")
        COLOR_10 = ("#4CAF50", "Green")
        COLOR_11 = ("#8BC34A", "Light Green")
        COLOR_12 = ("#CDDC39", "Lime")
        COLOR_13 = ("#FFEB3B", "Yellow")
        COLOR_14 = ("#FFC107", "Amber")
        COLOR_15 = ("#FF9800", "Orange")
        COLOR_16 = ("#FF5722", "Deep Orange")

    color = models.CharField(
        max_length=20,
        choices=ColorChoices.choices,
        default=ColorChoices.COLOR_3,
    )

    members = models.ManyToManyField(
        "users.User",
        null=True,
    )
    team_leader = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="leader",
    )

    def __str__(self) -> str:
        return self.teamname
