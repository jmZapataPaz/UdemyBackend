from rest_framework import serializers
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255, 
        required=True, 
        allow_blank=False,
        error_messages={
            'blank': 'Name cannot be blank.'
        })
    description = serializers.CharField(
        required=True, 
        allow_blank=False,
        error_messages={
            'blank': 'Description cannot be blank.'
        })
    
    file = serializers.ImageField(source = 'image', required = True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'file']