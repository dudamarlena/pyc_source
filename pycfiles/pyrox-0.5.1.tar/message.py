# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/messaging/message.py
# Compiled at: 2014-11-25 17:55:10


def message_from_request(request=None):
    """
    Utility method to extract relevant sms message data from inbound message
    :param request: the flask request object
    :return: message, a dict object of the message data
    """
    request_data = request.args if request.method == 'GET' else request.form
    message = {'message': request_data['Body'], 
       'number': request_data['From'], 
       'sid': request_data['MessageSid'], 
       'topic': request.view_args['topic'], 
       'from_city': get_if_available(request_data, 'FromCity'), 
       'from_state': get_if_available(request_data, 'FromState'), 
       'from_country': get_if_available(request_data, 'FromCountry'), 
       'from_zip': get_if_available(request_data, 'FromZip'), 
       'media': get_if_available(request_data, 'NumMedia'), 
       'reply': None}
    return message


def get_if_available(request_data, key):
    """
    returns a value for the provided key if it exists in request data
    :param request_data: request data where key may exist
    :param key: key to look for
    :return: value from request data if key exists, or dict if key is 'NumMedia'
    """
    if key in request_data.keys():
        if key == 'NumMedia':
            media = {'count': int(request_data['NumMedia']), 'media': {}}
            for i in range(media['count']):
                media['media'][request_data[('MediaUrl%s' % i)]] = request_data[('MediaContentType%s' % i)]

            return media
        return request_data[key]
    else:
        return