# Generated by Django 4.2.6 on 2023-11-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_is_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_social",
            field=models.BooleanField(default=False),
        ),
    ]
