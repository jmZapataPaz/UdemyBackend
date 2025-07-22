from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from orders.models import Order, OrderHasProducts
from orders.order_has_products_serializer import OrderListSerializer
from orders.serializers import OrderSerializer, OrderStatusUpdateSerializer
from products.models import Product

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    order_data = {  
        'id_user': request.data.get('id_user'),
        'id_address': request.data.get('id_address'),
        'status': request.data.get('status')  
    }
    
    serializer = OrderSerializer(data=order_data)
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
    
    order = serializer.save()
    products_data = request.data.get('products', [])
    
    if not products_data:  
        return Response(
            {"message": "No products provided", "statusCode": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    for product_data in products_data:
        try:
            product = Product.objects.get(id=product_data['id'])
            quantity = product_data.get('quantity')
            OrderHasProducts.objects.create(
                id_order=order,
                id_product=product,
                quantity=quantity   
            )
        except Product.DoesNotExist:
            order.delete()
            return Response(
                {
                    "message": f"Product with id {product_data['id']} does not exist",
                    "statusCode": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            order.delete()
            return Response(
                {
                    "message": str(e),
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )   
    
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request, id_user):
    orders = Order.objects.filter(id_user=id_user)
    if not orders.exists():
        return Response(
            {"message": "No orders found for this user", "statusCode": status.HTTP_404_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = OrderListSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    if not orders.exists():
        return Response(
            {"message": "No orders found", "statusCode": status.HTTP_404_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = OrderListSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request, id_order):
    try:   
        order = Order.objects.get (id = id_order)
        
        
    except Order.DoesNotExist:
        return Response(
            {
                "message": "Order not found", 
                "statusCode": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
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
    response_serializer = OrderListSerializer(order)
    return Response(response_serializer.data, status=status.HTTP_200_OK)