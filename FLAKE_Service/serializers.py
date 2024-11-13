from .models import Tutor ,Administrador, Persona
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    cedula = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'cedula'

    def validate(self, attrs):
        credentials = {self.username_field: attrs[self.username_field], 'password': attrs['password']}
        self.user = authenticate(**credentials)

        if not self.user or not self.user.is_active:
            raise AuthenticationFailed('No active account found with the given credentials')

        data = {}

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Agregar información adicional al token
        data['user_type'] = self.get_user_type(self.user)

        return data

    def get_user_type(self, user):
        if hasattr(user, 'administrador'):
            return 'Administrador'
        elif hasattr(user, 'tutor'):
            return 'Tutor'
        else:
            return 'Unknown'