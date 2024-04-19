from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from shop.models import CustomUser
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Esta vista personaliza la obtención de tokens JWT para la autenticación de usuarios.
    Puedes añadir lógica adicional antes o después de la autenticación en el método post.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Aquí puedes añadir cualquier lógica adicional antes de la autenticación
        return super().post(request, *args, **kwargs)
class LoginView(views.APIView):
    """
    Vista para autenticar usuarios. Toma un nombre de usuario y contraseña,
    autentica al usuario, y devuelve un token de autenticación si es exitoso.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Obtiene o crea un token para el usuario autenticado
            token, created = Token.objects.get_or_create(user=user)
            # Devuelve el token y el username como respuesta
            return Response({
                'token': token.key,
                'username': username  # Asegúrate de que el manejo del username aquí es seguro y adecuado para tu caso de uso
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas o usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(views.APIView):
    """
    Vista para cerrar sesión de un usuario. Invalida el token de autenticación del usuario,
    requiriendo que vuelva a autenticarse para obtener un nuevo token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Obtiene el token del usuario y lo elimina para cerrar sesión
            request.user.auth_token.delete()
            return Response({'success': 'Sesión cerrada con éxito.'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            # Maneja el caso donde el token no se encuentra o ya fue eliminado
            return Response({'error': 'Algo salió mal, no se pudo cerrar la sesión.'}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyUserToken(views.APIView):
    """
    Verifica si el token proporcionado pertenece al usuario especificado.
    
    Acepta el ID del usuario y un token, verificando si este último es válido y pertenece al usuario indicado.
    Solo usuarios autenticados pueden realizar esta operación.

    Métodos:
    - POST: Recibe 'user_id' y 'token' como datos, retorna confirmación de validez o error.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        token_key = request.data.get('token')

        try:
            usuario = get_object_or_404(CustomUser, pk=user_id)
            token = Token.objects.get(key=token_key, user=usuario)  # Optimizado para verificar directamente la relación

            # La verificación del token se realiza implícitamente al buscarlo.
            return Response({"success": "El token es válido y corresponde al usuario."}, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({"error": "Token inválido o no encontrado."}, status=status.HTTP_404_NOT_FOUND)