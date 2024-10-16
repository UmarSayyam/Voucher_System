from rest_framework import generics, status
from django.shortcuts import render
from .serializers import MemberSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vouchers.models import Voucher
from vouchers.serializers import VoucherSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Member, MemberVoucherUsage, Voucher
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def voucher_notification(request):
    return render(request, 'member/voucher_notification.html')

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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        member_id = request.data.get('member_id')
        voucher_id = request.data.get('voucher_id')

        try:
            # Fetch the member and voucher
            member = Member.objects.get(id=member_id)
            voucher = Voucher.objects.get(id=voucher_id)

        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Voucher.DoesNotExist:
            self.trigger_websocket_notification('Voucher not found')  # Send WebSocket notification
            return Response({"error": "Voucher not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Check if the authenticated user is the creator of the member
            if request.user != member.created_by:
                message = "You do not have permission to use this voucher for this member."
                self.trigger_websocket_notification(message)  # Send WebSocket notification
                raise PermissionDenied(message)

            # Birthday month check
            if voucher.birthday_members_only:
                current_month = datetime.now().month
                birthday_month = member.date_of_birth.month

                if current_month != birthday_month:
                    message = "You cannot use the voucher because this is not your birthday month."
                    self.trigger_websocket_notification(message)  # Trigger WebSocket notification
                    return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        
            # Handle voucher usage and expiry
            usage_record, created = MemberVoucherUsage.objects.get_or_create(member=member, voucher=voucher)

            if usage_record.is_expired:
                message = "Your voucher has expired."
                self.trigger_websocket_notification(message)  # Trigger WebSocket notification for expired voucher
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
            
            usage_record.usage_count += 1

            if usage_record.usage_count >= voucher.maximum_usability_of_voucher:
                usage_record.is_expired = True
                usage_record.save()

                message = "Your voucher has expired."
                self.trigger_websocket_notification(message)  # Trigger WebSocket notification for expired voucher
                return Response({"message": message}, status=status.HTTP_200_OK)
            
            else:
                usage_record.save()
                remaining_uses = voucher.maximum_usability_of_voucher - usage_record.usage_count
                
                message = f"Voucher used successfully. You have {remaining_uses} uses remaining."
                self.trigger_websocket_notification(message)  # Trigger WebSocket notification for successful usage

                return Response({
                    "message": message
                }, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            # Send WebSocket notification before raising PermissionDenied error
            self.trigger_websocket_notification(str(e))
            raise  # Re-raise the exception after sending the WebSocket message
        

    # Method to trigger WebSocket notification
    def trigger_websocket_notification(self, message):
        print(f"WebSocket message: {message}")  # Debugging
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "voucher_group",  # WebSocket group name
            {
                "type": "send_voucher_message",  # Type corresponds to the method in the consumer
                "message": message
            }
        )