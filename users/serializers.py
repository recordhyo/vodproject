from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Member
        fields = ['id', 'email', 'password', 'name', 'authenticated', 'profile_img',
                  'created_at', 'updated_at', 'provider']