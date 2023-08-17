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

            if user.team_set.all().exists():
                teams = user.team_set.all()
                user_schedules = Schedule.objects.filter(user=user)
                team_schedules = Schedule.objects.filter(team__in=teams)
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
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = serializers.ScheduleSerializer(schedule)
        return Response(serializer.data)

    def put(self, request, pk):
        schedule = self.get_object(pk)

        if schedule.user == request.user or (
            hasattr(schedule.team, "team_leader")
            and schedule.team.team_leader == request.user,
        ):
            serializer = serializers.ScheduleSerializer(
                schedule,
                data=request.data,
                partial=True,
            )
        if serializer.is_valid():
            updated_schedule = serializer.save()
            return Response(
                serializers.ScheduleSerializer(updated_schedule).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        schedule = self.get_object(pk)

        print(schedule.team)
        if schedule.team:
            if (
                schedule.user == request.user
                or schedule.team.team_leader == request.user
            ):
                schedule.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied
        else:
            if schedule.user == request.user:
                schedule.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied

    # def post(self, request, pk):
    #     schedule = self.get_object(pk)
    #     print("문자열:", schedule.user)
    #     print("request", request.user)

    #     print(schedule.team)


class ScheduleSearch(APIView):
    pass
