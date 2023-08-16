from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from .models import Schedule
from . import serializers


# 스케줄의 대략적인 정보
class Schedules(APIView):
    def get(self, request):
        all_schedules = Schedule.objects.filter(user=request.user)
        serializer = serializers.ScheduleSerializer(
            all_schedules,
            many=True,
        )
        return Response(serializer.data)


# 스케줄의 세부 정보 (description, 개인or팀, 댓글..? )
class ScheduleDetail(APIView):
    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = serializers.ScheduleSerializer(schedule)
        return Response(serializer.data)
