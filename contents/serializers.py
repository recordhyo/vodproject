from rest_framework import serializers
from .models import vodtest
class vodSerializer(serializers.ModelSerializer):

    class Meta:
        model = vodtest
        fields = '__all__'