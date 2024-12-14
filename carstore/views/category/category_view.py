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
from carstore.models import CustomUser, Product, Order, OrderProduct, Profile, Customer, Category
from carstore.serialiazers import CustomUserSerializer, ProductSerializer, OrderSerializer, ProfileSerializer, CustomerSerializer, CategorySerializer
from carstore.email_thread import Util
from django.core.exceptions import ValidationError





class CategoryListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error":"Category does not exist"})

class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def put(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category, data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error":"Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(APIView):
    def delete(self, request, category_id):
        try:
            category = Category.object.get(id=category_id)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist:
            return Response({"error":"Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

