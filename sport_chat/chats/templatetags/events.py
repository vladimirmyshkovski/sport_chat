import datetime
from django import template
from ..models import Event

register = template.Library()

'''
@register.inclusion_tag('chats/templatetags/event_list.html')
def my_custom_tag():
    things = MyModel.objects.all()
    return {'things' : things}
'''

#@register.assignment_tag()
@register.inclusion_tag('chats/templatetags/event_list.html')
def event_list():
	return {"events" : Event.objects.exclude(status='end')}
