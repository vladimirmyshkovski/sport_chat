from .serializers import MessageSerializer, EventSerializer
from rest_framework import generics

from .models import (
    Team,
    Event,
    Notification,
    Message
)

class MessageApiView(generics.ListAPIView):
    queryset = Message.objects.all()

    serializer_class = MessageSerializer


class EventApiView(generics.ListAPIView):
    queryset = Event.objects.all()

    serializer_class = EventSerializer


class EventListApiView(generics.ListAPIView):
    queryset = Event.objects.all()    

    serializer_class = EventSerializer

class EventDetailApiView(generics.RetrieveAPIView):
    queryset = Event.objects.all()

    serializer_class = EventSerializer


class EventMessageListApiView(generics.ListAPIView):
    
    def get_queryset(self):
    	#queryset = super(EventMessageApiView, self).get_queryset()
    	return Message.objects.filter(event=self.kwargs['pk']).order_by('timestamp')

    serializer_class = MessageSerializer