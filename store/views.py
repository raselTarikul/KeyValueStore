from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Storage
from .serializers import StorageSerializer
import datetime


@api_view(['POST'])
def add_value(request):
    serializer = StorageSerializer(data=request.data)
    if serializer.is_valid():
        storage = serializer.save()
        storage.last_updated = datetime.datetime.now()
        storage.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def get_and_update_values(request, id):
    value = get_object_or_404(Storage, pk=id)
