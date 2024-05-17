# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'fullName', 'email', 'password', 'confirmPassword')

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("As senhas não coincidem.")
        if len(data['fullName'].split()) < 2:
            raise serializers.ValidationError("Por favor, digite seu nome completo (nome e sobrenome).")
        return data

    def create(self, validated_data):
        fullName = validated_data.pop('fullName')
        password = validated_data.pop('password')
        validated_data.pop('confirmPassword')
        first_name, last_name = fullName.split(' ', 1)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
