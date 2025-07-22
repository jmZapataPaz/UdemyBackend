from rest_framework import serializers
from address.models import Address
from orders.models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(
        max_length=255,
        allow_blank=False,
        error_messages={
            'blank': 'El campo status no puede estar vacío.',
        }
    )
    id_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            'does_not_exist': 'El usuario especificado no existe.',
        }
    )
    id_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        error_messages={
            'does_not_exist': 'La dirección especificada no existe.',
        }
    )
    
    class Meta:
        model = Order
        fields =[ 'id', 'id_user','id_address','status', 'created_at', 'updated_at']
        
class OrderStatusUpdateSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['status']


