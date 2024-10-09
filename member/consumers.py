from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync 

class VoucherConsumer(WebsocketConsumer):

    def connect(self):
        # Add WebSocket connection to 'voucher_group'
        async_to_sync(self.channel_layer.group_add)(
            "voucher_group",
            self.channel_name
        )
        self.accept()  # Accept the WebSocket connection

    def disconnect(self, close_code):
        # Remove WebSocket connection from 'voucher_group'
        async_to_sync(self.channel_layer.group_discard)(
            "voucher_group",
            self.channel_name
        )

    # Handle incoming WebSocket message and send it to the client
    def send_voucher_message(self, event):
        message = event['message']
        print(f"Received WebSocket message: {message}")  # Debugging
        self.send(text_data=json.dumps({
            'message': message
        }))
