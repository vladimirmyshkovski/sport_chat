from channels.routing import route, include
from sport_chat.chats.consumers import chat_connect, chat_message, chat_disconnect, chat_message_consumer


chat_routing = [
    route("websocket.connect", chat_connect),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.receive", chat_message),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.disconnect", chat_disconnect),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("chat-messages", chat_message_consumer),
]


channel_routing = [
    include(chat_routing),
]
