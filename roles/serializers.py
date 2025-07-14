from rest_framework import serializers
from roles.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'image', 'route', 'created_at', 'updated_at']