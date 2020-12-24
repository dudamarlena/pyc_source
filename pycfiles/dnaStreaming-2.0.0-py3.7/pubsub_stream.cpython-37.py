# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/demo/pubsub_stream.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 1617 bytes
import os, json
from google.cloud import pubsub_v1
from dnaStreaming.listener import Listener
from dnaStreaming import logger
gcp_project_id = os.getenv('GCP_PROJECT_ID', None)
gcp_pubsub_topic = os.getenv('GCP_PUBSUB_TOPIC', None)
gcp_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
if gcp_project_id is not None and gcp_pubsub_topic is not None and gcp_creds is not None:
    listener = Listener()
    ps_publisher = pubsub_v1.PublisherClient()
    topic_path = ps_publisher.topic_path(gcp_project_id, gcp_pubsub_topic)
    print(('\n[ACTIVITY] Sending messages to Pub/Sub topic {} in GCP\n[0]'.format(gcp_pubsub_topic)), end='')

    def callback(message, subscription_id, file_handle=None):
        callback.counter += 1
        logger.info('Processing article with ID: {}'.format(message['an']))
        m_data = json.dumps(message, ensure_ascii=False).encode('utf-8')
        ps_publisher.publish(topic_path, data=m_data)
        logger.info('Sent to GCP Pub/Sub, article with ID: {}'.format(message['an']))
        if callback.counter % 10 == 0:
            print(('[{}]'.format(callback.counter)), end='')
        else:
            print('.', end='')
        return True


    callback.counter = 0
    listener.listen(callback)
else:
    print('[ERROR]: Required ENV variables not set')
    if gcp_project_id is None:
        print('    - GCP_PROJECT_ID: GCP Project ID')
    if gcp_pubsub_topic is None:
        print('    - GCP_PUBSUB_TOPIC: GCP Pub/Sub Topic Name')
    if gcp_creds is None:
        print('    - GOOGLE_APPLICATION_CREDENTIALS: Path to Service Account JSON Credentials File')