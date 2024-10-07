from rest_framework import serializers
from .models import Member
from vouchers.models import Voucher
from rest_framework.exceptions import PermissionDenied

class MemberSerializer(serializers.ModelSerializer):
    vouchers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Voucher.objects.all(), required=False
    )

    class Meta:
        model = Member
        fields = [
            'id', 'first_name', 'last_name', 'mobile_number', 'email', 'gender', 
            'date_of_birth', 'additional_phone_number', 'member_source', 'address', 
            'receive_notifications', 'marketing_email_notifications', 'marketing_text_notifications', 
            'preferred_language', 'created_by', 'vouchers'
        ]
        read_only_fields = ['created_by', 'email'] # mtlb ka yha sa jo user hy wo apni mrzi sa eidt kr skta hy ka kis na create kia hy


    def validate_vouchers(self, vouchers):
        user = self.context['request'].user
    # ya check kry gaka agr user na voucher bnaya hy ya nai
        for voucher in vouchers:
            if voucher.created_by != user:
                raise PermissionDenied(f"You do not have permission to assign voucher -name: '{voucher.name}'.")
        return vouchers