from django.contrib import admin
from .models import Member

# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_number', 'created_by')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_number')
    list_filter = ('preferred_language', 'member_source', 'created_by')