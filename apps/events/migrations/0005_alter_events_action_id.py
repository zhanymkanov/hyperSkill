# Generated by Django 3.2 on 2021-04-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_events_action_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='action_id',
            field=models.IntegerField(choices=[(0, 'See'), (1, 'Submit'), (2, 'Solve')]),
        ),
    ]
