from rest_framework import serializers
from .models import Storage


class StorageSerializer(serializers.ModelSerializer):
    """
    Serializer Class to serializer object into Json
    """
    class Meta:
        model = Storage
        fields = ['key', 'value', 'ttl']
