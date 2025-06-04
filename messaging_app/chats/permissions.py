# # permissions.py
# from rest_framework.permissions import BasePermission

# class IsConversationParticipant(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user in obj.participants.all()

from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient
