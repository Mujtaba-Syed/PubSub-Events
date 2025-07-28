from django.contrib import admin
from .models import PublishedMessage, ReceivedMessage
# Register your models here.
admin.site.register(PublishedMessage)
admin.site.register(ReceivedMessage)
