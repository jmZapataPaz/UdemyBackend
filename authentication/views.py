from django.shortcuts import render, get_object_or_404
from django.conf import settings
import bcrypt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from roles.models import Role
from roles.serializers import RoleSerializer
from users.models import User, UserHasRoles
from users.serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        client_role = get_object_or_404(Role, id='CLIENT') #para definir por defecto un rol al usuario
        UserHasRoles.objects.create(id_user=user, id_rol=client_role)
        
        #Esto para poner mas de 1 rol al usuario
        roles = Role.objects.filter(userhasroles__id_user=user) #doble barra para que acceda a la tabla intermedia de user has roles
        roles_serializer = RoleSerializer(roles, many=True) #esto es para que sea una lista
        response_data = {
            **serializer.data, 
            'roles': roles_serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    #manejos de errores
    error_messages= []
    for field, errors in serializer.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")
    error_response = {
        "message": error_messages,
        "statusCode": status.HTTP_400_BAD_REQUEST
    }
    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

def getCustomTokenForUser(user):
    refresh_token = RefreshToken.for_user(user)
    del refresh_token['user_id']  
    refresh_token.payload['id'] = user.id
    refresh_token.payload['name'] = user.name
    return refresh_token
 
 
@api_view(['POST'])
@permission_classes([AllowAny]) 
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {
                "message": "Email and password are required.",
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "message": "Invalid credentials.",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            }, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        # Verificar si la contraseña es válida
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            refresh_token = getCustomTokenForUser(user)
            access_token = str(refresh_token.access_token)
            
            # Obtener los roles del usuario
            roles = Role.objects.filter(userhasroles__id_user=user)
            roles_serializer = RoleSerializer(roles, many=True)
            
            user_data = {
                "user": {            
                    "id": user.id,
                    "name": user.name,
                    "lastname": user.lastname,
                    "email": user.email,
                    "phone": user.phone,
                    "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
                    "notification_token": user.notification_token,
                    "roles": roles_serializer.data
                },
                "token": 'Bearer ' + access_token
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "Invalid credentials.",
                    "statusCode": status.HTTP_401_UNAUTHORIZED
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    except ValueError:
        # La contraseña no está hasheada correctamente - comparación directa como fallback
        if user.password == password:
            # Actualizar la contraseña con hash bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')
            user.save()
            
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            
            # Obtener los roles del usuario
            roles = Role.objects.filter(userhasroles__id_user=user)
            roles_serializer = RoleSerializer(roles, many=True)
            
            user_data = {
                "user": {            
                    "id": user.id,
                    "name": user.name,
                    "lastname": user.lastname,
                    "email": user.email,
                    "phone": user.phone,
                    "image": user.image,
                    "notification_token": user.notification_token,
                    "roles": roles_serializer.data
                },
                "token": 'Bearer ' + access_token
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "Invalid credentials.",
                    "statusCode": status.HTTP_401_UNAUTHORIZED
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {
                "message": "An error occurred during login.",
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )