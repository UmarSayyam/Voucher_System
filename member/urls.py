from django.urls import path
from . import views

urlpatterns = [
    path('member/', views.MemberListCreateView.as_view(), name='member-list-create'),
    path('member/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
]
