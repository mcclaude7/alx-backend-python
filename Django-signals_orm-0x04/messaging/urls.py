from django.urls import path
from . import views

urlpatterns = [
    path('delete_account/', views.delete_user, name='delete_account'),
    path('threads/', views.threaded_messages_view, name='threaded_messages'),
]  

