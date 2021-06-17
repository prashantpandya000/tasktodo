from django.shortcuts import get_object_or_404, render

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User

from django.utils import timezone
from django.utils.module_loading import import_string

from .models import Attachment, Board, Comment, Item, Label, List













class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [CanViewBoard]

    def get_object(self):
        pk = self.kwargs.get('pk')
        label = get_object_or_404(Label, pk=pk)
        self.check_object_permissions(self.request, label.board)
        return label



class AttachmentList(generics.ListCreateAPIView):
    
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [
        permissions.AllowAny
    ]




