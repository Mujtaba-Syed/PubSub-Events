from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import PublishedMessage, ReceivedMessage
from .pubsub_service import PubSubService

def csrf_exempt_dispatch(cls):
    """Decorator to make dispatch method CSRF exempt"""
    cls.dispatch = method_decorator(csrf_exempt)(cls.dispatch)
    return cls

@csrf_exempt_dispatch
class PublishMessageView(View):
    """API endpoint to publish a message"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            topic_name = data.get('topic_name')
            message_data = data.get('message_data')
            
            # Initialize PubSub service
            pubsub_service = PubSubService()
            
            # Create topic if it doesn't exist
            pubsub_service.create_topic(topic_name)
            
            # Publish message
            message_id = pubsub_service.publish_message(topic_name, message_data)
            
            if message_id:
                return JsonResponse({
                    'success': True,
                    'message_id': message_id,
                    'topic_name': topic_name,
                    'message_data': message_data
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to publish message'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class GetPublishedMessagesView(View):
    """Get all published messages"""
    
    def get(self, request):
        try:
            messages = PublishedMessage.objects.all().order_by('-published_at')
            message_list = []
            
            for msg in messages:
                message_list.append({
                    'message_id': msg.message_id,
                    'topic_name': msg.topic_name,
                    'message_data': msg.message_data,
                    'published_at': msg.published_at.isoformat(),
                    'status': msg.status
                })
            
            return JsonResponse({
                'success': True,
                'messages': message_list,
                'count': len(message_list)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class GetReceivedMessagesView(View):
    """Get all received messages"""
    
    def get(self, request):
        try:
            messages = ReceivedMessage.objects.all().order_by('-received_at')
            message_list = []
            
            for msg in messages:
                message_list.append({
                    'message_id': msg.message_id,
                    'subscription_name': msg.subscription_name,
                    'message_data': msg.message_data,
                    'received_at': msg.received_at.isoformat(),
                    'processed': msg.processed
                })
            
            return JsonResponse({
                'success': True,
                'messages': message_list,
                'count': len(message_list)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class ListTopicsView(View):
    """List all topics"""
    
    def get(self, request):
        try:
            pubsub_service = PubSubService()
            topics = pubsub_service.list_topics()
            
            return JsonResponse({
                'success': True,
                'topics': topics,
                'count': len(topics)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class ListSubscriptionsView(View):
    """List all subscriptions"""
    
    def get(self, request):
        try:
            pubsub_service = PubSubService()
            subscriptions = pubsub_service.list_subscriptions()
            
            return JsonResponse({
                'success': True,
                'subscriptions': subscriptions,
                'count': len(subscriptions)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

@csrf_exempt_dispatch
class CreateTopicView(View):
    """Create a new topic"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            topic_name = data.get('topic_name')
            
            if not topic_name:
                return JsonResponse({
                    'success': False,
                    'error': 'topic_name is required'
                }, status=400)
            
            pubsub_service = PubSubService()
            success = pubsub_service.create_topic(topic_name)
            
            if success:
                return JsonResponse({
                    'success': True,
                    'message': f'Topic {topic_name} created successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to create topic {topic_name}'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

@csrf_exempt_dispatch
class CreateSubscriptionView(View):
    """Create a new subscription"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            topic_name = data.get('topic_name')
            subscription_name = data.get('subscription_name')
            
            if not topic_name or not subscription_name:
                return JsonResponse({
                    'success': False,
                    'error': 'Both topic_name and subscription_name are required'
                }, status=400)
            
            pubsub_service = PubSubService()
            success = pubsub_service.create_subscription(topic_name, subscription_name)
            
            if success:
                return JsonResponse({
                    'success': True,
                    'message': f'Subscription {subscription_name} created successfully for topic {topic_name}'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to create subscription {subscription_name}'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class HealthCheckView(View):
    """Health check endpoint"""
    
    def get(self, request):

        try:
            pubsub_service = PubSubService()
            print("project_id", pubsub_service.project_id)
            return JsonResponse({
                'success': True,
                'status': 'healthy',
                'project_id': pubsub_service.project_id,
                'message': 'Django Pub/Sub service is running'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'status': 'unhealthy',
                'error': str(e)
            }, status=500)