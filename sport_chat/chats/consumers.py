# In consumers.py
from channels import Group
import ujson as json
from channels.sessions import channel_session
from urllib.parse import parse_qs
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import allowed_hosts_only


# Connected to websocket.connect
#@allowed_hosts_only
#@channel_session_user_from_http
def chat_connect(message):
	message.reply_channel.send({"accept": True})
	Group('chat').add(message.reply_channel)


# Connected to websocket.receive
#@allowed_hosts_only
#@channel_session_user
def chat_message(message):
	print(message['text'])
	#room = Room.objects.fileter()
	Group('chat').send({
		'text': json.dumps({
			'text': message['text'],
			#'username': message.channel_session["username"],
		}),
	})


# Connected to websocket.disconnect
#@allowed_hosts_only
#@channel_session_user
def chat_disconnect(message):
    Group('chat').discard(message.reply_channel)
