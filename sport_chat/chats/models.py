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
	team_left = models.ForeignKey(
		Team,
		related_name = 'event_team_left',
		verbose_name = _('Left team'),
		)
	team_right = models.ForeignKey(
		Team,
		related_name = 'event_team_right',
		verbose_name = _('Right team'),
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

	def __str__(self):
		return self.name


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
	room = models.CharField(max_length=50)
	event = models.ForeignKey(
		Event
	)
	team = models.ForeignKey(
		Team,
		null=True,
	) 
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(db_index=True, default=timezone.now)
	content = models.TextField()

	def __str__(self):
		return '{0} at {1}'.format(self.user, self.timestamp)