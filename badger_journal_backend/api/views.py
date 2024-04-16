from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view

from .models import Entry
from .serializers import EntrySerializer

# Create your views here.
@api_view(['GET', 'POST'])
def entry_list(request):
    """
    Return all entries or create an entry
    """
    if request.method == 'GET':
        entries = Entry.objects.all()

        serializer = EntrySerializer(entries, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({
            'status_code': 400,
            'error': 'Invalid request'
        })

@api_view(['GET', 'POST', 'DELETE'])
def entry_detail(request, pk):
    """
    Return a single entry, update an entry or delete an entry
    """ 
    if request.method == 'GET':
        try:
            entry = Entry.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'error': f'Entry with id {pk} not found.'
            })
        else:
            serializer = EntrySerializer(entry)
            return JsonResponse(serializer.data)
            
        return JsonResponse(data)
    else:
        return JsonResponse({
            'status_code': 400,
            'error': 'Invalid request'
        })
