from rest_framework import routers, serializers, viewsets
from .models import emergencycall

class EmergencycallSerializer(serializers.ModelSerializer):
   class Meta:
       model = emergencycall
       fields = ('id', 'received', 'priority', 'details', 'description', 'place', 'address', 'unit', 'city', 'state', 'lat', 'lon', 'units')

class EmergencycallViewSet(viewsets.ModelViewSet):
    queryset = emergencycall.objects.all()
    serializer_class = EmergencycallSerializer

router = routers.SimpleRouter()
router.register('api-calls', EmergencycallViewSet)