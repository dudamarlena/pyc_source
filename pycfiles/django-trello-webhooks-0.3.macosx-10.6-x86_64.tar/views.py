# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-trello-webhooks/lib/python2.7/site-packages/trello_webhooks/views.py
# Compiled at: 2014-11-29 10:37:29
import logging
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from trello_webhooks.models import Webhook
logger = logging.getLogger(__name__)

@csrf_exempt
def api_callback(request, auth_token, trello_model_id):
    """Handle the callback from Trello.

    Callbacks come in two flavours - a HEAD request is the initial
    activation check from Trello - we can ignore that and simply respond
    with a 200. A POST request is an event - with the event payload as per
    the API docs.

    New callback events are stored locally, and then the django signal
    is sent so that client apps can handle the event.

    NB This is all happening synchronously whilst Trello is waiting for a
    response from the view, so don't have long-running processes handling
    the signal.

    Args:
        auth_token: string, the user token against which the webhook was
            registered.
        trello_model_id: string, the model id - which was registered with
            Trello initially. This is the object that has generated the
            callback.
    """
    if request.method == 'HEAD':
        logger.info("Trello activation callback received for '%s'", trello_model_id)
        return HttpResponse()
    if request.method == 'POST':
        logger.info("Trello event callback received for '%s'", trello_model_id)
        try:
            Webhook.objects.get(auth_token=auth_token, trello_model_id=trello_model_id).add_callback(request.body)
            return HttpResponse('Message received')
        except Webhook.DoesNotExist:
            logger.warning('No webhook found for %s:%s', trello_model_id, trello_model_id)
            return HttpResponseNotFound()

    return HttpResponseNotAllowed(['HEAD', 'POST'])