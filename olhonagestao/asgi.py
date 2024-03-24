import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from apps.authentication import routing as olhonagestao_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhonagestao.settings')
print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasssa')

# Obtenha a aplicação ASGI padrão do Django
django_asgi_application = get_asgi_application()

# Roteamento WebSocket para o aplicativo Channels
application = ProtocolTypeRouter({
    "http": django_asgi_application,
    "websocket": URLRouter(
        olhonagestao_routing.websocket_urlpatterns
    ),
})
