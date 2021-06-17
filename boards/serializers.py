from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.urls import Resolver404

from rest_framework import serializers
from rest_framework.fields import Field

from django.urls.base import resolve, reverse

from authentication.models import User
from users.serializers import UserSerializer

from .models import Attachment, Board, Item, List


class AttachmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attachment
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Item
        exclude = ['list']

    def get_assigned_to(self, obj):
        queryset = obj.assigned_to.all()
        return UserSerializer(queryset, many=True).data


class ListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = List
        exclude = ['board']

    def get_items(self, obj):
        queryset = Item.objects.filter(list=obj).order_by('order')
        return ItemSerializer(queryset, many=True).data



class BoardSerializer(ShortBoardSerializer):
    lists = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'image', 'image_url',
                   'created_at', 'owner', 'lists' ]

    def get_lists(self, obj):
        queryset = List.objects.filter(board=obj).order_by('order')
        return ListSerializer(queryset, many=True).data

    def validate(self, data):
        return data 