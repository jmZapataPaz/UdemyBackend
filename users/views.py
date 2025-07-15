import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from roles.models import Role
from roles.serializers import RoleSerializer
from users.models import User, UserHasRoles
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_user_by_id(request, id_user):
    try: 
        user = User.objects.get(id=id_user)
    except User.DoesNotExist:
        return Response(
            {
                "message": "User not found.",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, 
            status=status.HTTP_404_NOT_FOUND
        )
    roles = Role.objects.filter(userhasroles__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)
    user_data = {       
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email,
        "phone": user.phone,
        "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
        "notification_token": user.notification_token,
        "roles": roles_serializer.data
    }    
    return Response(user_data, status=status.HTTP_200_OK)   


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_all_users(request):
    users = User.objects.all()
    all_users_data = []
    
    for user in users:
        roles = Role.objects.filter(userhasroles__id_user=user)
        roles_serializer = RoleSerializer(roles, many=True)
        user_data = {       
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "phone": user.phone,
            "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
            "notification_token": user.notification_token,
            "roles": roles_serializer.data
        }
        all_users_data.append(user_data)
    return Response(all_users_data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])  #ruta protegida y que se requiere autenticacion
def update(request, id_user):
    if request.user.id != id_user:
        return Response(
            {
                "message": "You do not have permission to update this user.",
                "statusCode": status.HTTP_403_FORBIDDEN
            }, 
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        user = User.objects.get(id=id_user)
    except User.DoesNotExist:
        return Response(
            {
                "message": "User not found.",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, 
            status=status.HTTP_404_NOT_FOUND
        )
    name = request.data.get('name', None) #"Esto para que no sea obligatorio"
    lastname = request.data.get('lastname', None)
    phone = request.data.get('phone', None)
    
    if name is None and lastname is None and phone is None:
        return Response(
            {
                "message": "At least one field must be provided for update.",
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    if name is not None:
        user.name = name
        
    if lastname is not None:
        user.lastname = lastname
        
    if phone is not None:
        user.phone = phone
    
    user.save()
    roles = Role.objects.filter(userhasroles__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)
    
    user_data = {       
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email,
        "phone": user.phone,
        "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
        "notification_token": user.notification_token,
        "roles": roles_serializer.data
    }  
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def updateWithImage(request, id_user):
    # Convertir id_user a entero para la comparación
    try:
        id_user = int(id_user)
    except ValueError:
        return Response(
            {
                "message": "Invalid user ID format.",
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.id != id_user:
        return Response(
            {
                "message": "You do not have permission to update this user.",
                "statusCode": status.HTTP_403_FORBIDDEN
            }, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.get(id=id_user)
    except User.DoesNotExist:
        return Response(
            {
                "message": "User not found.",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    name = request.data.get('name', None)
    lastname = request.data.get('lastname', None)
    phone = request.data.get('phone', None)
    image = request.FILES.get('file', None)
    
    if name is None and lastname is None and phone is None and image is None:
        return Response(
            {
                "message": "At least one field must be provided for update.",
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if name is not None:
        user.name = name
        
    if lastname is not None:
        user.lastname = lastname
        
    if phone is not None:
        user.phone = phone
        
    if image is not None:
        file_extension = os.path.splitext(image.name)[1]
        file_path = f'uploads/users/{user.id}/{image.name}'
        
        try:
            saved_path = default_storage.save(file_path, ContentFile(image.read()))
            user.image = default_storage.url(saved_path)
        except Exception as e:
            return Response(
                {
                    "message": f"Error saving image: {str(e)}",
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    user.save()
    roles = Role.objects.filter(userhasroles__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)
    
    user_data = {       
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email,
        "phone": user.phone,
        "image": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{user.image}' if user.image else None,
        "notification_token": user.notification_token,
        "roles": roles_serializer.data
    }  
    return Response(user_data, status=status.HTTP_200_OK)