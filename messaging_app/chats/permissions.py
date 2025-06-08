
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
        user = request.user
        is_participant = user in obj.conversation.participants.all()

        if request.method in permissions.SAFE_METHODS:
            return is_participant
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant and user == obj.sender
        
        if request.method == 'POST':
            return is_participant
        
        return False
        # return (
        #     request.user == obj.sender or 
        #     request.user == obj.recipient or
        #     request.user in obj.conversation.participants.all()
        # )


