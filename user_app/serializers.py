# user_app/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered'}) 
        
        account = User(**validated_data)
        account.set_password(password)
        account.save()
        return account
