from functools import wraps

from .exceptions import ClientError
from .models import Event as Room
#from .models import Room
from annoying.functions import get_object_or_None
from django.core.cache import cache
from rest_framework.authtoken.models import Token

def catch_client_error(func):
    """
    Decorator to catch the ClientError exception and translate it into a reply.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            # If we catch a client error, tell it to send an error string
            # back to the client on their reply channel
            e.send_to(message.reply_channel)
    return inner


def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated():
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check permissions
    #if room.staff_only and not user.is_staff:
    #    raise ClientError("ROOM_ACCESS_DENIED")
    return room


def check_token(message=None):
    token = None
    if message:
        path = message.content['path'].split("/")[-1]
        print(path)
        if path.split('='):
            if path.split('=')[0] == 'token':
                token = get_object_or_None(Token, key=path.split('=')[1])
                print(token)
    if not token:
        raise ClientError("USER_HAS_TO_LOGIN")
    else:
        set_user(token)
    return token


def get_user(message=None):
    user = None
    if message:
        try:
            print(message.content)
            path = message.content['path'].split("/")[0]
            if path.split('='):
                if path.split('=')[0] == 'token':
                    user = cache.get(path.split('=')[1])
        except:
            pass
        try:
            user = cache.get(message.content['token'])
        except:
            pass
    if not user:
        raise ClientError("USER_HAS_TO_LOGIN")
        
    return user

def set_user(token=None):
    if token:
        cache.set(token, token.user)
    return cache.get(token)
