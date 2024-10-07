from django.urls import path
from . import views
from .views import MemberVouchersView

urlpatterns = [
    path('member/', views.MemberListCreateView.as_view(), name='member-list-create'),
    path('member/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('member/<int:member_id>/vouchers/', MemberVouchersView.as_view(), name='member-vouchers'),
]
