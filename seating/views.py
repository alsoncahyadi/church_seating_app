from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import *
from datetime import datetime
import json

def index(request):
    service = Service.get_or_new_now()
    layout = service.seats.layout
    states = service.seats.states
    layout_with_state = []
    
    # Construct template layout
    for row in layout:
        layout_with_state.append([])
        for seat_id in row:
            state = states.get(seat_id, 'vacant')
            layout_with_state[-1].append({ 'id': seat_id, 'state': state })

    return render(request, 'seating/index.html', {
        'service_date': mark_safe(json.dumps('')),
        'layout': layout_with_state,
    })

def service_date(request, service_date):
    service_date_datetime = datetime.strptime(service_date, Service.DATE_FORMAT)
    service = Service.get_or_new(service_date_datetime)
    layout = service.seats.layout
    states = service.seats.states
    layout_with_state = []
    
    # Construct template layout
    for row in layout:
        layout_with_state.append([])
        for seat_id in row:
            state = states.get(seat_id, 'vacant')
            layout_with_state[-1].append({ 'id': seat_id, 'state': state })

    return render(request, 'seating/index.html', {
        'service_date': mark_safe(json.dumps(service_date)),
        'layout': layout_with_state,
    })