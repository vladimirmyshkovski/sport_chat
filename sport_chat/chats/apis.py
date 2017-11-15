from .serializers import MessageSerializer, EventSerializer, TokenSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token

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
    	return Message.objects.filter(event=self.kwargs['pk']).order_by('timestamp')

    serializer_class = MessageSerializer


class TokenDetailApiView(generics.RetrieveAPIView):
    lookup_field = 'key'

    def get_queryset(self):
        print('KEY IS: ' + str(Token.objects.get(key=self.kwargs['key'])))
        return Token.objects.all()
    
    serializer_class = TokenSerializer