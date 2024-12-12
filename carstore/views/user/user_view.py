from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from carstore.models import CustomUser, Product, Order, OrderProduct, Profile, Customer
from carstore.serialiazers import CustomUserSerializer, ProductSerializer, OrderSerializer, ProfileSerializer, CustomerSerializer
from carstore.email_thread import Util
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(request_body=CustomUserSerializer)
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            email = serializer.data['email']
            username = serializer.data['username']
            password = request.data['password']

            user = CustomUser.objects.create_user(username=username, email=email, password=password)

            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            domain = get_current_site(request).domain
            relative_url = reverse("email-verify")

            abs_url = "http://" + domain + relative_url + "?token=" + access_token

            email_subject = "email verification"

            email_body = f"Hi {username} please verify your email by clicking the following link"  + " " + abs_url

            email_data = {
                "to_email": email,
                "email_subject": email_subject,
                "email_body": email_body,
            }

            Util.send_email(email_data=email_data)
            return Response({"success":"Check your email for verification link"}, status=status.HTTP_201_CREATED)
        return Response({"Bad request":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        validated_token = AccessToken(token)

        user_id = validated_token.payload['user_id']

        user = CustomUser.objects.get(id=user_id)

        if user:
            user.is_verified = True
            user.save()
            print({"Success":"Verified email successfully"})
            return Response({"Success":"Verified email successfully"}, status=status.HTTP_200_OK)
        return Response({"Failure": "Verification Failed"})


class LogInView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    @swagger_auto_schema(request_body=CustomUserSerializer)
    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print("this is",user)

        if user and user.is_verified:
            refresh_token = RefreshToken().for_user(user)
            access_token = str(refresh_token.access_token)
            return Response({"refresh_token":str(refresh_token), "access_token":access_token}, status=status.HTTP_201_CREATED)
        return Response({"Failed": "Log in Failed"}, status=status.HTTP_401_UNAUTHORIZED)

#logger = logging.getLogger(__name__)

class LogOutView(APIView):
    permission_classes =[IsAuthenticated]
    serializer_class = CustomUserSerializer
    @swagger_auto_schema(request_body=CustomUserSerializer)
    def post(self, request):
        print("This is before")
        print(request.META)
        refresh_token = request.data["refresh_token"]
        print("I am authenticated")
        try:          
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.create(token=outstanding_token)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)