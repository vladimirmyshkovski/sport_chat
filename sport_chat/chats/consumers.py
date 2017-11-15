# In consumers.py
from channels import Group, Channel
import ujson as json
from channels.sessions import channel_session
from urllib.parse import parse_qs
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import allowed_hosts_only
from .models import Message, Event as Room, Team
from sport_chat.users.models import User
from django.db.models import Q
from django.utils import timezone
from .utils import get_room_or_error, catch_client_error
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .exceptions import ClientError
from .auth_token import rest_token_user
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from .utils import check_token, get_user, set_user

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
	if event.team_left == team:
		room2 = event.team_right.pk
	else:
		room2 = event.team_left.pk
	
	Group('chat-%s' % room2).send({
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
	print('chat_connect')
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
	#print(message.content['path'])
	Group('chat-%s' % message.channel_session['room']).discard(message.reply_channel)



'''
@channel_session_user_from_http
def notification_connect(message):
	print('notification_connect')
	room = message.content['path'].split("/")[-1]
	print('ROOM IS' + str(room))
	message.channel_session['room'] = room
	Group('notification-%s' % room).add(message.reply_channel)
	message.reply_channel.send({"accept": True})


@channel_session_user
def notification_message(message):
	print('notification_message')
	room = message.channel_session['room']
	#Group('notification-%s' %  room).send({
	#	"room": room,
	#	"message": message['text'],
	#})	


@channel_session_user
def notification_disconnect(message):
	print('notification_disconnect')
	room = message.channel_session['room']
	Group('notification-%s' % room).discard(message.reply_channel)
'''


def widget_chat_message_consumer(message):
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
	if event.team_left == team:
		room2 = event.team_right.pk
	else:
		room2 = event.team_left.pk
	
	Group('widget-chat-%s' % room2).send({
		"text": json.dumps({
			"message": message.content['message'],
			"username": username,
			"team": team.name,
			"room": room,
		}),
	})


#@channel_session_user_from_http
#@rest_token_user
def widget_chat_connect(message):
	token = check_token(message)
	if token:
		message.reply_channel.send({'accept': True})
		rooms = Room.objects.exclude(status='end')
		message.user = token.user
		for room in rooms:
			if message.user in room.users.all():
				room.websocket_group.add(message.reply_channel)
				cache.set('chat_rooms', [room.id for room in rooms])
				set_user(token)
				#cache.set(token, token.user)
	#message.channel_session['rooms'] = [room.id for room in rooms]
	'''
	print(room_name)
	print(message.content)
	room = 1 #message.content['path'].split("/")[-1]
	message.channel_session['room'] = room
	Group('widget-chat-%s' % room).add(message.reply_channel)
	message.reply_channel.send({"accept": True})
	'''


#@channel_session_user
def widget_chat_message(message):
	'''
	Channel('widget-chat-messages').send({
		"room": message.channel_session['room'],
		"message": message['text'],
		"username": message.user.username,
	})
	'''
	payload = json.loads(message['text'])
	payload['reply_channel'] = message.content['reply_channel']
	Channel("chat.receive").send(payload)


#@channel_session_user
def widget_chat_disconnect(message):
	# Unsubscribe from any connected rooms
	message.user = get_user(message)
	if(cache.get('chat_rooms')):
		for room_id in cache.get('chat_rooms'):#message.channel_session.get("rooms", set()):
		    try:
		        room = Room.objects.get(pk=room_id)
		        # Removes us from the room's send group. If this doesn't get run,
		        # we'll get removed once our first reply message expires.
		        room.websocket_group.discard(message.reply_channel)
		    except Room.DoesNotExist:
		        pass


#@channel_session_user
@catch_client_error
def chat_join(message):
	# Find the room they requested (by ID) and add ourselves to the send group
	# Note that, because of channel_session_user, we have a message.user
	# object that works just like request.user would. Security!
	message.user = get_user(message)
	room = get_room_or_error(message["room_id"], message.user)
	team_id = message['team_id']
	team_name = message['team_name']
	team_align = message['team_align']
	team_name = message['team_name']
	
	# Send a "enter message" to the room if available
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
	    room.send_message(None, message.user, team_id, team_align, team_name, MSG_TYPE_ENTER)

	# OK, add them in. The websocket_group is what we'll send messages
	# to so that everyone in the chat room gets them.
	room.websocket_group.add(message.reply_channel)
	#message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
	# Send a message back that will prompt them to open the room
	# Done server-side so that we could, for example, make people
	# join rooms automatically.

	room.add_to_room(message.user, team_id, team_name, team_align)

	message.reply_channel.send({
	    "text": json.dumps({
	        "join": str(room.id),
	        "room_name": room.name,
	        "team_id": team_id,
	        "team_name": team_name,
	        "timestamp": timezone.now().strftime('%I:%M:%S %p')
	    }),
	})


#@channel_session_user
@catch_client_error
def chat_leave(message):
	# Reverse of join - remove them from everything.
	message.user = get_user(message)
	room = get_room_or_error(message["room"], message.user)
	team_id = message['team_id']
	team_name = message['team_name']
	team_align = message['team_align']
	team_name = message['team_name']

	# Send a "leave message" to the room if available
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
	    room.send_message(None, message.user, team_id, team_align, team_name, MSG_TYPE_LEAVE)

	room.websocket_group.discard(message.reply_channel)
	#message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
	# Send a message back that will prompt them to close the room

	room.leave_from_room(message.user, team_name, team_align)

	message.reply_channel.send({
	    "text": json.dumps({
	        "leave": str(room.id),
	    }),
	})


#@channel_session_user
@catch_client_error
def chat_send(message):
	message.user = get_user(message)
	# Check that the user in the room
	if int(message['room']) not in cache.get('chat_rooms'):#message.channel_session['rooms']:
	    raise ClientError("ROOM_ACCESS_DENIED")
	# Find the room they're sending to, check perms
	room = get_room_or_error(message["room"], message.user)
	team_id = message['team_id']
	team_name = message['team_name']
	team_align = message['team_align']
	team_name = message['team_name']
	# Send the message along
	room.send_message(message["message"], message.user, team_id, team_align, team_name)
