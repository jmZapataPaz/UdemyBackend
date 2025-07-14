from rest_framework import serializers
from .models import User
import bcrypt

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email', 'password', 'phone', 'image', 'notification_token', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}  #para que el campo de contraseña no se muestre en las respuestas
        }
        
    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8') #todo esto para encriptar la contraseña
        user = User.objects.create(**validated_data)
        return user
    
         