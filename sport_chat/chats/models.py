from django.db import models
from django.conf import settings
from django.utils import timezone
from image_cropping import ImageRatioField
from django.core.urlresolvers import reverse
from model_utils import Choices, FieldTracker
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import StatusField, MonitorField
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel, SoftDeletableModel
from channels import Group

from .settings import MSG_TYPE_MESSAGE, MESSAGE_TYPES_CHOICES
import ujson as json
from .signals import create_message

from django.core.exceptions import ValidationError
from django.db.models import Q

from django.contrib.postgres.fields import JSONField


def team_flag_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/team_<name>/<filename>
    return 'team_{0}/{1}'.format(instance.name, filename)


@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
	
	tracker = FieldTracker()

	class Meta:
		abstract = True


@python_2_unicode_compatible
class Team(Base):

	name = models.CharField(
		max_length=55,
		verbose_name = _('Name of team'),
		)
	flag = models.ImageField(upload_to=team_flag_directory_path)
	cropping = ImageRatioField('flag', '430x360')


	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Event(Base):

	STATUS = Choices(
		('soon', 'soon', _('Soon')), 
		('online', 'online', _('Online')),
		('end', 'end', _('End'))
	)

	status = models.CharField(
		choices=STATUS, 
		default=STATUS.soon,
		max_length=20
	)
	name = models.CharField(
		max_length=55,
		verbose_name = _('Name of event'),
		)
	home_team = models.ForeignKey(
		Team,
		related_name = 'event_home_team',
		verbose_name = _('Left team'),
		null=True,
		blank=False
		)
	away_team = models.ForeignKey(
		Team,
		related_name = 'event_away_team',
		verbose_name = _('Right team'),
		null=True,
		blank=False
		)
	start_date = models.DateTimeField(
		verbose_name = _('Start date and time'),
		help_text = _('Date and time when the event should start')
		)
	end_date = models.DateTimeField(
		verbose_name = _('End date and time'),
		help_text = _('Date and time when the event should end')
		)

	started_at = MonitorField(
		monitor='status', 
		when=['online']
	)
	ended_at = MonitorField(
		monitor='status', 
		when=['end']
	)
	users = models.ManyToManyField(
		settings.AUTH_USER_MODEL, 
		blank=False
	)
	data = JSONField(
		default={},
		null=True, 
		blank=False
	)

	def __str__(self):
		return self.name

	def clean(self):
		event = Event.objects.exclude(
			Q(status='end'),
		).filter(
			Q(home_team=self.home_team, away_team=self.away_team) | 
			Q(home_team=self.away_team, away_team=self.home_team) |
			Q(home_team=self.home_team) | Q(home_team=self.away_team) |
			Q(away_team=self.home_team) | Q(away_team=self.away_team)
		).exists()
		if event:
			raise ValidationError(_('You must end the event with these commands before you start a new one.'))

		if self.home_team == self.away_team:
			raise ValidationError(_('You must end the event with these commands before you start a new one.'))


		if self.start_date > self.end_date:
			raise ValidationError(_('Start date can not be longer than end date.'))


	@property
	def websocket_group(self):
	    """
	    Returns the Channels Group that sockets should subscribe to to get sent
	    messages as they are generated.
	    """
	    return Group("room-%s" % self.id)

	def add_to_room(self, user, team_id, team_name, team_align):
		if not user in self.users.all():
			self.users.add(user)
			self.data[user.username] = {'team_id': team_id, 'team_name': team_name, 'team_align': team_align}
			self.save()

	def leave_from_room(self, user, team_name, team_align):
		if user in self.users.all():
			self.users.delete(user)
			del self.data[user.username]
			self.save()

	def send_message(self, message, user, team_id=None, team_align=None, team_name=None, msg_type=MSG_TYPE_MESSAGE):
		"""
		Called to send a message to the room on behalf of a user.
		"""
		final_msg = {
			'room_id': str(self.id), 'message': message, 'username': user.username, 'team_id': team_id, 
			'team_name': team_name, 'msg_type': msg_type, "timestamp": timezone.now().strftime('%I:%M:%S %p'),
			'team_align': team_align
		}
		
		# Send signal for create new message
		create_message.send(
			sender=self.__class__, user=user, team=team_id, event=self.id, 
			message=message, msg_type=msg_type, team_type=team_align
			)

		# Send out the message to everyone in the room
		self.websocket_group.send(
		    {"text": json.dumps(final_msg)}
		)


@python_2_unicode_compatible
class Notification(Base):

	event = models.ForeignKey(
		Event
	)
	message = models.CharField(
		max_length=255
	)
	every = models.PositiveSmallIntegerField(
		default=0,
		verbose_name = _('Every'),
		help_text = _('The message will be sent each N number of minutes')
		)

	def __str__(self):
		return '{}'.format(self.pk)


@python_2_unicode_compatible
class Message(Base):

	TEAM_TYPES = Choices(
		('home', 'home', _('Home')), 
		('away', 'away', _('Away')),
	)
	event = models.ForeignKey(
		Event,
		related_name='event_messages'
	)
	team = models.ForeignKey(
		Team,
		related_name='team_messages',
		null=True,
	)
	msg_type = models.PositiveSmallIntegerField(
		choices=MESSAGE_TYPES_CHOICES,
		default=MESSAGE_TYPES_CHOICES[0][0],
	)
	team_type = models.CharField(
		choices=TEAM_TYPES, 
		default=TEAM_TYPES.home,
		max_length=4
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(db_index=True, default=timezone.now)
	message = models.TextField()

	@property
	def human_timestamp(self):
		return self.timestamp.strftime('%I:%M:%S %p')

	def __str__(self):
		return '{0} at {1}'.format(self.user, self.timestamp)

