# Generated by Django 5.2 on 2025-04-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="age",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]
