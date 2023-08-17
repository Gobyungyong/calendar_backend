from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from . import serializers


# team에 속한 user의 team schedule과 개인 스케줄
class Schedules(APIView):
    # authentication_classes = [TokenAuthentication]
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

    def post(self, request):
        serializer = serializers.ScheduleSerializer(data=request.data)

        if serializer.is_valid():
            schedule = serializer.save()
            return Response(
                serializers.ScheduleSerializer(schedule).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ScheduleDetails(APIView):
    pass


class ScheduleSearch(APIView):
    pass
