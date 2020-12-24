# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/messaging/send.py
# Compiled at: 2014-11-25 17:55:11
import logging
from twilio.rest import TwilioRestClient
import pyrowire.config.configuration as config

def sms(message_data, key='reply'):
    """
    wrapper function around the twilio.rest api to send a message
    :param message_data: the message data object containing the handled message information
    :param key: the key for the message data object that holds the final response
    :return: boolean, whether the twilio message was created successfully.
    :raise e: TypeError if message_data is None
    """
    if not message_data:
        raise TypeError('message_data must not be None')
    logging.basicConfig(level=config.log_level())
    logger = logging.getLogger(__name__)
    if not message_data:
        logger.error(TypeError('Message data must be provided'))
        return False
    twilio_config = config.twilio(message_data['topic'])
    twilio_client = TwilioRestClient(twilio_config['account_sid'], twilio_config['auth_token'])
    try:
        twilio_client.messages.create(to=message_data['number'], from_=twilio_config['from_number'], body=message_data[key])
        return True
    except Exception as e:
        logger.error(e)
        return False


def mms(message_data, include_text=False, text_key='reply', media_url=None):
    """
    wrapper function around the twilio.rest api to send a message
    ** Currently only works with Short Codes in the US **
    :param message_data: the message data object containing the handled message information
    :param key: the key for the message data object that holds the final response
    :return: boolean, whether the twilio message was created successfully.
    :raise e: TypeError if message_data is None
    """
    if not message_data:
        raise TypeError('message_data must not be None')
    logging.basicConfig(level=config.log_level())
    logger = logging.getLogger(__name__)
    if not message_data or not media_url:
        missing_item = 'data' if not message_data else 'media_url'
        logger.error(TypeError('Message %s must be provided' % missing_item))
        return False
    twilio_config = config.twilio(message_data['topic'])
    twilio_client = TwilioRestClient(twilio_config['account_sid'], twilio_config['auth_token'])
    try:
        if include_text:
            twilio_client.messages.create(to=message_data['number'], from_=twilio_config['from_number'], body=message_data[text_key], media_url=media_url)
        else:
            twilio_client.messages.create(to=message_data['number'], from_=twilio_config['from_number'], media_url=media_url)
        return True
    except Exception as e:
        logger.error(e)
        return False