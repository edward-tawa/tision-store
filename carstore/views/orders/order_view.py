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

class OrdersListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            orders = Order.objects.filter(customer=customer)
            if not orders:
                return Response({"error":"No orders found"}, status=status.HTTP_404_NOT_FOUND)
            order_serializer = OrderSerializer(orders, many=True)
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(id=order_id, customer=customer)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def post(self, request):
        try:
            serializer = OrderSerializer(data=request.data)
            customer = Customer.objects.get(user=request.user)
            if serializer.is_valid():
                order = serializer.save(customer=customer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error":"Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderUpdateView(APIView):
    def put(self, request, order_id):
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(id=order_id, customer=customer)
            serializer = OrderSerializer(order, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error":"Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND) 


class OrderDeleteView(APIView):
    def delete(self, request, order_id):
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(order_id, customer)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"error":"Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({"error":"Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


