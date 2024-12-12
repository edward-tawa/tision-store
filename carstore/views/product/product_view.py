from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from carstore.models import CustomUser, Product, Order, OrderProduct, Profile, Customer
from carstore.serialiazers import CustomUserSerializer, ProductSerializer, OrderSerializer, ProfileSerializer, CustomerSerializer
from carstore.email_thread import Util
from django.core.exceptions import ValidationError

class ProductListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    def get(self, request):
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer, status=status.HTTP_200_OK)

class ProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error":"Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
class ProductCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"Error":"Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ProductDeleteView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error":"Product does not exist"})
                
