
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


-----------------------------------------

✔️사용자가 조회할 수 있는 항목들( get )
🔔 [o] 로그인을 한 사람만 달력을 조회할 수 있도록 예외처리 할 것
- [o] 팀의 스케줄 
- [o] 개인의 스케줄 
➡️ Schedule 모델에서 team에 user이 있으면 팀의 스케줄을 보여주고, 없으면 개인의 스케줄만 보여주기

- [] 일정에 남겼던 댓글 조회하기 


- [o]검색어를 입력하면 사용자가 정한 제목과 일치하는 일정을 찾도록하기(검색어와 일정명과의 매칭)
➡️그러려면! 일정들의 제목들을 다 한 곳으로 모아서 검색어랑 제목이 일치하게 만들기


✔️달력에서 사용자가 생성하는 요소들 ( post )
-  [o] 개인 일정 추가하기
-  [o] 팀의 일정은 팀에 소속된 인간들이 추가할 수 있음

✔️달력에서 사용자가 수정하는 요소들 (put)
🔔개인 일정일 경우, 수정하려는 사람과 일정을 작성한 사람이 일치하도록 설정
-  [o] 개인 일정 수정
🔔팀의 일정일 경우, 수정할 수 있는 권한을 팀을 구성한 사람에게만 부여+ 작성자
-  [o] 팀 일정 수정

✔️달력에서 사용자가 삭제하는 요소들(delete)
🔔개인의 일정일 경우, 삭제하려는 사람과 등록한 사람이 일치할 때만 삭제할 수 있도록 만들기
-  [o] 개인 일정 삭제
🔔팀의 일정일 경우, 일정을 삭제할 수 있는 권한은 팀을 만든 사람에게만 부여하기 + 작성자 
- [o] 팀 일정 삭제