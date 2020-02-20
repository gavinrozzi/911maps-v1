from calls.models import emergencycall
from django.contrib.gis.geos import Point
for l in emergencycall.objects.all():
    l.point = Point(x=l.lon, y=l.lat, srid=4326)
    l.save()
