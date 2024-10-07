from django.db import models
from django.conf import settings
from vouchers.models import Voucher

class Member(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    mobile_number = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()
    additional_phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    SOURCE_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('friend', 'Friend'),
        ('ads', 'Ads'),
        ('other', 'Other'),
    ]
    member_source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    address = models.TextField(max_length=250, null=False, blank=False)

# notifications
    receive_notifications = models.BooleanField(default=True)
    marketing_email_notifications = models.BooleanField(default=True)
    marketing_text_notifications = models.BooleanField(default=True)

    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('arabic', 'Arabic'),
        ('urdu', 'Urdu'),
        ('faarsi', 'Faarsi'),
        ('python', 'Python'),
    ]
    preferred_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='faarsi')

# to link this with useraccounts user app
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='member', on_delete=models.CASCADE)

 # so by this i can create many-to-many relatioships between apps(user and vouchers)
    vouchers = models.ManyToManyField('vouchers.Voucher', related_name='member', blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class MemberVoucherUsage(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0)  # Tracks how many times the voucher has been used by this member
    is_expired = models.BooleanField(default=False)  # To track if the voucher has expired for this member

    class Meta:
        unique_together = ('member', 'voucher')  # Ensures that a member can only have one usage record per voucher

    def __str__(self):
        return f"{self.member} - {self.voucher} - Usage: {self.usage_count}"