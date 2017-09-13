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
    Notification
)

class TeamCreateView(CreateView):

    model = Team
    fields = '__all__'


class TeamDeleteView(DeleteView):

    model = Team


class TeamDetailView(DetailView):

    model = Team


class TeamUpdateView(UpdateView):

    model = Team


class TeamListView(ListView):

    model = Team


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


