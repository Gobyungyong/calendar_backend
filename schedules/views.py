from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from teams.models import Team
from . import serializers
from .serializers import TeamSerializer

from comments.serializers import ScheduleCommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class Schedules(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["모든 일정 API"],
        description="로그인 시 사용자의 개인 일정 및 팀의 스케줄 조회",
        summary="전체 일정 조회",
        responses={
            200: serializers.ScheduleSerializer(many=True),  # HTTP 200 OK
            404: "일정을 찾을 수 없음",  # HTTP 404 Not Found
            403: "허가 거부됨",  # HTTP 403 Forbidden
        },
    )
    # def get(self, request):
    #     try:
    #         user = request.user

    #         if user.team_set.all().exists():
    #             teams = user.team_set.all()
    #             user_schedules = Schedule.objects.filter(user=user)
    #             team_schedules = Schedule.objects.filter(team__in=teams)
    #             schedules = user_schedules.union(team_schedules)

    #             schedule_serializer = serializers.ScheduleSerializer(
    #                 schedules,
    #                 many=True,
    #             )
    #             team_serializer = serializers.TeamSerializer(
    #                 teams,
    #                 many=True,
    #             )

    #             response_data = {
    #                 "schedules": schedule_serializer.data,
    #                 "teams": team_serializer.data,
    #             }
    #             return Response(response_data, status=status.HTTP_200_OK)
    #         else:
    #             user_schedules = Schedule.objects.filter(user=user)
    #             serializer = serializers.ScheduleSerializer(
    #                 user_schedules,
    #                 many=True,
    #             )
    #             return Response(serializer.data, status=status.HTTP_200_OK)

    #     except NotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except PermissionDenied:
    #         return Response(status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        try:
            user = request.user

            if user.is_authenticated:  # 사용자가 로그인한 경우
                if user.team_set.all().exists():
                    teams = user.team_set.all()
                    user_schedules = Schedule.objects.filter(user=user)
                    team_schedules = Schedule.objects.filter(team__in=teams)
                    schedules = user_schedules.union(team_schedules)

                    schedule_serializer = serializers.ScheduleSerializer(
                        schedules,
                        many=True,
                    )
                    team_serializer = serializers.TeamSerializer(
                        teams,
                        many=True,
                    )

                    response_data = {
                        "schedules": schedule_serializer.data,
                        "teams": team_serializer.data,
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    user_schedules = Schedule.objects.filter(user=user)
                    serializer = serializers.ScheduleSerializer(
                        user_schedules,
                        many=True,
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:  # 익명 사용자인 경우
                return Response(
                    {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
                )

        except NotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["모든 일정 API"],
        summary="일정 추가",
        description="일정 추가",
        responses={
            201: serializers.ScheduleSerializer,  # HTTP 201 Created
            400: OpenApiTypes.OBJECT,  # HTTP 400 Bad Request
        },
        examples=[
            OpenApiExample(
                response_only=True,
                summary="성공적으로 추가된 일정",
                name="calendar",
                value={
                    "title": "일정명",
                    "description": "상세 내용",
                    "state": "상태",
                    "start_date": "시작 일시",
                    "end_date": "종료 일시",
                    "team": "팀",
                },
            ),
        ],
    )
    def post(self, request):
        team_id = request.data.get("team", None)

        if team_id is not None:
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            team = None

        serializer = serializers.ScheduleSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            schedule = serializer.save(
                user=request.user,
                team=team,
            )
            team_data = TeamSerializer(team).data

            response_data = {
                "schedule": serializers.ScheduleSerializer(schedule).data,
                "team": team_data,
            }

            return Response(
                response_data,
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

    @extend_schema(
        tags=["일정 조회, 수정 및 삭제 API"],
        summary="일정 및 연결된 댓글 조회",
        description="일정 조회 및 일정에 연결된 댓글 조회",
    )
    def get(self, request, pk):
        schedule = self.get_object(pk)
        comments = schedule.comments.all()
        serializer = serializers.ScheduleSerializer(schedule)
        comment_serializer = ScheduleCommentSerializer(
            comments,
            many=True,
        )

        response_data = {
            "schedule": serializer.data,
            "comments": comment_serializer.data,
        }

        return Response(response_data)

    @extend_schema(
        tags=["일정 조회, 수정 및 삭제 API"],
        summary="일정 수정",
        description="일정 수정(조회 API 형식에 일부 수정 가능하게 만들어놨으니, 수정하고 싶은 데이터만 작성)",
    )
    def put(self, request, pk):
        schedule = self.get_object(pk)
        if schedule.team:
            if (
                schedule.user == request.user
                or schedule.team.team_leader == request.user
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
                return Response(
                    "team_유효한 serializer",
                )
            else:
                raise PermissionDenied(
                    "팀의 일정을 수정할 권한이 없습니다",
                )

        else:
            if schedule.user == request.user:
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
                return Response(
                    "user_유효한 serializer",
                )

            else:
                raise PermissionDenied(
                    "개인의 일정을 수정할 권한이 없습니다",
                )

    @extend_schema(
        tags=["일정 조회, 수정 및 삭제 API"],
        summary="일정 삭제",
    )
    def delete(self, request, pk):
        schedule = self.get_object(pk)

        if schedule.team:
            if (
                schedule.user == request.user
                or schedule.team.team_leader == request.user
            ):
                schedule.delete()
                return Response(
                    "팀 일정이 삭제되었습니다",
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise PermissionDenied(
                    "팀의 일정을 삭제할 권한이 없습니다",
                )
        else:
            if schedule.user == request.user:
                schedule.delete()
                return Response(
                    "개인 일정이 삭제되었습니다",
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                raise PermissionDenied(
                    "개인의 일정을 삭제할 권한이 없습니다",
                )


class ScheduleSearch(APIView):
    @extend_schema(
        tags=["일정 검색 API"],
        summary="일정 검색",
        description="일정 검색 API",
        responses={
            200: serializers.ScheduleSerializer(many=True),
            400: "검색어가 필요합니다.",  # HTTP 400 Bad Request
            404: "검색 결과가 없습니다.",  # HTTP 404 Not Found
        },
        examples=[
            OpenApiExample(
                response_only=True,
                summary="일정 검색",
                name="calendar",
                value={
                    "search": " 검색어명",
                    "title": "일정명",
                    # "description": "상세 내용",
                    # "state": "상태",
                    # "start_date": "시작 일시",
                    # "end_date": "종료 일시",
                    "user": "사용자",
                    "team": "팀",
                },
            ),
        ],
    )
    def post(self, request):
        keyword = request.data.get("search")

        if keyword:
            user = request.user

            if user.team_set.all().exists():
                teams = user.team_set.all()

                user_schedules = Schedule.objects.filter(user=user).filter(
                    title__icontains=keyword
                )
                team_schedules = Schedule.objects.filter(team__in=teams).filter(
                    title__icontains=keyword
                )

                schedules = user_schedules.union(team_schedules)
            else:
                schedules = Schedule.objects.filter(user=user).filter(
                    title__icontains=keyword
                )

            if schedules.exists():
                serializer = serializers.ScheduleSerializer(
                    schedules,
                    many=True,
                )

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("검색결과가 없어!")

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
