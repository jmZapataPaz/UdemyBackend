from rest_framework import serializers
from address.serializers import AddressSerializer
from orders.models import Order, OrderHasProducts
from products.serializers import ProductSerializer
from users.serializer import UserSerializer

class order_has_products_serializer(serializers.ModelSerializer):
    product = ProductSerializer(source = 'id_product')
    
    class Meta:
        model = OrderHasProducts
        fields = ['product', 'quantity', 'created_at', 'updated_at']

class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(source = 'id_user')
    address = AddressSerializer(source = 'id_address')
    orderHasProducts = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'status', 'created_at', 'updated_at', 'orderHasProducts']
        
    def get_orderHasProducts(self, obj):
        order_has_products = OrderHasProducts.objects.filter(id_order=obj)
        return order_has_products_serializer(order_has_products, many=True).data
    