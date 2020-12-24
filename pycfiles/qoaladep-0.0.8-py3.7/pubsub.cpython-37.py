# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/gcp/pubsub/pubsub.py
# Compiled at: 2020-03-12 06:38:40
# Size of source mod 2**32: 1298 bytes
from google.cloud import pubsub_v1

def callback(message):
    message.ack()


def publish_message(project_id, topic_name, payload_pubsub):
    """[Function for publishing message to pubsub]
    
    Arguments:
        project_id {[string]} -- [Project ID]
        topic_name {[string]} -- [Topic name for pubsub]
        payload_pubsub {[string]} -- [Message payload for publising message]

    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    result = publisher.publish(topic_path, data=data).result()
    return result


def pull_message(project_id, subscription_name, timeout=5.0):
    """[Function for pulling message from pubsub]
    
    Arguments:
        project_id {[string]} -- [Project ID]
        subscription_name {[string]} -- [Subscription name for pubsub]
        timeout {[float]} -- [Time limit for waiting pulling message]
    
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        result = streaming_pull_future.result(timeout=timeout)
    except:
        result = streaming_pull_future.cancel()

    return result