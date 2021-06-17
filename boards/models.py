from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Max
from authentication.models import User

class Board(models.Model):
    owner_model = models.ForeignKey(ContentType, blank=False, null=False,
                                    related_name='board',
                                    on_delete=models.CASCADE,
                                    limit_choices_to=models.Q(app_label='users', model='user'))
    owner_id = models.PositiveIntegerField(null=False, blank=False)
    owner = GenericForeignKey('owner_model', 'owner_id')

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    # Only one of the below will be used from the frontend
    image_url = models.URLField(blank=True, null=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title



class List(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        filtered_objects = List.objects.filter(board=self.board)
        if not self.order and filtered_objects.count() == 0:
            self.order = 2 ** 16 - 1
        elif not self.order:
            self.order = filtered_objects.aggregate(Max('order'))[
                'order__max'] + 2 ** 16 - 1
        return super().save(*args, **kwargs)



class Item(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    image_url = models.URLField(blank=True, null=False)
    color = models.CharField(blank=True, null=False, max_length=6)  # Hex Code

    order = models.DecimalField(max_digits=30,decimal_places=15, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        filtered_objects = Item.objects.filter(list=self.list)
        if not self.order and filtered_objects.count() == 0:
            self.order = 2 ** 16 - 1 
        elif not self.order:
            self.order = filtered_objects.aggregate(Max('order'))[
                'order__max'] + 2 ** 16 - 1
        return super().save(*args, **kwargs)




class Attachment(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='attachments')
    upload = models.FileField(upload_to='attachments')