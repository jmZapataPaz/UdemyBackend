from rest_framework import serializers

from categories.models import Category
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': 'El nombre del producto no puede estar en blanco.'
        }    
    )
    description = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': 'La descripción del producto no puede estar en blanco.'
        }
    )
    
    price = serializers.FloatField(
        required=True,
        error_messages={
            'blank': 'El precio del producto no puede estar en blanco.',
        }
    )
    id_category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages={
            'does_not_exist': 'La categoría especificada no existe.',
        }
    )
    
    class Meta:
        model = Product
        fields = ['id', 'id_category', 'name', 'description', 'price', 'image1', 'image2', 'created_at', 'updated_at']
    