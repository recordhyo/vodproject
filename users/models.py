from django.db import models

class Member(models.Model) :
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=128, null=False)
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=20, null=False)
    authenticated = models.BooleanField(default=False)
    profile_img = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    provider = models.TextField(max_length=10, default="None")
