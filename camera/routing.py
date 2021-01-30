from channels.routing import route
# from .consumers import ws_connect, ws_receive, ws_disconnect, chat_join, chat_leave, chat_send
from .consumers import ChatConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from channels.auth import AuthMiddlewareStack

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/camera/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]

# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We could path match here if we wanted.
websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ChatConsumer.connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ChatConsumer.receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ChatConsumer.disconnect),
]

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", ChatConsumer.chat_join, command="^join$"),
    route("chat.receive", ChatConsumer.chat_leave, command="^leave$"),
    route("chat.receive", ChatConsumer.chat_send, command="^send$"),
]