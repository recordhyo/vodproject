# Generated by Django 4.2.6 on 2023-10-25 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=128)),
                ("password", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=20)),
                ("authenticated", models.BooleanField(default=False)),
                ("profile_img", models.ImageField(upload_to="")),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now_add=True)),
                ("provider", models.TextField(max_length=10)),
            ],
        ),
    ]
