from django.db import models


# Create your models here.
class Comment(models.Model):
    description = models.TextField()

    # author, scedule 은 연결된 값인데 연결하는 것에 대한 건 추후에
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)

    schedule = models.ForeignKey("schedules.Schedule", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.schedule
