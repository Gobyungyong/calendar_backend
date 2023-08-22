from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommentSerializer
from schedules.models import Schedule
from .models import Comment


class NewComment(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        try:
            schedule = Schedule.objects.get(id=request.data.get("schedule_id"))
        except Schedule.DoesNotExist:
            raise NotFound("해당하는 일정이 없습니다.")

        if serializer.is_valid():
            new_comment = serializer.save(author=request.user, schedule=schedule)
            return Response(
                CommentSerializer(new_comment).data,
                status=status.HTTP_201_CREATED,
            )

        raise ParseError("잘못된 요청입니다.")


class Comments(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise NotFound("존재하지 않는 댓글입니다.")

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)

        if (comment.author != request.user) and (
            comment.schedule.team.team_leader != request.user
        ):
            raise PermissionDenied("삭제권한이 없습니다.")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, comment_id):
        comment = self.get_object(comment_id)

        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True,
        )

        if (comment.author != request.user) and (
            comment.schedule.team.team_leader != request.user
        ):
            raise PermissionDenied("수정권한이 없습니다.")

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        raise ParseError("잘못된 요청입니다.")
