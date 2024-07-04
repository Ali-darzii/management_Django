from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
