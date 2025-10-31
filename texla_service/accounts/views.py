from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserLiteSerializer
from .permissions import IsAdmin

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]  # only admins can create users

class MeView(generics.RetrieveAPIView):
    serializer_class = UserLiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
