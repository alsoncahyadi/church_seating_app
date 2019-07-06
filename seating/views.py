from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import *
import json

def index(request):
    return render(request, 'seating/index.html', data)

def service_date(request, service_date):
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

    print(layout,states,layout_with_state)
    
    return render(request, 'seating/index.html', {
        'service_date_json': mark_safe(json.dumps(service_date)),
        'layout': layout_with_state,
    })