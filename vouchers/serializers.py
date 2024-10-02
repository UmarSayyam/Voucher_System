from rest_framework import serializers
from .models import Voucher, VoucherAvailability, TimeSlot

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherAvailability
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'voucher_availability']

