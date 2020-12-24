# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/views.py
# Compiled at: 2019-12-02 16:01:32
# Size of source mod 2**32: 2788 bytes
import json, logging
from braces import views
from django import forms
from django.views.generic import View
from atws.wrapper import AutotaskAPIException, AutotaskProcessException
from django.http import HttpResponse, HttpResponseBadRequest
from djautotask import sync, models
from djautotask.api import parse_autotaskprocessexception, parse_autotaskapiexception
logger = logging.getLogger(__name__)

class CallBackView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, View):
    CALLBACK_TYPES = {'ticket': (
                sync.TicketSynchronizer, models.Ticket)}

    def post(self, request, *args, **kwargs):
        """
        Add, OR update entity by fetching it from AT. The only real useful
        information we get from the callback is the id of the ticket. Right
        now Autotask only supports callbacks for Tickets, but it looks like
        support could be added for any other entity at some point. We don't
        receive the ticket object, just its ID, current status, the datetime
        it was originally created, and the user domain it came from, which
        is a lot of useless info. Use the ID to sync the ticket.

        Note that we don't get a callback when a ticket is deleted, so it will
        only get scooped up next sync.
        """
        form = CallBackForm(request.POST)
        error_msg = None
        if not form.is_valid():
            fields = ', '.join(form.errors.keys())
            msg = 'Received callback with missing parameters: {}.'.format(fields)
            logger.warning(msg)
            return HttpResponseBadRequest(json.dumps(form.errors))
        else:
            entity_id = form.cleaned_data['id']
            synchronizer = sync.TicketSynchronizer
            try:
                try:
                    self.handle(entity_id, synchronizer)
                except AutotaskProcessException as e:
                    error_msg = parse_autotaskprocessexception(e)
                except AutotaskAPIException as e:
                    error_msg = parse_autotaskapiexception(e)

            finally:
                if error_msg:
                    logger.error('API call failed in Ticket ID {} callback: {}'.format(entity_id, error_msg))

            return HttpResponse(status=204)

    def handle(self, entity_id, synchronizer):
        """
        Do the interesting stuff here, so that it can be overridden in
        a child class if needed.
        """
        synchronizer().fetch_sync_by_id(entity_id)


class CallBackForm(forms.Form):
    id = forms.IntegerField()