from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from .models import UserKeyword

from django.contrib.auth.models import User
from .models import UserKeyword
@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):

    if created:
        admin_user = User.objects.get(username='admin')  # Assuming 'admin' is the username of the admin user
        admin_keywords = UserKeyword.objects.filter(user='admin')
        predefined_keywords = list(admin_keywords.values_list('keyword', flat=True))
        print('********keywords:************', predefined_keywords)

        #GETTING THE PARAGRAPH FROM THE CLIENT
        sentences = instance.message.split('.')
        # Initialize a list to store matched keyword sentences
        matched_keyword_sentences = []
        # Iterate over each sentence
        for sentence in sentences:
            # Check for each predefined keyword
            for keyword in predefined_keywords:
                if keyword in sentence:
                    # If a keyword is found, add the matched sentence to the list
                    matched_keyword_sentences.append(f"{keyword}: {sentence.strip()}")

        if matched_keyword_sentences:
            # Prepare the notification message
            notification_message = '\n'.join(matched_keyword_sentences)

            # Send notification to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'public_room',
                {
                    "type": "send_notification",
                    'message': f'{notification_message}'
                }
            )
