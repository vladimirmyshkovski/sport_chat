from django.contrib import admin
from .models import Event, Team, Notification
from image_cropping import ImageCroppingMixin


class TeamAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
	exclude = ['started_at' ,'ended_at']


admin.site.register(Event, EventAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Notification)