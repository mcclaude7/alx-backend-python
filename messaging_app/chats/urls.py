# from django.urls import path, include
# from rest_framework_nested import routers
# from .views import ConversationViewSet, MessageViewSet

# # Primary router for conversations
# router = routers.DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')

# # Nested router for messages within conversations
# convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(convo_router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]




