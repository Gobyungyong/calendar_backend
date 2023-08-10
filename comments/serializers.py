from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer
from schedules.serializers import ScheduleSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
