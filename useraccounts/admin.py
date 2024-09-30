from django.contrib import admin
from .models import CustomUserModel

admin.site.site_header = 'Voucher System'

class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ("id","email","first_name", "last_name", 'company_name', 'phone_number')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'User Basic Information such as name, email, phone number.'}
        return super().changelist_view(request, extra_context=extra_context)
 
admin.site.register(CustomUserModel, CustomUserModelAdmin)

