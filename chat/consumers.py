from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from users.models import Message,User,Group
from users.serializers import MessageSerializer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        
        # 1. Retrieve and send all messages for this group
        # self.send_group_messages()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # 2. Receive message from WebSocket
    def receive(self, text_data):
        print('1 ere etape ',text_data)
        text_data_json = json.loads(text_data)
        print('2 eme etape ',text_data_json)
        message_content = text_data_json['content']
        print('3 message_content ',message_content)
        
        source_user_id = text_data_json['source']
        print('4 source_user_id ',source_user_id)
        
        destination_user_id = text_data_json['destination']
        print('5 destination_user_id',destination_user_id)
        # 3. Create message and send to room group
        self.create_and_send_message(source_user_id, destination_user_id, message_content)

    # 4. Receive message from room group
    def chat_message(self, event):
        message_content = event['content']
        source_user_id = event['source']
        destination_user_id = event['destination']
        group_id= event['group']
        created_at=event['created_at']
        iid=event['id']
        # 5. Send message to WebSocket
        self.send(text_data=json.dumps({
            'content': message_content,
            'source': source_user_id,
            'destination': destination_user_id,
            'group': group_id,
            'id':iid,
            'created_at':created_at
        }))

    def create_and_send_message(self, source_user_id, destination_user_id, message_content):
        # Create the message in the database
        print('da5l la function source_user_id',source_user_id)
        print('da5l la function destination_user_id',destination_user_id)
        print('da5l la function message_content',message_content)
        source = User.objects.filter(id=source_user_id).first()  # Utilisez first() pour récupérer le premier objet de la requête
        destination = User.objects.filter(id=destination_user_id).first()
        group = Group.objects.filter(id=self.room_name).first()
        print('da5l la function source',source)        
        print('da5l la function destination',destination)        
        print('da5l la function group',group)
        content=message_content
        print('da5l la function content',content)
        message = Message.objects.create(source=source,destinataion=destination,group=group,content=content)
        print('da5l la function message a ete creer deja ',message)
        # Serialize the message
        serialized_message = MessageSerializer(message).data
        x={
                'type': 'chat.message',
                'content': serialized_message['content'],
                'created_at': serialized_message['created_at'],
                'source': serialized_message['source'],
                'destination': serialized_message['destinataion'],
                'group': serialized_message['group'],
                'id':serialized_message['id'],
            }
        print(x)
        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'content': serialized_message['content'],
                'created_at': serialized_message['created_at'],
                'source': serialized_message['source'],
                'destination': serialized_message['destinataion'],
                'group': serialized_message['group'],
                'id':serialized_message['id'],
            }
        )





































    # def send_group_messages(self):
    #     # Retrieve all messages for the current group from the database
    #     messages = Message.objects.filter(group_id=self.room_name)
    #     print('messages  ;;;',messages)
    #     # Serialize messages
    #     serialized_messages = MessageSerializer(messages, many=True).data
    #     print('serialized_messages  ;;;',serialized_messages)
        
    #     # Send each message to the WebSocket
    #     for message in serialized_messages:
    #         self.send(text_data=json.dumps({
    #             'content': message['content'],
    #             'source': message['source'],
    #             'destination': message['destination']
    #         }))
