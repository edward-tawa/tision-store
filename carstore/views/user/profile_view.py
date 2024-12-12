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

class ProfileView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user_serializer = CustomUserSerializer(user)
            profile, created = Profile.objects.get_or_create(user=user)
            if created or profile:
                profile_serializer = ProfileSerializer(profile)
                if profile_serializer:
                    return Response({**profile_serializer.data, **user_serializer.data}, status=status.HTTP_200_OK)
            return Response({"error_message":"Could not retirive profile"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error":"Customer does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error":"Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewUpdate(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    def put(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error":"profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
















        
        
