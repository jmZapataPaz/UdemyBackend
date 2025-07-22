from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from address.models import Address
from address.serializers import AddressSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_address(request):
    serializer = AddressSerializer(data=request.data)
    if not serializer.is_valid():
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        error_response = {
            "message": error_messages,
            "statusCode": status.HTTP_400_BAD_REQUEST
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_address_by_user(request, id_user):
    try:
        addresses = Address.objects.filter(id_user=id_user)
        if not addresses.exists():
            return Response(
                {
                    "message": "No addresses found for this user", 
                    "statusCode": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_addresses = AddressSerializer(addresses, many=True).data
        return Response(serializer_addresses, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {
                "message": str(e), 
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address(request, id_address):
    try:
        address = Address.objects.get(id=id_address)
        address.delete()
        return Response(True, status=status.HTTP_200_OK)
        
    except Address.DoesNotExist:
        return Response(
            {
                "message": "Address not found", 
                "statusCode": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )
        
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_address(request, id_address):
    try:
        address = Address.objects.get(id=id_address)
        
    except Address.DoesNotExist:
        return Response(
            {
                "message": "Address not found", 
                "statusCode": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = AddressSerializer(address, data=request.data, partial=True)
    if not serializer.is_valid():
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        error_response = {
            "message": error_messages,
            "statusCode": status.HTTP_400_BAD_REQUEST
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    