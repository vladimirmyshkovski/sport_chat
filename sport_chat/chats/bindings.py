# polls/bindings.py

from channels_api.bindings import ResourceBinding

from .models import Team
from .serializers import TeamSerializer

class TeamBinding(ResourceBinding):

    model = Team
    stream = "teams"
    serializer_class = TeamSerializer
    queryset = Team.objects.all()