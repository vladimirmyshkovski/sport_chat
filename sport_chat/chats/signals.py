import django.dispatch

create_message = django.dispatch.Signal(providing_args=["event", "team", "msg_type", "team_type", "user", "message"])