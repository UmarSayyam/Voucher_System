from rest_framework import generics, status
from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from vouchers.models import Voucher
from rest_framework.exceptions import NotFound
from vouchers.serializers import VoucherSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Member.objects.all()
        return Member.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = MemberSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Member.objects.all()
#         return Member.objects.filter(created_by=self.request.user)

#     def check_object_permissions(self, request, obj):
#         if request.user.is_staff:
#             return
#         if obj.created_by != request.user:
#             raise PermissionDenied("You do not have permission to access this member.")

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
            raise PermissionDenied("permission nai ay boos.")

    def update(self, request, *args, **kwargs):
        member = self.get_object()
        vouchers = request.data.get('vouchers', [])
        if not vouchers:
            return Response({"error": "koi voucher to do"}, status=status.HTTP_400_BAD_REQUEST)
        # Get the voucher instances
        voucher_objects = Voucher.objects.filter(id__in=vouchers)
        for voucher in voucher_objects:
            if voucher.created_by != request.user:
                raise PermissionDenied(f"tu mera puttar chutti kr tjy permission koi ni '{voucher.name}'.")
        # Assign vouchers to the member
        member.vouchers.set(voucher_objects)
        return Response({
            "message": f"rona band kro apka kam ho gya hy {[voucher.name for voucher in voucher_objects]} to member {member.first_name} {member.last_name}."
        }, status=status.HTTP_200_OK)




class MemberVouchersView(generics.GenericAPIView):
    def get(self, request, member_id, *args, **kwargs):
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise NotFound("Member not found")
        vouchers = member.vouchers.all()
        if vouchers.exists():
            # Serialize the vouchers and return the list
            serializer = VoucherSerializer(vouchers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "This member has no vouchers allocated."}, status=status.HTTP_200_OK)
