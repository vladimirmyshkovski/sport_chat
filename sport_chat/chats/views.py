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
from django.contrib.auth.mixins import LoginRequiredMixin


class TeamCreateView(LoginRequiredMixin, CreateView):

    model = Team
    fields = '__all__'


class TeamDeleteView(LoginRequiredMixin, DeleteView):

    model = Team


class TeamDetailView(LoginRequiredMixin, DetailView):

    model = Team


class TeamChatDetailView(LoginRequiredMixin, DetailView):

    model = Team
    template_name = 'chats/team_chat.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamChatDetailView, self).get_context_data(*args, **kwargs)
        event = Event.objects.exclude(
            Q(status='end'),
            Q(team_left=self.object) | Q(team_right=self.object)
        )
        #print(event)
        if event:
            context['event'] = event[0].pk
        context['chat_messages'] = Message.objects.filter(event=event)
        return context


class TeamUpdateView(LoginRequiredMixin, UpdateView):

    model = Team


class TeamListView(LoginRequiredMixin, ListView):

    model = Team


class EventCreateView(LoginRequiredMixin, CreateView):

    model = Event
    fields = '__all__'


class EventDeleteView(LoginRequiredMixin, DeleteView):

    model = Event


class EventDetailView(LoginRequiredMixin, DetailView):

    model = Event


class EventUpdateView(LoginRequiredMixin, UpdateView):

    model = Event


class EventListView(LoginRequiredMixin, ListView):

    model = Event

    def get_queryset(self):
        queryset = super(EventListView).get_queryset()
        return queryset.exclude(status='end')


class NotificationCreateView(LoginRequiredMixin, CreateView):

    model = Notification
    fields = '__all__'


class NotificationDeleteView(LoginRequiredMixin, DeleteView):

    model = Notification


class NotificationDetailView(LoginRequiredMixin, DetailView):

    model = Notification


class NotificationUpdateView(LoginRequiredMixin, UpdateView):

    model = Notification


class NotificationListView(LoginRequiredMixin, ListView):

    model = Notification


