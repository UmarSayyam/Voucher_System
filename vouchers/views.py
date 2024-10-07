from rest_framework import generics
from .models import Voucher, VoucherAvailability, TimeSlot
from .serializers import VoucherSerializer, VoucherAvailabilitySerializer, TimeSlotSerializer, VoucherCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class VoucherListCreateView(generics.ListCreateAPIView):
    serializer_class = VoucherSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return Voucher.objects.all()
        return Voucher.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class VoucherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Voucher.objects.all()
        return Voucher.objects.filter(created_by=self.request.user)

class VoucherAvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = VoucherAvailabilitySerializer

    def get_queryset(self):
        voucher = Voucher.objects.get(id=self.kwargs['voucher_id'])
        if voucher.created_by != self.request.user:
            raise PermissionDenied("apka pas is voucher ko dekhny ki shakian nahi hy.")
        return VoucherAvailability.objects.filter(voucher=voucher)

    def perform_create(self, serializer):
        voucher = Voucher.objects.get(id=self.kwargs['voucher_id'])
        if voucher.created_by != self.request.user:
            raise PermissionDenied("apky pas is voucehr ki availabilities ko cherny ki taaqat nai ay.")
        serializer.save(voucher=voucher)


class VoucherAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VoucherAvailabilitySerializer

    def get_queryset(self):
        return VoucherAvailability.objects.filter(voucher__created_by=self.request.user)

    def perform_update(self, serializer):
        availability = self.get_object()
        if availability.voucher.created_by != self.request.user:
            raise PermissionDenied("apky pas is voucher ki update availability ka haqq nai ay.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.voucher.created_by != self.request.user:
            raise PermissionDenied("bhai tu is voucher ki availability ko delete krny ka salahiyat nai ay :).")
        instance.delete()

class TimeSlotListCreateView(generics.ListCreateAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        availability = VoucherAvailability.objects.get(id=self.kwargs['voucher_availability_id'])
        if availability.voucher.created_by != self.request.user:
            raise PermissionDenied("bhai nai kr skty ap time add jaan choro.")
        return TimeSlot.objects.filter(voucher_availability=availability)

    def perform_create(self, serializer):
        availability = VoucherAvailability.objects.get(id=self.kwargs['voucher_availability_id'])
        if availability.voucher.created_by != self.request.user:
            raise PermissionDenied("ap timeslot bhi add nai kr skty.")
        serializer.save(voucher_availability=availability)

class TimeSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()

    def perform_update(self, serializer):
        time_slot = self.get_object()
        if time_slot.voucher_availability.voucher.created_by != self.request.user:
            raise PermissionDenied("ap slot update nai kr skty.")
        serializer.save()
    def perform_destroy(self, instance):
        if instance.voucher_availability.voucher.created_by != self.request.user:
            raise PermissionDenied("ap timeslot delete krna ki salahiayat nahi rkty maazrat bbhai jaan.")
        instance.delete()

class VoucherNestedCreateView(generics.CreateAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherCreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# funtion base / class base
# member voucher apply