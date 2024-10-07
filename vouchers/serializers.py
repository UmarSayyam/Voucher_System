from rest_framework import serializers
from .models import Voucher, VoucherAvailability, TimeSlot
from member.models import Member

class VoucherSerializer(serializers.ModelSerializer):
    # member = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Member.objects.all(), required=False
    # )
    class Meta:
        model = Voucher
        fields = [
            'id', 
            'name', 'description', 'voucher_code', 'discount_type', 'discount_value',
            'start_date', 'end_date', 'minimum_spending', 'maximum_usability_of_voucher',
            'birthday_members_only', #'member', 
        ]

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time']



class VoucherAvailabilitySerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, required=False)

    class Meta:
        model = VoucherAvailability
        fields = ['id', 'day_of_week', 'time_slots']


class VoucherCreateSerializer(serializers.ModelSerializer):
    availabilities = VoucherAvailabilitySerializer(many=True)

    class Meta:
        model = Voucher
        fields = [
            'id',
            'name', 'description', 'voucher_code', 'discount_type', 'discount_value',
            'start_date', 'end_date', 'minimum_spending', 'maximum_usability_of_voucher',
            'birthday_members_only', 'availabilities'
        ]

    def create(self, validated_data):
        availabilities_data = validated_data.pop('availabilities')
        voucher = Voucher.objects.create(**validated_data)

        for availability_data in availabilities_data:
            time_slots_data = availability_data.pop('time_slots')
            availability = VoucherAvailability.objects.create(voucher=voucher, **availability_data)
            
            for time_slot_data in time_slots_data:
                TimeSlot.objects.create(voucher_availability=availability, **time_slot_data)

        return voucher

