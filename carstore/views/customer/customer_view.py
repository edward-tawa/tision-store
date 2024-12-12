from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from carstore.models import CustomUser, Product, Order, OrderProduct, Profile, Customer
from carstore.serialiazers import CustomUserSerializer, ProductSerializer, OrderSerializer, ProfileSerializer, CustomerSerializer
from carstore.email_thread import Util
from django.core.exceptions import ValidationError



class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerSerializer
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    def get(self, request):
        try:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error":"No customers in the database"}, status=status.HTTP_404_NOT_FOUND)

class CustomerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer_serializer = CustomerSerializer(customer)
            return Response(customer_serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)


class UpdateCustomerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    
    def put(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer, request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error":"customer does not exist"}, status=status.HTTP_404_NOT_FOUND)


class DeleteCustomerView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"error":"Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

