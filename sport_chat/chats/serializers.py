from rest_framework import serializers, pagination
from .models import Message, Event, Team
from sport_chat.users.serializers import UserSerializer



class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ('id', 'name', 'flag', 'cropping')

class MessageSerializer(serializers.ModelSerializer):
	team = TeamSerializer()
	user = UserSerializer()

	class Meta:
		model = Message
		fields = ('id', 'msg_type', 'team', 'team_type', 'user', 'timestamp', 'human_timestamp', 'message')


class EventSerializer(serializers.ModelSerializer):
	#event_messages = MessageSerializer(many=True)
	#messages = serializers.SerializerMethodField('event_messages')
	messages = serializers.HyperlinkedIdentityField(view_name='api_v1:event_messages_list')
	home_team = TeamSerializer()
	away_team = TeamSerializer()
	in_room = serializers.SerializerMethodField('check_user')

	def check_user(self, obj):
		user = self.context['request'].user
		return user in obj.users.all()

	class Meta:
	    model = Event
	    fields = ('id', 'status', 'name', 'home_team', 'away_team', 'messages', 'data', 'in_room')

