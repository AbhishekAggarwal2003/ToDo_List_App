# Generated by Django 5.1.4 on 2025-01-06 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0003_todo_timer_duration_todo_timer_started_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='timer_started_at',
            new_name='deadline',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='timer_duration',
        ),
    ]
