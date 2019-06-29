from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'seating/index.html', {})

def service_date(request, service_date):
    return render(request, 'seating/room.html', {
        'service_date_json': mark_safe(json.dumps(service_date))
    })