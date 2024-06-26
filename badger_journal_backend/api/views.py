from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

from .models import Entry
from .serializers import UserSerializer, EntrySerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Create a new user
    """
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        # check if user already exists before trying to create
        if (User.objects.filter(username=data['username'])):
            return JsonResponse({
                'status': status.HTTP_409_CONFLICT,
                'error': 'User already exists.'
            })
        serializer.save()
        return JsonResponse({
            'data':'User created.',
            'status':status.HTTP_201_CREATED
        })
    else:
        return JsonResponse({
            'status': status.HTTP_400_BAD_REQUEST,
            'error': 'Invalid request'
        })

@api_view(['GET', 'POST'])
def entry_list(request):
    """
    Return all entries or create an entry
    """
    user = request.user
    if request.method == 'GET':
        entries = Entry.objects.filter(user=user)

        serializer = EntrySerializer(entries, many=True)

        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['user'] = user.username
        serializer = EntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse({
                'data':data,
                'status':status.HTTP_201_CREATED
            }) 
    else:
        return JsonResponse({
            'status': status.HTTP_400_BAD_REQUEST,
            'error': 'Invalid request'
        })

@api_view(['GET', 'PUT', 'DELETE'])
def entry_detail(request, pk):
    """
    Return a single entry, update an entry or delete an entry
    """
    user = request.user
    try:
        entry = Entry.objects.get(pk = pk)
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': status.HTTP_404_NOT_FOUND,
            'error': f'Entry with id {pk} not found.'
        })

    if entry.user_id != user.id:
        return JsonResponse({
            'status': status.HTTP_401_UNAUTHORIZED,
            'error': f'Entry does not belong to {user}.'
        })

    if request.method == 'GET':
        serializer = EntrySerializer(entry)
        return JsonResponse(serializer.data)
            
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EntrySerializer(entry, data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse({
                'data':serializer.data,
                'status':status.HTTP_200_OK
            })
    elif request.method == 'DELETE':
        entry.delete()
        return JsonResponse({
                'message': 'Entry deleted.',
                'status':status.HTTP_200_OK
            })
    else:
        return JsonResponse({
            'status': status.HTTP_400_BAD_REQUEST,
            'error': 'Invalid request'
        })
