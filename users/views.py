from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response

from users.models import User
from users.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly




class LoginView(TokenObtainPairView):
    ...


class UserView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        user = User.objects.all()

        serializer = UserSerializer(user, many=True)

        return Response(serializer.data, 200)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, 201)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsOwnerOrAdmin]

    def get(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, 200)

    def patch(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)