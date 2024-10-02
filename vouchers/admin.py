from django.contrib import admin
from .models import Voucher, VoucherAvailability, TimeSlot

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['name', 'voucher_code', 'discount_type', 'start_date', 'end_date']
    #  'standalone_voucher'

@admin.register(VoucherAvailability)
class VoucherAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'day_of_week']

@admin.register(TimeSlot)
class TimeSlot(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']