from django.db import models
from channels.layers import get_channel_layer
from .settings import MSG_TYPE_MESSAGE
import json
from asgiref.sync import async_to_sync
#from channels import Group

channel_layer = get_channel_layer()
from six import python_2_unicode_compatible

@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """
    # Room title
    title = models.CharField(max_length=255, default='title')

    def str(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
         
        return (channel_layer.channel_name("room-%s" % self.id))

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )