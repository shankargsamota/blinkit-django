from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from vendor.models import Vendor



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'is_vendor', 'is_customer']


    
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)  # no need to get back after registration
    location = serializers.CharField(write_only=True, required=False)  # Adding location
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True) 

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_vendor' , 'location']

    def validate(self,attrs):
        is_vendor = attrs.get('is_vendor', False)
        location = attrs.get('location', None)

        if not attrs.get('first_name'):
            raise serializers.ValidationError({"first_name": "First name is required."})
        if not attrs.get('last_name'):
            raise serializers.ValidationError({"last_name": "Last name is required."})
        if is_vendor and not location:
            raise serializers.ValidationError({"location": "Location is required for vendors."})
        
        return attrs
    

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self,data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError('Invalid Emial or Password!')
    


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    @classmethod
    def get_token(cls,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }




# class AddressSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Address
#         fields = ['add_type' , 'id' , 'city' , 'street' , 'state' , 'country','postal_code']