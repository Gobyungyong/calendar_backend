from rest_framework.serializers import ModelSerializer
from .models import Nickname
from users.serializers import UserSerializer
from teams.serializers import TeamSerializer


class AddNicknameSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Nickname
        fields = "__all__"
