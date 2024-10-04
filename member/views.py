from rest_framework import generics
from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class MemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Member.objects.all()
        return Member.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Member.objects.all()
        return Member.objects.filter(created_by=self.request.user)

    def check_object_permissions(self, request, obj):
        if request.user.is_staff:
            return
        if obj.created_by != request.user:
            raise PermissionDenied("You do not have permission to access this member.")
