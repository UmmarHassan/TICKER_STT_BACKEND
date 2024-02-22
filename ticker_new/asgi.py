"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticker_new.settings')

from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application

application = get_asgi_application()

from channels.auth import AuthMiddlewareStack

# from polls.consumers import VideoUploadConsumer,OrderProgress,CounterConsumer,VideoConsumer,YoloConsumer,YolotwoConsumer
from django.conf import settings
#When defining the url pattern for websocket for connecting to the url of view write them in same order as views of url of views

from django.urls import re_path


ws_pattern=[
#     # path('ws/pizza/<order_id>',OrderProgress.as_asgi()),
#         # path('',PizzaProgress.as_asgi()),
#                 # path('yolo/',YoloProgress.as_asgi()),
# # Counter running consumer is Counter Consumer
#         # path('', CounterConsumer.as_asgi()),
#         # frame running consumer is VideoConsumer
#         # path('', VideoConsumer.as_asgi()),

#                 path('', YoloConsumer.as_asgi()),
#                  path('ws/two/', YolotwoConsumer.as_asgi()),
#     # path('ws/video/<int:video_id>/',VideoUploadConsumer.as_asgi(), name='ws_video'),

#     path('ws/video/', VideoUploadConsumer.as_asgi()),



]
application=ProtocolTypeRouter({
    "http":application,
    'websocket':AuthMiddlewareStack(URLRouter(ws_pattern))
})


# # 👇 2. Update the application var
# from channels.security.websocket import AllowedHostsOriginValidator
# from myapp.routing import websocket_urlpatterns

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
# })