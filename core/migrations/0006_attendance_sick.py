# Generated by Django 4.1.7 on 2024-04-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_rename_recieved_by_notification_received_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="sick",
            field=models.BooleanField(default=False, verbose_name="Sick"),
        ),
    ]
