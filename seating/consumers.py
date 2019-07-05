import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

# from .models import Thread, ChatMessage

class SeatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.service_date = self.scope['url_route']['kwargs']['service_date']

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

    async def receive_json(self, content):
        print("received json:", content)

        await self.channel_layer.group_send(
            self.service_date,
            {
                'type': 'seat_change_blast',
                'data': content,
            }
        )

        # await self.send_json({
        #     'data': 'Okay',
        #     'seat': content,
        # })

    async def seat_change_blast(self, event):
        await self.send(text_data=json.dumps(event['data']))
