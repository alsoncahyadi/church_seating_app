import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

# from .models import Thread, ChatMessage

class SeatConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        print("received json:", content)
        await self.send_json({
            'data': 'Okay'
        })
