import os
# from channels import route
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })

# from channels import include
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
#from camera.routing import websocket_routing

from workpair.WOP.camera.routing import websocket_routing

application = ProtocolTypeRouter({
     "websocket": 
        URLRouter(
            [
                # Include sub-routing from an app.
                re_path(r"^/chat/stream" ,websocket_routing),

                # Custom handler for message sending (see Room.send_message).
                # Can't go in the include above as it's not got a 'path' attribute to match on.
                re_path("camera.routing.custom_routing"),

                # A default "http.request" route is always inserted by Django at the end of the routing list
                # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
                # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
                # fall through to normal views.
            ]
        ),   
})



# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we match
# on a path prefix, and then include routing from the chat module.
# channel_routing = [
#     # Include sub-routing from an app.
#     include("camera.routing.websocket_routing", path=r"^/chat/stream"),

#     # Custom handler for message sending (see Room.send_message).
#     # Can't go in the include above as it's not got a 'path' attribute to match on.
#     include("camera.routing.custom_routing"),

#     # A default "http.request" route is always inserted by Django at the end of the routing list
#     # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
#     # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
#     # fall through to normal views.
# ]