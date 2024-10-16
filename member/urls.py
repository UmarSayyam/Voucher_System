from django.urls import path
from . import views
from .views import MemberVouchersView
from .views import UseVoucherView
from .views import voucher_notification

urlpatterns = [
    path('member/', views.MemberListCreateView.as_view(), name='member-list-create'),
    path('member/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('member/<int:member_id>/vouchers/', MemberVouchersView.as_view(), name='member-vouchers'),
    path('use-voucher/', UseVoucherView.as_view(), name='use-voucher'),
    path('voucher-notification/', voucher_notification, name='voucher_notification'),
]
