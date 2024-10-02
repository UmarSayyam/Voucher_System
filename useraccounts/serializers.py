from rest_framework import serializers
from .models import CustomUserModel
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'company_name', 'phone_number', 'country', 'state', 'city')

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()

        if CustomUserModel.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exist.')
        return attrs
    
    def create(self, validate_data):
        
        user = CustomUserModel.objects.create_user(**validate_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() #(write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self):
        try:
            RefreshToken(self.token)
        except Exception as e:
            raise serializers.ValidationError("Invalid token")