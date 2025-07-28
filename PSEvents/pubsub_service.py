import json
import logging
from google.cloud import pubsub_v1
from django.conf import settings
from .models import PublishedMessage, ReceivedMessage

logger = logging.getLogger(__name__)

class PubSubService:
    def __init__(self):
        """Initialize the Pub/Sub service"""
        try:
            # Get project ID from settings or environment
            self.project_id = getattr(settings, 'GOOGLE_CLOUD_PROJECT_ID', 'robotic-tiger-467309-t6')
            print("project_id", self.project_id)

            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()
            
            logger.info(f"PubSub service initialized for project: {self.project_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize PubSub service: {e}")
            raise
    
    def publish_message(self, topic_name, message_data, **kwargs):
        """
        Publish a message to a topic
        
        Args:
            topic_name (str): Name of the topic
            message_data (dict): Message data to publish
            **kwargs: Additional message attributes
        
        Returns:
            str: Message ID if successful, None otherwise
        """
        try:
            # Create the topic path
            topic_path = self.publisher.topic_path(self.project_id, topic_name)
            
            # Convert message data to JSON string
            if isinstance(message_data, dict):
                message_json = json.dumps(message_data)
            else:
                message_json = str(message_data)
            
            # Publish the message
            future = self.publisher.publish(
                topic_path,
                data=message_json.encode('utf-8'),
                **kwargs
            )
            
            message_id = future.result()
            # Save to database
            PublishedMessage.objects.create(
                message_id=message_id,
                topic_name=topic_name,
                message_data=message_json,
                status='published'
            )
            
            logger.info(f"Message published successfully. ID: {message_id}, Topic: {topic_name}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return None
    
    def create_topic(self, topic_name):
        """
        Create a new topic
        
        Args:
            topic_name (str): Name of the topic to create
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            topic_path = self.publisher.topic_path(self.project_id, topic_name)
            topic = self.publisher.create_topic(name=topic_path)
            logger.info(f"Topic created: {topic.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create topic: {e}")
            return False
    
    def create_subscription(self, topic_name, subscription_name):
        """
        Create a subscription for a topic
        
        Args:
            topic_name (str): Name of the topic
            subscription_name (str): Name of the subscription
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            topic_path = self.publisher.topic_path(self.project_id, topic_name)
            subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
            
            subscription = self.subscriber.create_subscription(
                name=subscription_path,
                topic=topic_path
            )
            
            logger.info(f"Subscription created: {subscription.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create subscription: {e}")
            return False
    
    def callback(self, message):
        """
        Callback function for processing received messages
        
        Args:
            message: The received message object
        """
        try:
            # Decode the message data
            message_data = message.data.decode('utf-8')
            
            # Save to database
            ReceivedMessage.objects.create(
                message_id=message.message_id,
                subscription_name=message.subscription,
                message_data=message_data,
                processed=False
            )
            
            logger.info(f"Message received: {message.message_id}")
            logger.info(f"Message data: {message_data}")
            
            # Acknowledge the message
            message.ack()
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Nack the message to retry
            message.nack()
    
    def subscribe_to_topic(self, subscription_name, timeout=None):
        """
        Subscribe to a topic and listen for messages
        
        Args:
            subscription_name (str): Name of the subscription
            timeout (int): Timeout in seconds (None for infinite)
        """
        try:
            subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
            
            # Create the subscription
            subscription = self.subscriber.subscribe(subscription_path, callback=self.callback)
            
            logger.info(f"Listening for messages on {subscription_path}")
            
            try:
                # Keep the subscription alive
                subscription.result(timeout=timeout)
            except KeyboardInterrupt:
                subscription.cancel()
                logger.info("Subscription cancelled")
            
        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
    
    def list_topics(self):
        """
        List all topics in the project
        
        Returns:
            list: List of topic names
        """
        try:
            project_path = f"projects/{self.project_id}"
            topics = self.publisher.list_topics(request={"project": project_path})
            return [topic.name.split('/')[-1] for topic in topics]
        except Exception as e:
            logger.error(f"Failed to list topics: {e}")
            return []
    
    def list_subscriptions(self):
        """
        List all subscriptions in the project
        
        Returns:
            list: List of subscription names
        """
        try:
            project_path = f"projects/{self.project_id}"
            subscriptions = self.subscriber.list_subscriptions(request={"project": project_path})
            return [sub.name.split('/')[-1] for sub in subscriptions]
        except Exception as e:
            logger.error(f"Failed to list subscriptions: {e}")
            return []