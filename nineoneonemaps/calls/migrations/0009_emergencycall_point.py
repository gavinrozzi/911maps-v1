# Generated by Django 2.1.8 on 2019-08-10 21:42

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0008_auto_20190507_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycall',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', geography=True, srid=4326),
        ),
    ]
