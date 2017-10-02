import os
from channels.asgi import get_channel_layer

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app_path = os.path.dirname(os.path.abspath(__file__)).replace('/config', '')
sys.path.append(os.path.join(app_path, 'sport_chat'))

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


channel_layer = get_channel_layer()

