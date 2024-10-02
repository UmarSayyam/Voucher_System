from django.db import models
from django.utils.translation import gettext as _

class Voucher(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage'),
    ]
# nothing can be null
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # can be null
    voucher_code = models.CharField(max_length=100, unique=True, null=False, blank=False)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False) 
    start_date = models.DateTimeField('Start Date', null=False, blank=False) #add time todo
    end_date = models.DateTimeField('End Date', null=False, blank=False) # #add time todo
    minimum_spending = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_usability_of_voucher = models.IntegerField(_("Maximum Usability of Voucher"), default=5)
    #Field(max_digits=10, decimal_places=2, null=False, blank=False) # max use count of a voucher
    birthday_members_only = models.BooleanField(default=False)
    # standalone_voucher = models.BooleanField(default=False)
    # apply_on_all_items = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class VoucherAvailability(models.Model):
    DAYS_OF_WEEK_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    voucher = models.ForeignKey(Voucher, related_name='availabilities', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES)


    # start_time = models.TimeField()
    
    # end_time = models.TimeField() # add multiple start and end time for a single day.
    

    def __str__(self):
        return f"{self.voucher.name} on {self.day_of_week} from {self.start_time} to {self.end_time}"


class TimeSlot(models.Model):
    voucher_availability = models.ForeignKey(VoucherAvailability, related_name='time_slots', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

