from rest_framework import serializers

from core.user.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',read_only=True,format='hex')
    
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id","username","email","password","first_name","last_name","created","updated"]
        red_only_field = ["is_active", "is_staff", "is_superuser"]