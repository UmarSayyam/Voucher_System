from django.urls import path
from . import views

urlpatterns = [
    #voucher ka liye
    path('vouchers/', views.VoucherListCreateView.as_view(), name='voucher-list'),
    path('vouchers/<int:pk>/', views.VoucherDetailView.as_view(), name='voucher-detail'),
    #avalability voucher ka liye
    path('vouchers/<int:voucher_id>/availabilities/', views.VoucherAvailabilityListCreateView.as_view(), name='voucher-availability-list'),
    path('availabilities/<int:pk>/', views.VoucherAvailabilityDetailView.as_view(), name='voucher-availability-detail'),
    #timeslot ka liye
    path('voucher-availabilities/<int:voucher_availability_id>/time-slots/', views.TimeSlotListCreateView.as_view(), name='time-slot-list-create'),
    path('time-slots/<int:pk>/', views.TimeSlotDetailView.as_view(), name='time-slot-detail'),
    #for all in one
    path('voucher/create-nested/', views.VoucherNestedCreateView.as_view(), name='voucher-nested-create'),
]
