import ujson as json
from .models import Event, Notification
from celery import shared_task
#from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from annoying.functions import get_object_or_None


def send_notification(notification_pk, event_pk, message):
	event = get_object_or_None(Event, pk=event_pk)
	notification = get_object_or_None(Notification, pk=notification_pk)
	if event:
		if event.status == 'end':
			task = get_object_or_None(
				PeriodicTask, 
				name='sending event notification #{} to event #{}'.format(
					notification_pk,
					event_pk
					)
				)
			task.delete()
		else:
			pass
			#send_notification

@shared_task
def change_status(event_pk):
	
	event = get_object_or_None(Event, pk=event_pk)
	if event:
		
		if event.status == 'soon':
			event.status = 'online'
		
		elif event.status == 'online':
			event.status = 'end'

		event.save()


@receiver(post_save, sender=Event)
def change_event_status(sender, instance, created, **kwargs):
	
	if created:
		if instance.status == 'soon':
			countdown = instance.start_date - instance.created
		elif instance.status == 'online':
			countdown = instance.end_date - instance.start_date 
		change_status.apply_async(args=(instance.pk, ), countdown=countdown.seconds)


@receiver(post_save, sender=Notification)
def schedule_task(sender, instance, created, **kwargs):
	if created:
		every = instance.every

		schedule, created = IntervalSchedule.objects.get_or_create(
			every=every,
			period=IntervalSchedule.MINUTES,
			)

		PeriodicTask.objects.create(
			interval=schedule,
			name='sending event notification #{} to event #{}'.format(
				instance.pk, 
				instance.event.pk
				),
			task='chats.tasks.send_notification',
				args=json.dumps([
					instance.pk,
					instance.event.pk,
					instance.mesage
					]),
				kwargs=json.dumps({
					'be_careful': True,
					}),
				expires=None,
				)