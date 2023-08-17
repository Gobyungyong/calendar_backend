from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from . import serializers


# team에 속한 user의 team schedule과 개인 스케줄
class UserTeamSchedules(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            if hasattr(user, "team"):
                team = user.team
                user_schedules = Schedule.objects.filter(user=user)
                team_schedules = Schedule.objects.filter(team=team)
                schedules = user_schedules.union(team_schedules)
                serializer = serializers.ScheduleSerializer(
                    schedules,
                    many=True,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user_schedules = Schedule.objects.filter(user=user)
                serializer = serializers.ScheduleSerializer(
                    user_schedules,
                    many=True,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)

        except NotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
