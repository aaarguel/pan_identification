from rest_framework import serializers

from chat.models import Thread,ChatMessage
from django.contrib.auth import get_user_model

User= get_user_model()
class UserSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = User
        fields = ('first_name', 'username')

class ChatMessageSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = ChatMessage
        fields = ['message']

class ThreadSerializer(serializers.HyperlinkedModelSerializer   ):
    first_person = UserSerializer()
    second_person = UserSerializer()
    chatmessage_thread = ChatMessageSerializer(many=True)
    class Meta:
        model = Thread
        fields = ('id','first_person','second_person','chatmessage_thread')





