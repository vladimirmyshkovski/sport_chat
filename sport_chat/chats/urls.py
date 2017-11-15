# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from . import apis

urlpatterns = [

    url(
        regex="^event/~create/$",
        view=views.EventCreateView.as_view(),
        name='event_create',
    ),
    url(
        regex="^event/(?P<pk>\d+)/~delete/$",
        view=views.EventDeleteView.as_view(),
        name='event_delete',
    ),
    url(
        regex="^event/(?P<pk>\d+)/$",
        view=views.EventDetailView.as_view(),
        name='event_detail',
    ),
    url(
        regex="^event/(?P<pk>\d+)/~update/$",
        view=views.EventUpdateView.as_view(),
        name='event_update',
    ),
    url(
        regex="^event/$",
        view=views.EventListView.as_view(),
        name='event_list',
    ),

    url(
        regex="^team/~create/$",
        view=views.TeamCreateView.as_view(),
        name='team_create',
    ),
    url(
        regex="^team/(?P<pk>\d+)/~delete/$",
        view=views.TeamDeleteView.as_view(),
        name='team_delete',
    ),
    url(
        regex="^team/(?P<pk>\d+)/$",
        view=views.TeamDetailView.as_view(),
        name='team_detail',
    ),
    url(
        regex="^team_chat/(?P<pk>\d+)/$",
        view=views.TeamChatDetailView.as_view(),
        name='team_chat_detail',
    ),
    url(
        regex="^team/(?P<pk>\d+)/~update/$",
        view=views.TeamUpdateView.as_view(),
        name='team_update',
    ),
    url(
        regex="^team/$",
        view=views.TeamListView.as_view(),
        name='team_list',
    ),

    url(
        regex="^notification/~create/$",
        view=views.NotificationCreateView.as_view(),
        name='notification_create',
    ),
    url(
        regex="^notification/(?P<pk>\d+)/~delete/$",
        view=views.NotificationDeleteView.as_view(),
        name='notification_delete',
    ),
    url(
        regex="^notification/(?P<pk>\d+)/$",
        view=views.NotificationDetailView.as_view(),
        name='notification_detail',
    ),
    url(
        regex="^notification/(?P<pk>\d+)/~update/$",
        view=views.NotificationUpdateView.as_view(),
        name='notification_update',
    ),
    url(
        regex="^notification/$",
        view=views.NotificationListView.as_view(),
        name='notification_list',
    ),

]

from sport_chat.users.views import token_auth


api_urlpatterns = [
    url(
        regex="^events/$",
        view=apis.EventListApiView.as_view(),
        name='event_list',
    ),
    url(
        regex="^events/(?P<pk>\d+)/$",
        view=apis.EventDetailApiView.as_view(),
        name='event_detail',
    ),
    url(
        regex="^events/(?P<pk>\d+)/messages/$",
        view=apis.EventMessageListApiView.as_view(),
        name='event_messages_list',
    ),
    url(
        regex = "^token/(?P<key>[^/]+)/$", 
        view = apis.TokenDetailApiView.as_view(), 
        name = "token_detail",
    ),
]
