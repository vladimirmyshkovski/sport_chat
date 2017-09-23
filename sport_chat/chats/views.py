# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,
    RedirectView,
)

from .models import (
    Team,
    Event,
    Notification,
    Message
)

from django.db.models import Q


class TeamCreateView(CreateView):

    model = Team
    fields = '__all__'


class TeamDeleteView(DeleteView):

    model = Team


class TeamDetailView(DetailView):

    model = Team


class TeamChatDetailView(DetailView):

    model = Team
    template_name = 'chats/team_chat.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamChatDetailView, self).get_context_data(*args, **kwargs)
        event = Event.objects.exclude(
            Q(status='end'),
            Q(team_left=self.object) | Q(team_left=self.object)
        )
        context['chat_messages'] = Message.objects.filter(event=event)
        return context


class TeamUpdateView(UpdateView):

    model = Team


class TeamListView(ListView):

    model = Team

    def get_queryset(self):
        queryset = super(TeamListView).get_queryset()
        return queryset.exclude(status='end')

class EventCreateView(CreateView):

    model = Event
    fields = '__all__'


class EventDeleteView(DeleteView):

    model = Event


class EventDetailView(DetailView):

    model = Event


class EventUpdateView(UpdateView):

    model = Event


class EventListView(ListView):

    model = Event


class NotificationCreateView(CreateView):

    model = Notification
    fields = '__all__'


class NotificationDeleteView(DeleteView):

    model = Notification


class NotificationDetailView(DetailView):

    model = Notification


class NotificationUpdateView(UpdateView):

    model = Notification


class NotificationListView(ListView):

    model = Notification


