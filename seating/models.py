from djongo import models
from model_utils import Choices
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class Seats(models.Model):
    STATE = Choices(
        (0, 'vacant', 'vacant'),
        (1, 'occupied', 'occupied')
    )

    DEFAULT_LAYOUT = [
        ['1A', '1B', '1C', '1D', '1E', '1F', '1G',],
        ['2A', '2B', '2C', '2D', '2E', '2F', '2G',],
        ['3A', '3B', '3C', '3D', '3E', '3F', '3G',],
        ['4A', '4B', '4C', '4D', '4E', '4F', '4G',],
        ['5A', '5B', '5C', '5D', '5E', '5F', '5G',],
        ['6A', '6B', '6C', '6D', '6E', '6F', '6G',],
        ['7A', '7B', '7C', '7D', '7E', '7F', '7G',],
        ['8A', '8B', '8C', '8D', '8E', '8F', '8G',],
        ['9A', '9B', '9C', '9D', '9E', '9F', '9G',],
    ]

    layout = models.ListField(default=DEFAULT_LAYOUT)
    states = models.DictField(default={})

    def set_state(self, seat_id, state):
        self.states[seat_id] = state
        return self.states[seat_id]

    def __str__(self):
        return str(self.layout)

    class Meta:
        abstract = True

class Service(models.Model):
    service_date = models.DateField(max_length=255, db_index=True)
    seats = models.EmbeddedModelField(model_container=Seats, default=Seats())

    objects = models.DjongoManager()

    def get_or_new_now():
        return Service.get_or_new(datetime.now())

    def get_or_new(date):
        service = None
        try:
            service = Service.objects.get(service_date=date)
        except ObjectDoesNotExist:
            service = Service.objects.create(service_date=date, seats=Seats())
        
        return service
