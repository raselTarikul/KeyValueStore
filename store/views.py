from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Storage
from .serializers import StorageSerializer
import datetime
from django.db.models import Q


@api_view(['POST', 'GET'])
def add_value(request):
    if request.method == 'POST':
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            storage = serializer.save()
            storage.last_updated = datetime.datetime.now()
            storage.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes = int(storage.ttl))
            storage.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET' and not request.GET.get('key', None):
        # remove expaired object
        Storage.objects.filter(expiration_time__lt=datetime.datetime.now()).delete()
        #Get obejcts
        values = Storage.objects.filter(expiration_time__gt=datetime.datetime.now())
        response_data = dict()
        for value in values:
            response_data[value.key] = value.value
            value.last_updated = datetime.datetime.now()
            value.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=int(value.ttl))
            value.save()
        return Response(response_data)
    elif request.method == 'GET' and request.GET.get('key', None):
        # remove expaired object
        Storage.objects.filter(expiration_time__lt=datetime.datetime.now()).delete()
        # Get obejcts
        keys = request.GET.get('key').split(',')
        values = Storage.objects.filter(Q(expiration_time__gt=datetime.datetime.now()) & Q(key__in=keys))
        response_data = dict()
        for value in values:
            response_data[value.key] = value.value
            value.last_updated = datetime.datetime.now()
            value.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=int(value.ttl))
            value.save()
        return Response(response_data)


@api_view(['GET', 'PATCH'])
def get_and_update_values(request, key):
    value = get_object_or_404(Storage, key=key)

    if request.method == 'PATCH':
        serializer = StorageSerializer(instance=value, data=request.data)
        if serializer.is_valid():
            inatance = serializer.save()
            inatance.last_updated = datetime.datetime.now()
            inatance.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=int(value.ttl))
            inatance.save()
            response_data = dict()
            response_data[inatance.key] = inatance.value
            return Response(response_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # remove expaired object
        Storage.objects.filter(expiration_time__lt=datetime.datetime.now()).delete()
        response_data = dict()
        response_data[value.key] = value.value
        return Response(response_data)

