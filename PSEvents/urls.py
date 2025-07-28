from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    
    # Publishing
    path('api/publish/', views.PublishMessageView.as_view(), name='publish_message'),
    path('api/topics/create/', views.CreateTopicView.as_view(), name='create_topic'),
    
    # Subscriptions
    path('api/subscriptions/create/', views.CreateSubscriptionView.as_view(), name='create_subscription'),
    
    # Listing
    path('api/topics/', views.ListTopicsView.as_view(), name='list_topics'),
    path('api/subscriptions/', views.ListSubscriptionsView.as_view(), name='list_subscriptions'),
    
    # Messages
    path('api/messages/published/', views.GetPublishedMessagesView.as_view(), name='get_published_messages'),
    path('api/messages/received/', views.GetReceivedMessagesView.as_view(), name='get_received_messages'),
]