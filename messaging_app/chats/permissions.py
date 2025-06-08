
from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
    

class IsMessageParticipant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.sender or 
            request.user == obj.recipient or
            request.user in obj.conversation.participants.all()
        )


