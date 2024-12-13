from rest_framework import serializers
from carstore.models import CustomUser, Product, Order, Profile, Customer, Category


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "date_of_birth", "gender", "email", "password"]
        extra_kwargs = {"password":{"write_only": True}}

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "address", "user", "phone_number", "gender"]
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =[
                    "id",
                    "product_name",
                    "description",
                    "quantity",
                    "price",
                    "category",
                    "image",
                    "created_at", 
                    "updated_at", 
                ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "order_date", "customer", "order_status", "order_products"]


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order", "product", "quantity", "unit_price"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "bio", "profile_picture", "phone_number"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description"]

    
