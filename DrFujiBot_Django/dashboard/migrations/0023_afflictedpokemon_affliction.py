# Generated by Django 2.2.5 on 2020-01-03 16:04

from dashboard.models import Affliction
from django.db import migrations, models
import django.db.models.deletion
import json
import os

def import_afflictions(apps, schema_editor):
    json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'afflictions.json')

    with open(json_path) as json_file:
        affliction_data = json.load(json_file)
        affliction_objects = []

        for name in affliction_data.keys():
            affliction_object = Affliction(name=name, description=affliction_data[name])
            affliction_objects.append(affliction_object)

        Affliction.objects.bulk_create(affliction_objects)

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_stats_commands'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affliction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='AfflictedPokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=200)),
                ('affliction_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affliction_1', to='dashboard.Affliction')),
                ('affliction_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affliction_2', to='dashboard.Affliction')),
            ],
            options={
                'verbose_name_plural': 'Afflicted Pokemon',
            },
        ),
        migrations.RunPython(import_afflictions),
    ]
