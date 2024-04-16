from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Entry

# Create your views here.
def entry_list(request):
    """
    Return all entries
    """
    entries = Entry.objects.all()

    data = {'entries': list(entries.values())}

    return JsonResponse(data)

def entry_detail(request, pk):
    """
    Return a single entry
    """ 
    try:
        entry = Entry.objects.get(pk = pk)
    except ObjectDoesNotExist:
        return JsonResponse({
            'status_code': 404,
            'error': f'Entry with id {pk} not found.'
        })
    else:
        data = {
            'id': entry.id,
            'title': entry.title,
            'text': entry.text,
            'date': str(entry.date),
            'user': entry.user.username
        }
        
    return JsonResponse(data)