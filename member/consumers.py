from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt, json

User = get_user_model()

class VoucherConsumer(WebsocketConsumer):
    def connect(self):
        # Extract the JWT token from the headers
        token_header = dict(self.scope['headers']).get(b'authorization', None)
        
        if not token_header:
            raise DenyConnection("Authorization token not provided.")

        try:
            # Decode the JWT token manually
            token = token_header.decode().split(' ')[1]  # Extract Bearer token
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')

            # Fetch the user from the database
            user = User.objects.get(id=user_id)
            self.user = user  # Store the authenticated user in the consumer

            # Add this WebSocket connection to the "voucher_group"
            async_to_sync(self.channel_layer.group_add)(
                "voucher_group",  # Group name
                self.channel_name
            )
            self.accept()  # Accept the WebSocket connection

        except jwt.ExpiredSignatureError:
            raise DenyConnection("Token has expired.")
        except jwt.InvalidTokenError:
            raise DenyConnection("Invalid token.")
        except User.DoesNotExist:
            raise DenyConnection("User not found.")

    def disconnect(self, close_code):
        # Remove this WebSocket connection from the "voucher_group"
        async_to_sync(self.channel_layer.group_discard)(
            "voucher_group",
            self.channel_name
        )

    # Receive a message from the group and send it to the WebSocket client
    def send_voucher_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
