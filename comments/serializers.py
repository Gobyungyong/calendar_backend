from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer
from schedules.serializers import ScheduleSerializer
from .models import Comment
from rest_framework import serializers


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ScheduleCommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_is_author(self, comment):
        return comment.author == self.context["request"].user
