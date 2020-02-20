from django.db import models
from django.contrib.gis.db import models
from autoslug import AutoSlugField

class agency(models.Model):
        name = models.CharField(max_length=50, default=None)
        slug = AutoSlugField(populate_from='name')

        def __str__(self):
            return self.name

class emergencycall(models.Model):
        id = models.PositiveIntegerField(primary_key=True)
        received = models.DateTimeField()
        sent = models.DateTimeField()
        priority = models.IntegerField(null=True)
        description = models.CharField(max_length=50)
        details = models.TextField()
        external_data = models.TextField(blank=True)
        place = models.CharField(max_length=50, blank=True)
        address = models.TextField()
        unit = models.TextField(blank=True)
        cross_street = models.TextField(blank=True)
        city = models.TextField(blank=True)
        state = models.TextField(blank=True)
        source = models.TextField(blank=True)
        units = models.CharField(max_length=25, blank=True)
        cad_code = models.CharField(max_length=25, blank=True)
        messages = models.TextField(blank=True)
        responses = models.TextField(blank=True)
        agency = models.ForeignKey(agency, default=None, on_delete=models.CASCADE)
        lat = models.FloatField()
        lon = models.FloatField()
        point = models.PointField(geography=True, default='POINT(0.0 0.0)')
     
        def __str__(self):
            return self.description
