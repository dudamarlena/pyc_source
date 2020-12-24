# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/user_data.py
# Compiled at: 2019-02-06 12:21:52
import functools, ocs.api.decorators, slumber
from flask import request
from flask_classy import route
from ocs.api import exports
from ocs.api.clients import ComputeAPIClient
from ocs.api.exceptions import NotFound
from ocs.api.validators import Validator
from ocs.conf import build_object_from_conf
from . import CONFIGURATION_NAME, MetadataAPIBaseView, client_ip

def only_for_root(decorated):
    """ Limit user data to root user, who is the only user that can bind to a
    source port below 1024.
    """

    @functools.wraps(decorated)
    def wrapped(*args, **kwargs):
        local_port = request.environ.get('REMOTE_PORT')
        if local_port is None:
            return ('uwsgi variable REMOTE_PORT must be set to the client port', 500)
        else:
            if int(local_port) >= 1024:
                return ('# For security reason, you need to query user data with a source port below 1024. For instance, with curl, run as root: # curl http://169.254.42.42/user_data/... --local-port 1-1023\n',
                        403)
            return decorated(*args, **kwargs)

    return wrapped


class UserDataView(MetadataAPIBaseView):
    route_base = '/user_data'
    decorators = MetadataAPIBaseView.decorators + [
     exports.select_export(default='sh'),
     only_for_root]

    def index(self):
        server = self._get_server_by_ip(client_ip())
        response = self.privileged_compute_api.query().servers(server['id']).user_data.get()
        return response

    def delete(self, key):
        server = self._get_server_by_ip(client_ip())
        response = self.privileged_compute_api.query().servers(server['id']).user_data(key).delete()
        return ({}, 204)


class TextPlainSerializer(slumber.serialize.BaseSerializer):
    """ Slumber only implements a JSON and a YAML serializers.
    TextPlainSerializer helps to query API endpoints that require the content
    type to be text/plain.
    """
    key = 'plain'
    content_types = ['text/plain']

    def get_content_type(self):
        return self.content_types[0]

    def dumps(self, data):
        return data


class CustomPrivilegedComputeAPIClient(ComputeAPIClient):
    """ The compute API endpoint PATCH /servers/:id/user_data expects to
    receive a text/plain content type.

    Ideally, we should:

    1/ add the TextPlainSerializer to the serializers of slumber
    2/ set the content type of the request to text/plain to let slumber choose
       the right serializer

    Because of the bad design of slumber, there's no way to set a per-request
    content-type so the 2/ is impossible.

    CustomPrivilegedComputeAPIClient is a regular compute privileged API,
    except the query() method - that creates a slumber.API object - is
    overriden to force the serializer to always be a TextPlainSerializer.
    """

    @classmethod
    def build(cls):
        """ Returns an instance of CustomPrivilegedComputeAPIClient.
        """
        return build_object_from_conf(cls, {'auth_token': (
                        CONFIGURATION_NAME,
                        'api-metadata.api-compute.token'), 
           'base_url': (
                      CONFIGURATION_NAME,
                      'api-metadata.api-compute.url',
                      None), 
           'verify_ssl': (
                        CONFIGURATION_NAME,
                        'api-metadata.api-compute.verify_ssl',
                        True)})

    def query(self):
        """ Create a slumber.API object, but force change the default
        serializer.
        """
        return slumber.API(self.get_api_url(), session=self.make_requests_session(), serializer=TextPlainSerializer())


def force_text_plain(decorated):
    """ Decorate a flask view to force the Content-Type header to be
    text/plain.
    """

    @functools.wraps(decorated)
    def wrapped(*args, **kwargs):
        """ The decorated view can return a tuple of 1, 2 or 3 elements.
        """
        ret = decorated(*args, **kwargs)
        if not isinstance(ret, tuple):
            ret = (
             ret,)
        assert len(ret) in (1, 2, 3)
        if len(ret) == 1:
            return ret + (200, {'Content-Type': 'text/plain'})
        if len(ret) == 2:
            return ret + ({'Content-Type': 'text/plain'},)
        ret[2]['Content-Type'] = 'text/plain'
        return ret

    return wrapped


class UserDataRawViewValidator(Validator):

    def validate_patch(self, view, key):
        content_type = request.environ.get('CONTENT_TYPE')
        if content_type != 'text/plain':
            return (
             'Content-Type must be text/plain and not %s' % content_type,
             400)
        return view(key)


class UserDataRawView(MetadataAPIBaseView):
    """ Forwards GET and PATCH requests to /servers/:id/user_data. The compute
    API doesn't expect applications/json but text/plain requests for these
    endpoints, so we need to remove JSON decorators.

    Note we also remove ocs.api.decorators.handle_api_exceptions, because it
    expects its return value to be serialized by ocs.api.decorators.jsonify.
    """
    decorators = [ _dec for _dec in MetadataAPIBaseView.decorators if _dec not in (
     ocs.api.decorators.handle_api_exceptions,
     ocs.api.decorators.jsonify, ocs.api.decorators.validate_json_fmt)
                 ] + [
     force_text_plain, only_for_root]
    route_base = '/user_data'
    validation_class = UserDataRawViewValidator()

    def patch(self, key):
        try:
            server = self._get_server_by_ip(client_ip())
        except NotFound as exc:
            return (
             exc.message, exc.http_status_code)

        data = request.get_data()
        api = CustomPrivilegedComputeAPIClient.build()
        response = api.query().servers(server['id']).user_data(key).patch(data)
        return ('', 204)

    def get(self, key):
        try:
            server = self._get_server_by_ip(client_ip())
        except NotFound as exc:
            return (
             exc.message, exc.http_status_code)

        try:
            response = self.privileged_compute_api.query().servers(server['id']).user_data(key).get()
        except slumber.exceptions.HttpNotFoundError as exc:
            return ('Invalid key', 404)

        return response