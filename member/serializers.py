from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'id', 'first_name', 'last_name', 'mobile_number', 'email', 'gender', 
            'date_of_birth', 'additional_phone_number', 'member_source', 'address', 
            'receive_notifications', 'marketing_email_notifications', 'marketing_text_notifications', 
            'preferred_language', 'created_by'
        ]
        read_only_fields = ['created_by'] # mtlb ka yha sa jo user hy wo apni mrzi sa eidt kr skta hy ka kis na create kia hy
