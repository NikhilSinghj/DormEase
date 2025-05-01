from rest_framework import serializers
from .models import User , Students , Room ,Warden

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','name','room_no','username', 'password', 'email', 'f_name', 'contact']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            name=validated_data['name'],
            contact=validated_data['contact'],
            f_name=validated_data['f_name'],
            room_no = validated_data['room_no']
        )
        return user



class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class RoomSerializer(serializers.ModelSerializer):

    class Meta:

        model = Room

        fields = ['id', 'hostel', 'room_number', 'capacity']


class WardenSerializer(serializers.ModelSerializer):

    class Meta:

        model = Warden

        fields = ['id', 'user', 'hostel']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ['id','email','std_name', 'dept', 'year', 'u_rollno', 'std_contact', 'f_contact', 'm_contact', 'room_altd', 'seater_altd']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','password','username','email','std_name', 'dept', 'year', 'u_rollno', 'std_contact', 'f_contact', 'm_contact', 'room_altd', 'seater_altd']
