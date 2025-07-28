from django.db import models
from django.utils import timezone

class PublishedMessage(models.Model):
    """Model to track published messages"""
    message_id = models.CharField(max_length=255, unique=True)
    topic_name = models.CharField(max_length=255)
    message_data = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='published')
    
    def __str__(self):
        return f"{self.message_id} - {self.topic_name}"
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "Published Message"
        verbose_name_plural = "Published Messages"

class ReceivedMessage(models.Model):
    """Model to track received messages"""
    message_id = models.CharField(max_length=255, unique=True)
    subscription_name = models.CharField(max_length=255)
    message_data = models.TextField()
    received_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.message_id} - {self.subscription_name}"
    
    class Meta:
        ordering = ['-received_at']
        verbose_name = "Received Message"
        verbose_name_plural = "Received Messages"
