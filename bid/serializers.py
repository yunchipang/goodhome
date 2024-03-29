from rest_framework import serializers
from rest_framework.views import APIView
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
