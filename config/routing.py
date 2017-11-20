from channels.routing import route, include
from sport_chat.chats.consumers import chat_connect, chat_message, chat_disconnect, chat_message_consumer, \
										widget_chat_connect, widget_chat_message, widget_chat_disconnect, widget_chat_message_consumer, \
										chat_join, chat_leave, chat_send
										#notification_connect, notification_message, notification_disconnect

chat_routing = [
    route("websocket.connect", chat_connect),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.receive", chat_message),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("websocket.disconnect", chat_disconnect),# path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/(?P<team>[a-zA-Z0-9_]+)/$"),#path=r'^/(?P<username_from>[a-zA-Z0-9_]+)/(?P<username_to>[a-zA-Z0-9_]+)/$'),
    route("chat-messages", chat_message_consumer),
]

widget_chat_routing = [
	route("websocket.connect", widget_chat_connect),
	route("websocket.receive", widget_chat_message),
	route("websocket.disconnect", widget_chat_disconnect),
	route("widget-chat-messages", widget_chat_message_consumer),
]

custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_leave, command="^leave$"),
    route("chat.receive", chat_send, command="^send$"),
]

#notification_routing = [
#	route("notification_connect.connect", notification_connect),
#	route("notification_message.receive", notification_message),
#	route("notification_disconnect.disconnect", notification_disconnect),
#]




from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class

from sport_chat.chats.bindings import TeamBinding

class APIDemultiplexer(WebsocketDemultiplexer):

    consumers = {
      'teams': TeamBinding.consumer
    }

channel_routing = [
    #include(chat_routing),
    #include(widget_chat_routing),
    #include(custom_routing),
    #include(notification_routing),
    route_class(APIDemultiplexer)

]
