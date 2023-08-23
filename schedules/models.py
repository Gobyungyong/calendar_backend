from django.db import models


# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()

    class StateChoices(models.TextChoices):
        TODO = ("To do", "to_do")
        DOING = ("Doing", "doing")
        Done = ("Done", "done")

    state = models.CharField(
        max_length=20,
        choices=StateChoices.choices,
    )

    # class RepeatChoices(models.TextChoices):
    #     NONE = ("none", "반복 없음")
    #     WEEKLY = ("weekly", "매주 반복")
    #     MONTHLY = ("monthly", "매달 반복")
    #     YEARLY = ("yearly", "매년 반복")

    # repeat = models.CharField(
    #     max_length=10,
    #     choices=RepeatChoices.choices,
    # )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # user이 삭제되면 schedule도 삭제

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # team이 삭제되면 schedule도 삭제

    def __str__(self) -> str:
        return self.title
