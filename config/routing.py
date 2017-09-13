from channels.routing import route, include
from sport_chat.chats.consumers import chat_connect, chat_message, chat_disconnect
import json


chat_routing = [
    route("websocket.connect", chat_connect, ),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.receive", chat_message, ),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.disconnect", chat_disconnect, ),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
]


channel_routing = [
    include(chat_routing, path=r'^/chat/'),
]
