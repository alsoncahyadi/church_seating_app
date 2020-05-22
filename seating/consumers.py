import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import *

# from .models import Thread, ChatMessage

class SeatConsumer(AsyncJsonWebsocketConsumer):
    END_STATE_MAP = {
        # beginning state => end state
        'vacant': 'occupied',
        'occupied': 'vacant',
    }

    @database_sync_to_async
    def get_service(self, date):
        return Service.get_or_new(date)

    @database_sync_to_async
    def set_seat_state(self, seat_id, state):
        self.service.seats.set_state(seat_id, state)
        self.service.save()

    async def connect(self):
        self.service_date = self.scope['url_route']['kwargs'].get(
            'service_date',
            datetime.now().strftime("%Y-%m-%d") # default
        )
        self.service = await self.get_service(datetime.strptime(self.service_date, Service.DATE_FORMAT))

        await self.channel_layer.group_add(
            self.service_date,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.service_date,
            self.channel_name
        )

    async def receive_json(self, data):
        print("received json:", data)

        new_state = self.END_STATE_MAP[data['state']]
        await self.set_seat_state(data['id'], new_state)

        blast_data = {
            'id': data['id'],
            'state': new_state,
        }

        await self.channel_layer.group_send(
            self.service_date,
            {
                'type': 'seat_change_blast',
                'data': blast_data,
            }
        )

    async def seat_change_blast(self, event):
        await self.send(text_data=json.dumps(event['data']))
