from rest_framework import serializers
from address.models import Address
from users.models import User

class AddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(
        required=True,
        allow_blank=True,
        error_messages={
            'blank': 'Address cannot be blank.',
        }            
    )
    neighborhood = serializers.CharField(
        required=True,
        allow_blank=True,
        error_messages={
            'blank': 'Neighborhood cannot be blank.',
        }
    )
    id_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            'does_not_exist': 'User does not exist.',
        }
    )
    
    class Meta:
        model = Address
        fields = ['id','id_user','address', 'neighborhood', 'created_at', 'updated_at']