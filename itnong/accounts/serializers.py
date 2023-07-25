from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()

    def create(self, validated_data):
        password = validated_data['password']
        password_confirm = validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=password,
            phone_number=validated_data['phone_number'],
        )
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm', 'phone_number']
