from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer, EventDetailSerializer, EventStatusUpdateSerializer

class EventListView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.organizer == self.request.user or self.request.user.is_staff:
            return super().perform_destroy(instance)
        else:
            raise PermissionDenied("You do not have permission to delete this event.")
