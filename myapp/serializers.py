from rest_framework import serializers
from .models import *
from django import forms
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['role','name','email','phone','gender','address','password','confirm_password']


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            role=validated_data['role'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            gender=validated_data['gender'],
            address=validated_data['address'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email =serializers.EmailField(max_length = 225)
    class Meta:
        model = User
        fields = ['email','password']



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['name','phone','gender','address','profile']




class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','phone','gender','address','profile']
    
class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['verify']




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['product_name','category','quantity','price','pic','description']



class AddToCartSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Mycart
        fields = ['quantity']


class MyCartSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Mycart
        fields = ['user','product','quantity']


class BuyProductSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Buyproduct
        fields = ['address','payment_method']


class BuyProductViewSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Buyproduct
        fields = ['product','address','status','payment_method','total_amount','ordered_date','quantity']


class UpdateOderStatusSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Buyproduct
        fields = ['status']