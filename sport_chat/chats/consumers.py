# In consumers.py
from channels import Group, Channel
import ujson as json
from channels.sessions import channel_session
from urllib.parse import parse_qs
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import allowed_hosts_only
from .models import Message, Event, Team
from sport_chat.users.models import User
from django.db.models import Q
from django.utils import timezone


def chat_message_consumer(message):
	room = message.content['room']
	username = message.content['username']
	user = User.objects.get(username=username)
	team = Team.objects.get(pk=room)
	event = Event.objects.exclude(
		Q(status='end'),
		Q(team_left=team) | Q(team_left=team))
	if event.count() > 0:
		event = event[0]
	Message.objects.create(
		user=user,
		event=event,
		team=team,
		room=room,
		content=message.content['message'],
		timestamp=timezone.now(),
	)
	Group('chat-%s' % room).send({
		"text": json.dumps({
			"message": message.content['message'],
			"username": username,
			"team": team.name,
			"room": room,
			}),
	})

#@channel_session
@channel_session_user_from_http
def chat_connect(message):
	room = message.content['path'].split("/")[-1]
	message.channel_session['room'] = room
	Group('chat-%s' % room).add(message.reply_channel)
	message.reply_channel.send({"accept": True})


#@channel_session
#@channel_session_user_from_http
@channel_session_user
def chat_message(message):
	Channel('chat-messages').send({
		"room": message.channel_session['room'],
		"message": message['text'],
		"username": message.user.username,
	})	


#@channel_session
#@channel_session_user_from_http
@channel_session_user
def chat_disconnect(message):
	print(message.content['path'])
	Group('chat-%s' % message.channel_session['room']).discard(message.reply_channel)
