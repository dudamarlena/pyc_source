# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Development/django-sms-gateway/sms/views.py
# Compiled at: 2012-11-26 00:43:01
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from decimal import Decimal
import datetime, logging
from sms.models import Message, MessageSet, Gateway
logger = logging.getLogger('sms-gateway')

@csrf_exempt
def update_delivery_status(request):
    logger.debug('Status update received. %s' % request.GET)
    if not request.GET:
        return HttpResponse('OK')
    data = {}
    for k, v in request.GET.items():
        if isinstance(v, list) and len(v) == 1:
            data[k] = v[0]
        else:
            data[k] = v

    logger.debug('%s' % data)
    msg = Message.objects.get_matching_message(data)
    if not msg:
        logger.warn('Message could not be found: %s' % data)
        return HttpResponse('OK')
    logger.debug('Found message %i' % msg.pk)
    gateway = msg.gateway
    if not gateway.status_mapping or data.get(gateway.status_status) not in gateway.status_mapping.keys():
        msg.status = 'Failed'
    else:
        msg.status = gateway.status_mapping[data.get(gateway.status_status)]
    logger.debug('Updated status to %s' % msg.status)
    if msg.status == 'Delivered':
        if gateway.status_date:
            if gateway.status_date_format:
                msg.delivery_date = datetime.datetime.strptime(data.get(gateway.status_date), gateway.status_date_format)
            else:
                msg.delivery_date = datetime.datetime.fromtimestamp(float(data.get(gateway.status_date)))
        else:
            msg.delivery_date = datetime.datetime.now()
        logger.debug('Message was delivered at %s' % msg.delivery_date)
    else:
        msg.status_message = data.get(gateway.status_error_code)
        logger.debug('Error message was %s' % msg.status_message)
    if gateway.charge_keyword:
        charge = data.get(gateway.charge_keyword)
        if charge:
            msg.gateway_charge = charge
    msg.save()
    return HttpResponse('OK')


@csrf_exempt
def handle_reply(request):
    logger.debug('SMS Reply received.')
    if not request.GET:
        return HttpResponse('OK')
    data = {}
    for k, v in request.GET.items():
        if isinstance(v, list) and len(v) == 1:
            data[k] = v[0]
        else:
            data[k] = v

    msg = Message.objects.get_original_for_reply(data)
    if not msg:
        logger.warn('Original message could not be found: %s' % data)
        return HttpResponse('OK')
    logger.debug('Found message %i' % msg.pk)
    gateway = msg.gateway
    if gateway.reply_date_format:
        reply_date = datetime.datetime.strptime(data.get(gateway.reply_date), gateway.reply_date_format)
    else:
        reply_date = datetime.datetime.fromtimestamp(float(data.get(gateway.reply_date)))
    reply = msg.replies.create(content=data.get(gateway.reply_content), date=reply_date)
    logger.debug('Reply created')
    logger.debug('Message content was: %s' % reply.content)
    if msg.reply_callback:
        logger.debug('Callback found, running that.')
        msg.reply_callback(reply)
    return HttpResponse('OK')


def get_message_set_status(request, uuid):
    message_set = MessageSet.objects.get(uuid=uuid)
    message_set.update_data()
    if message_set.is_complete():
        return HttpResponse(json.dumps(message_set.data.values()))
    return HttpResponse(json.dumps({'percent_complete': message_set.percentage_complete}))