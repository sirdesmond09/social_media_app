import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # authenticate the user
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        # join the broadcast group
        await self.channel_layer.group_add(
            "feed",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):

        # disconnect from feed
        await self.channel_layer.group_discard(
            "feed",
            self.channel_name
        )
        return super().disconnect(close_code)
    

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "feed",
            {
                "type": "feed_message",
                "message": data["message"]
            }
        )

    async def feed_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
