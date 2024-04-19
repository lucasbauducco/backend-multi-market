from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from shop.serializers import CustomUserSerializer, StateChangeSerializer, CustomUserDetailSerializer
from django.shortcuts import get_object_or_404
from shop.models import UserHistory
import json

User = get_user_model()
class CreateUserView(views.APIView):
    """
    Vista para crear nuevos usuarios. Solo los administradores tienen permiso para crear nuevos usuarios.
    
    Métodos:
    - POST: Crea un nuevo usuario basado en los datos proporcionados.
    """
    
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUserView(views.APIView):
    """
    Vista para actualizar la información de un usuario existente. Solo los administradores tienen permiso para actualizar usuarios.
    
    Métodos:
    - PUT: Actualiza la información de un usuario existente.
    """
    
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            original_data = json.dumps(serializer.initial_data)
            updated_user = serializer.save()
            UserHistory.objects.create(
                user=updated_user,
                modified_by=request.user,
                motive=serializer.validated_data.get('motive', ''),
                changes=original_data
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserStateView(views.APIView):
    """
    Vista para cambiar el estado de un usuario.

    Permite a los usuarios administradores cambiar el estado de un usuario específico mediante un método POST.
    Registra el cambio de estado en el historial del usuario.

    Atributos:
        permission_classes (list): Define las clases de permiso para la vista. Aquí, se restringe a usuarios administradores.

    Métodos:
        post: Maneja las solicitudes POST para cambiar el estado de un usuario.
    """

    # Define que solo los usuarios administradores pueden acceder a esta vista.
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = StateChangeSerializer(data=request.data)
        if serializer.is_valid():
            user.state = serializer.validated_data['state']
            user.save()

            UserHistory.objects.create(
                user=user,
                modified_by=request.user,
                changes=f"State changed to {user.state}",
                motive=serializer.validated_data.get('motive', '')
            )
            return Response({'status': 'state changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserDetailView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def get_permissions(self):
        """
        Permite al usuario acceder a su propio perfil o a administradores.
        """
        if self.request.user.username == self.kwargs['username'] or self.request.user.is_staff:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]