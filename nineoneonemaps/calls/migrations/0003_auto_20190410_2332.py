# Generated by Django 2.1.7 on 2019-04-11 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_auto_20190402_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycall',
            name='priority',
            field=models.IntegerField(null=True),
        ),
    ]
