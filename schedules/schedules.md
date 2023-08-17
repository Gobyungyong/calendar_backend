
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Schedule
from . import serializers


class Schedules(APIView):
    def get(self, request):
        try:
            # 사용자가 요청받은 사용자인지 확인
            user = request.user

            if hasattr(user, "team"):
                # user이 소속된 team이 있는지 확인
                team = user.team
                # 만약 user가 소속된 팀이 있다면
                schedules = Schedule.objects.filter(team=team)
                # 해당 team의 schedules를 가져오기
                serializer = serializers.ScheduleSerializer(schedules, many=True)
                return Response(serializer.data)
                # 결국 serializer을 통해서 나오게 된 data는 개인이 속해있는 팀의 스케줄
            else:
                raise NotFound("현재 소속된 팀이 없습니다.")
        except NotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
