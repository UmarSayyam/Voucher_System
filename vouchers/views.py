from django.shortcuts import render
from rest_framework import generics
from .models import Voucher, VoucherAvailability, TimeSlot
from .serializers import VoucherSerializer, VoucherAvailabilitySerializer, TimeSlotSerializer, VoucherCreateSerializer
from rest_framework.response import Response
from rest_framework import status

class VoucherListCreateView(generics.ListCreateAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

class VoucherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Voucher deleted successfully"}, status=status.HTTP_200_OK)

class VoucherAvailabilityListCreateView(generics.ListCreateAPIView):
    queryset = VoucherAvailability.objects.all()
    serializer_class = VoucherAvailabilitySerializer

    def get_queryset(self):
        return VoucherAvailability.objects.filter(voucher_id=self.kwargs['voucher_id'])

    def perform_create(self, serializer):
        voucher = Voucher.objects.get(id=self.kwargs['voucher_id'])
        serializer.save(voucher=voucher)

class VoucherAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VoucherAvailability.objects.all()
    serializer_class = VoucherAvailabilitySerializer

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Voucher availability deleted successfully"}, status=status.HTTP_200_OK)




class TimeSlotListCreateView(generics.ListCreateAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.filter(voucher_availability_id=self.kwargs['voucher_availability_id'])

    def perform_create(self, serializer):
        voucher_availability = VoucherAvailability.objects.get(id=self.kwargs['voucher_availability_id'])
        serializer.save(voucher_availability=voucher_availability)


class TimeSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer




# make a new api (class)
# which will inherit both of above classes than add its url to urls.py


class VoucherNestedCreateView(generics.CreateAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherCreateSerializer