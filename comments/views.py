from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommentSerializer
from schedules.models import Schedule
from .models import Comment


class NewComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        try:
            schedule = Schedule.objects.get(id=request.data.get("schedule"))
        except Schedule.DoesNotExist:
            raise NotFound("해당하는 일정이 없습니다.")

        if serializer.is_valid():
            newSchedule = serializer.save(author=request.user, schedule=schedule)
            return Response(
                CommentSerializer(newSchedule).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise NotFound("존재하지 않는 댓글입니다.")

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)

        if comment.author != request.user:  # 추후 teamleader 추가 시 권한추가
            raise PermissionDenied("삭제권한이 없습니다.")

        comment.delete()
        return Response("delete success", status=status.HTTP_204_NO_CONTENT)
