from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .serializers import SignUpUserSerializer, UserInfoSerializer
from .models import User


class Signup(APIView):
    def post(self, request):
        user = SignUpUserSerializer(data=request.data)

        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"errors": "이미 존재하는 아이디입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_valid():
            user = User.objects.create_user(
                username=request.data["username"],
                name=request.data["name"],
                password=request.data["password"],
                email=request.data["email"],
            )
            print(user)
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        raise ParseError("잘못된 요청입니다.")


class Login(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        if not (username and password):
            raise ParseError("아이디 또는 비밀번호가 없습니다.")

        user = authenticate(  # 성공 시 user instance 반환 아닐 시 None 반환
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(
            {"errors": "올바른 유저정보가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST
        )


class Logout(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class CheckUsername(APIView):
    def post(self, request):
        username = request.data["username"]
        if not username:
            raise ParseError("아이디 값이 없습니다.")
        if User.objects.filter(username=username).exists():
            return Response(
                {"errors": "이미 존재하는 아이디입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "사용가능한 아이디입니다."}, status=status.HTTP_200_OK)


class UserInfo(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("존재하지 않는 유저입니다.")

    def get(self, request, username):
        user = self.get_object(username)

        if user != request.user:
            raise PermissionDenied("타인 정보 조회는 불가합니다.")

        serializer = UserInfoSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        user = self.get_object(username)

        if user != request.user:
            raise PermissionDenied("비밀번호 변경 권한이 없습니다.")

        user.set_password(request.data["password"])
        user.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, username):
        user = self.get_object(username)

        if user != request.user:
            raise PermissionDenied("권한이 없습니다.")

        user.is_active = False
        user.save()
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)
