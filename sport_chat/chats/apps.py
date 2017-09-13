from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'sport_chat.chats'
    verbose_name = "Chats"

    def ready(self):
    	pass
