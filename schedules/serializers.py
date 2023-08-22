from rest_framework import serializers
from .models import Schedule
from teams.models import Team
from users.serializers import UserSerializer
from teams.serializers import TeamSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True,
    )
    team = TeamSerializer(
        read_only=True,
    )

    class Meta:
        model = Schedule
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
