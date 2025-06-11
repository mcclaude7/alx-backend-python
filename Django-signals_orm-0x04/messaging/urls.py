from django.urls import path
from . import views

urlpatterns = [
    path('delete_account/', views.delete_user, name='delete_account'),
    path('threads/', views.threaded_messages_view, name='threaded_messages'),
    path('unread/', views.unread_inbox_view, name='unread_inbox'),
    path('conversation/', views.conversation_view, name='conversation_view'),

]  

