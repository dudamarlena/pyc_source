# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/views.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
import json
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import six
from django.views.generic import View
from djblets.avatars.services import URLAvatarService
from djblets.db.query import get_object_or_none
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.admin.server import get_server_url
from reviewboard.avatars import avatar_services
from reviewbotext.extension import ReviewBotExtension

def _serialize_user(request, user):
    """Serialize a user into a JSON-encodable format.

    Args:
        request (django.http.HttpRequest):
            The HTTP request.

        user (django.contrib.auth.models.User):
            The user to serialize.

    Returns:
        dict:
        A dictionary of data to be encoded and sent back to the client.
    """
    if user:
        service = avatar_services.for_user(user)
        if service:
            avatar_url = service.get_avatar_urls(request, user, 48)[b'1x']
        else:
            avatar_url = None
        return {b'avatar_url': avatar_url, 
           b'id': user.id, 
           b'fullname': user.get_full_name(), 
           b'username': user.username}
    else:
        return
        return


class ConfigureView(View):
    """The basic "Configure" page for Review Bot."""
    template_name = b'reviewbot/configure.html'

    def get(self, request):
        """Render and return the admin page.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

        Returns:
            django.http.HttpResponse:
            The response.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        extension = ReviewBotExtension.instance
        user = get_object_or_none(User, pk=extension.settings.get(b'user'))
        return render(request, self.template_name, {b'extension': extension, 
           b'reviewbot_user': user})

    def post(self, request):
        """Save the extension configuration.

        Args:
            request (django.http.HttpRequest):
                The HTTP request, including POSTed data.

        Returns:
            django.http.HttpResponse:
            The response. The body of the response is a JSON-encoded blob which
            indicates success or failure, and in the success case, includes the
            the current configuration.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        extension = ReviewBotExtension.instance
        should_save = False
        new_user = request.POST.get(b'reviewbot_user')
        if new_user:
            try:
                user = User.objects.get(pk=new_user)
            except User.DoesNotExist:
                return HttpResponseBadRequest(json.dumps({b'result': b'error', 
                   b'field': b'user', 
                   b'error': b'The specified user does not exist.'}), content_type=b'application/json')

            extension.settings[b'user'] = user.pk
            should_save = True
        else:
            user = get_object_or_none(User, pk=extension.settings.get(b'user'))
        if b'reviewbot_broker_url' in request.POST:
            broker_url = request.POST[b'reviewbot_broker_url']
            extension.settings[b'broker_url'] = broker_url
            should_save = True
        else:
            broker_url = extension.settings.get(b'broker_url', b'')
        if should_save:
            extension.settings.save()
        return HttpResponse(json.dumps({b'result': b'success', 
           b'broker_url': broker_url, 
           b'user': _serialize_user(request, user)}), content_type=b'application/json')


class ConfigureUserView(View):
    """An endpoint for setting the user for Review Bot."""

    def get(self, request):
        """Return the configured user.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

        Returns:
            django.http.HttpResponse:
            A response containing the currently-configured user.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        extension = ReviewBotExtension.instance
        user = get_object_or_404(User, pk=extension.settings.get(b'user'))
        return HttpResponse(json.dumps(_serialize_user(request, user)), content_type=b'application/json')

    def post(self, request):
        """Create a new user for Review Bot.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

        Returns:
            django.http.HttpResponse:
            A response containing the newly-configured user.
        """
        if not request.user.is_superuser:
            return self.get_no_access_error(request)
        siteconfig = SiteConfiguration.objects.get_current()
        noreply_email = siteconfig.get(b'mail_default_from')
        extension = ReviewBotExtension.instance
        try:
            with transaction.atomic():
                user = User.objects.create(username=b'reviewbot', email=noreply_email, first_name=b'Review', last_name=b'Bot')
                profile = user.get_profile()
                profile.should_send_email = False
                profile.save()
                avatar_service = avatar_services.get_avatar_service(URLAvatarService.avatar_service_id)
                extension = ReviewBotExtension.instance
                avatar_service.setup(user, {b'1x': extension.get_static_url(b'images/reviewbot.png'), 
                   b'2x': extension.get_static_url(b'images/reviewbot@2x.png')})
        except IntegrityError:
            return HttpResponseBadRequest()

        extension.settings[b'user'] = user.pk
        extension.settings.save()
        return HttpResponse(json.dumps(_serialize_user(request, user)), content_type=b'application/json')


class WorkerStatusView(View):
    """An "API" to get worker status.

    This view is an internal API to query the workers and return their status.
    """

    def get(self, request):
        """Query workers and return their status.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

        Returns:
            django.http.HttpResponse:
            The response.
        """
        extension = ReviewBotExtension.instance
        response = {}
        if extension.is_configured:
            try:
                payload = {b'session': extension.login_user(), 
                   b'url': get_server_url()}
                reply = extension.celery.control.broadcast(b'update_tools_list', payload=payload, reply=True, timeout=10)
                response = {b'state': b'success', 
                   b'hosts': [ {b'hostname': hostname.split(b'@', 1)[1], b'tools': data[b'tools']} for item in reply for hostname, data in six.iteritems(item)
                           ]}
            except IOError as e:
                response = {b'state': b'error', 
                   b'error': b'Unable to connect to broker: %s.' % e}

        else:
            response = {b'state': b'error', 
               b'error': b'Review Bot is not yet configured.'}
        return HttpResponse(json.dumps(response), content_type=b'application/json')