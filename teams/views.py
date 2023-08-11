from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied

from .serializers import TeamSerializer
from users.models import User
from .models import Team


class NewTeam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            new_team = serializer.save()
            team_leader = User.objects.get(username=request.user)
            team_leader.leader = new_team
            team_leader.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Teams(APIView):
    permission_classes = [IsAuthenticated]

    def get_team(self, team_id):
        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise NotFound("해당 팀이 없습니다.")

    def get_user(self, user):
        try:
            return User.objects.get(username=user)
        except User.DoesNotExist:
            raise NotFound("해당 사용자가 없습니다.")

    def post(self, request, team_id):
        team = self.get_team(team_id)
        user = self.get_user(request.user)

        if not team.members.filter(id=user.id).exists():
            return Response(
                {"errors": "해당 팀에 소속된 사용자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        team.members.remove(user)

        return Response(status=status.HTTP_200_OK)

    def put(self, request, team_id):
        team = self.get_team(team_id)

        serializer = TeamSerializer(
            team,
            data=request.data,
            partial=True,
        )

        try:
            team.leader.get(username=request.user)
        except:
            raise PermissionDenied("팀 정보수정은 팀장만 가능합니다.")

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(
            {"errors": "올바르지 않은 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, team_id):
        team = self.get_team(team_id)

        try:
            team.leader.get(username=request.user)
        except:
            raise PermissionDenied("팀 삭제는 팀장만 가능합니다.")

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
