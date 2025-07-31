import os
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create(request):
    if not request.user.userhasroles_set.filter(id_rol__id='ADMIN').exists():
        return Response(
            {
                "message": "You do not have permission to update categories.",
                "statusCode": status.HTTP_403_FORBIDDEN
            },
            status=status.HTTP_403_FORBIDDEN
        )
        
    serializer = ProductSerializer(data=request.data)
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
    uploaded_images = request.FILES.getlist('files')
    image_urls = []
    if uploaded_images:
        for index, image in enumerate(uploaded_images[:2]):
            file_path = f'uploads/products/{serializer.instance.id}/{image.name}'
            saved_path = default_storage.save(file_path, ContentFile(image.read()))
            image_urls.append(default_storage.url(saved_path))
        serializer.instance.image1 = image_urls[0] if len(image_urls) > 0 else None
        serializer.instance.image2 = image_urls[1] if len(image_urls) > 1 else None
    serializer.instance.save()
    
    product_data = ProductSerializer(serializer.instance).data
    return Response({
        **product_data,
        "image1": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{serializer.instance.image1}' if serializer.instance.image1 else None,
        "image2": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{serializer.instance.image2}' if serializer.instance.image2 else None,
    }, status=status.HTTP_201_CREATED)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_products_by_category(request, id_category):
    try:
        products = Product.objects.filter(id_category=id_category)
        if not products.exists():
            return Response({
                "message": "No se encontraron productos para esta categoría.",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        serializer_products = []
        for product in products:
            serializer_data = ProductSerializer(product).data
            serializer_data['image1'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image1}' if product.image1 else None
            serializer_data['image2'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image2}' if product.image2 else None
            serializer_products.append(serializer_data)
        return Response(serializer_products, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "message": f"Error al obtener los productos: {str(e)}",
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def delete_by_id_product(request, id_product):
    if not request.user.userhasroles_set.filter(id_rol__id='ADMIN').exists():
        return Response(
            {
                "message": "You do not have permission to update categories.",
                "statusCode": status.HTTP_403_FORBIDDEN
            },
            status=status.HTTP_403_FORBIDDEN
        )
        
    try:
        product = Product.objects.get(id=id_product)
        
        if product.image1:
            image1_path = product.image1
            if image1_path.startswith('/media/'):
                image1_path = image1_path.replace('/media/', '')
            elif image1_path.startswith('media/'):
                image1_path = image1_path.replace('media/', '')
            
            if default_storage.exists(image1_path):
                default_storage.delete(image1_path)
        
        if product.image2:
            image2_path = product.image2
            if image2_path.startswith('/media/'):
                image2_path = image2_path.replace('/media/', '')
            elif image2_path.startswith('media/'):
                image2_path = image2_path.replace('media/', '')
            
            if default_storage.exists(image2_path):
                default_storage.delete(image2_path)
        
        product.delete()
        
        return Response({
            "message": "Producto eliminado correctamente.",
            "statusCode": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)  

    except Product.DoesNotExist:
        return Response({
            "message": "Producto no encontrado.",
            "statusCode": status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "message": f"Error al eliminar el producto: {str(e)}",
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def update_by_id_product(request, id_product):
    if not request.user.userhasroles_set.filter(id_rol__id='ADMIN').exists():
        return Response(
            {
                "message": "You do not have permission to update categories.",
                "statusCode": status.HTTP_403_FORBIDDEN
            },
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        product = Product.objects.get(id=id_product)
    except Product.DoesNotExist:
        return Response({
            "message": "Producto no encontrado.",
            "statusCode": status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "message": f"Error al obtener el producto: {str(e)}",
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    serializer = ProductSerializer(product, data=request.data, partial=True)
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
    
    if 'files' in request.FILES:
        files = request.FILES.getlist('files')
        
        if len(files) >= 1:
            if product.image1:
                image1_path = product.image1
                if image1_path.startswith('/media/'):
                    image1_path = image1_path.replace('/media/', '')
                elif image1_path.startswith('media/'):
                    image1_path = image1_path.replace('media/', '')
                
                if default_storage.exists(image1_path):
                    default_storage.delete(image1_path)
            
            file_path1 = f'uploads/products/{product.id}/{files[0].name}'
            saved_path1 = default_storage.save(file_path1, ContentFile(files[0].read()))
            product.image1 = default_storage.url(saved_path1)
        
        if len(files) >= 2:
            if product.image2:
                image2_path = product.image2
                if image2_path.startswith('/media/'):
                    image2_path = image2_path.replace('/media/', '')
                elif image2_path.startswith('media/'):
                    image2_path = image2_path.replace('media/', '')
                
                if default_storage.exists(image2_path):
                    default_storage.delete(image2_path)
            
            file_path2 = f'uploads/products/{product.id}/{files[1].name}'
            saved_path2 = default_storage.save(file_path2, ContentFile(files[1].read()))
            product.image2 = default_storage.url(saved_path2)
        
        product.save()
    
    image1_url = request.build_absolute_uri(product.image1) if product.image1 else None
    image2_url = request.build_absolute_uri(product.image2) if product.image2 else None
    
    serializer_data = ProductSerializer(product).data
    return Response({
        **serializer_data,
        "image1": image1_url,
        "image2": image2_url,
        "message": "Producto actualizado correctamente.",
        "statusCode": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)
