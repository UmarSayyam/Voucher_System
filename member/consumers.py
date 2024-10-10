# # from channels.generic.websocket import WebsocketConsumer
# # import json
# # from asgiref.sync import async_to_sync 

# # class VoucherConsumer(WebsocketConsumer):

# #     def connect(self):
# #         # Add WebSocket connection to 'voucher_group'
# #         async_to_sync(self.channel_layer.group_add)(
# #             "voucher_group",
# #             self.channel_name
# #         )
# #         self.accept()  # Accept the WebSocket connection

# #     def disconnect(self, close_code):
# #         # Remove WebSocket connection from 'voucher_group'
# #         async_to_sync(self.channel_layer.group_discard)(
# #             "voucher_group",
# #             self.channel_name
# #         )

# #     # Handle incoming WebSocket message and send it to the client
# #     def send_voucher_message(self, event):
# #         message = event['message']
# #         print(f"Received WebSocket message: {message}")  # Debugging
# #         self.send(text_data=json.dumps({
# #             'message': message
# #         }))






# # from channels.generic.websocket import WebsocketConsumer
# # from asgiref.sync import async_to_sync
# # from channels.exceptions import DenyConnection
# # # from rest_framework_simplejwt.tokens import AccessToken
# # from django.contrib.auth import get_user_model
# # from django.conf import settings
# # import json
# # import jwt

# # # User = get_user_model()

# # class VoucherConsumer(WebsocketConsumer):
# #     def connect(self):
# #         # Get the JWT token from the headers
# #         # token_header = self.scope['headers']
# #         # token = None

# #         # Extract the 'Authorization' header
# #         # for header in token_header:
# #         #     if header[0] == b'authorization':
# #         #         token = header[1].decode().split(' ')[1]  # Extract the token from 'Bearer <token>'

# #         # if not token:
# #         #     # Deny the connection if no token is provided
# #         #     raise DenyConnection("Authorization token not provided.")

# #         try:
# #             # Validate the JWT token and get the user
# #             # access_token = AccessToken(token)
# #             # user = User.objects.get(id=access_token['user_id'])

# #             # # Check if the user is authorized (e.g., an admin or voucher creator)
# #             # # You can add custom logic here to check if the user is allowed
# #             # self.user = user  # Store the authenticated user in the consumer

# #             # Add this WebSocket connection to the "voucher_group"
# #             async_to_sync(self.channel_layer.group_add)(
# #                 "voucher_group",  # Group name
# #                 self.channel_name
# #             )
# #             self.accept()  # Accept the WebSocket connection

# #         except Exception as e:
# #             pass
# #             # Deny the connection if the token is invalid or the user is unauthorized
# #             # raise DenyConnection(f"Connection denied: {str(e)}")

# #     def disconnect(self, close_code):
# #         # Remove this WebSocket connection from the "voucher_group"
# #         async_to_sync(self.channel_layer.group_discard)(
# #             "voucher_group",
# #             self.channel_name
# #         )

# #     # Receive a message from the group and send it to the WebSocket client
# #     def send_voucher_message(self, event):
# #         message = event['message']
# #         self.send(text_data=json.dumps({
# #             'message': message
# #         }))





# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from channels.exceptions import DenyConnection
# from django.contrib.auth import get_user_model
# import jwt  # Import PyJWT for manual JWT decoding
# from django.conf import settings
# import json

# User = get_user_model()

# class VoucherConsumer(WebsocketConsumer):
#     def connect(self):
#         token_header = self.scope['headers']
#         token = None

#         # Extract the 'Authorization' header
#         for header in token_header:
#             if header[0] == b'authorization':
#                 token = header[1].decode().split(' ')[1]  # Extract the token from 'Bearer <token>'

#         if not token:
#             raise DenyConnection("Authorization token not provided.")

#         try:
#             # Decode the JWT token manually using the PyJWT library
#             decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             user_id = decoded_token.get('user_id')

#             # Fetch the user from the database
#             user = User.objects.get(id=user_id)
#             self.user = user  # Store the authenticated user in the consumer

#             # Add this WebSocket connection to the "voucher_group"
#             async_to_sync(self.channel_layer.group_add)(
#                 "voucher_group",  # Group name
#                 self.channel_name
#             )
#             self.accept()  # Accept the WebSocket connection

#         except jwt.ExpiredSignatureError:
#             raise DenyConnection("Token has expired.")
#         except jwt.InvalidTokenError:
#             raise DenyConnection("Invalid token.")
#         except User.DoesNotExist:
#             raise DenyConnection("User not found.")

#     def disconnect(self, close_code):
#         # Remove this WebSocket connection from the "voucher_group"
#         async_to_sync(self.channel_layer.group_discard)(
#             "voucher_group",
#             self.channel_name
#         )

#     # Receive a message from the group and send it to the WebSocket client
#     def send_voucher_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps({
#             'message': message
#         }))






from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
import json

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
