from rest_framework import generics, status
from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vouchers.models import Voucher
from vouchers.serializers import VoucherSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Member, MemberVoucherUsage

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


class UseVoucherView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        member_id = request.data.get('member_id')
        voucher_id = request.data.get('voucher_id')
        try:
            member = Member.objects.get(id=member_id)
            voucher = Voucher.objects.get(id=voucher_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        except Voucher.DoesNotExist:
            return Response({"error": "Voucher not found"}, status=status.HTTP_404_NOT_FOUND)
        usage_record, created = MemberVoucherUsage.objects.get_or_create(member=member, voucher=voucher)
        if usage_record.is_expired:
            return Response({"message": "Your voucher has expired."}, status=status.HTTP_400_BAD_REQUEST)
        usage_record.usage_count += 1
        if usage_record.usage_count >= voucher.maximum_usability_of_voucher:
            usage_record.is_expired = True
            usage_record.save()
            return Response({"message": "Your voucher has expired."}, status=status.HTTP_200_OK)
        else:
            usage_record.save()
            remaining_uses = voucher.maximum_usability_of_voucher - usage_record.usage_count
            return Response({
                "message": f"Voucher used successfully. You have {remaining_uses} uses remaining."
            }, status=status.HTTP_200_OK)
