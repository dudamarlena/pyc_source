# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/conf.py
# Compiled at: 2017-11-27 05:10:38
import functools, itertools, arrow
from flask import request
from flask_classy import route
from ocs.api import decorators, exports
from ocs.api.validators import Validator
from . import MetadataAPIBaseView, client_ip, compat

class ConfViewValidator(Validator):

    def validate_conf(self, view):
        return view(client_ip())


def _compat_conf(view):
    """ Decorates /conf to call the export function on the view response.
    """

    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        export_decorator, ret = view(*args, **kwargs)
        flask_response = decorators.jsonify(lambda : ret)()
        return export_decorator(lambda : flask_response)()

    return wrapped


class ConfView(MetadataAPIBaseView):
    route_base = '/'
    validation_class = ConfViewValidator()

    def _server_info(self, ip_addr):
        """ Queries the compute API to get server info that has the IP
        `ip_addr`.
        """
        server = self._get_server_by_ip(ip_addr)
        return (
         {'id': server.get('id'), 
            'name': server.get('name'), 
            'commercial_type': server.get('commercial_type'), 
            'hostname': server.get('hostname'), 
            'tags': server.get('tags'), 
            'state_detail': server.get('state_detail'), 
            'public_ip': server.get('public_ip'), 
            'private_ip': server.get('private_ip'), 
            'volumes': server.get('volumes'), 
            'organization': server.get('organization'), 
            'location': server.get('location', {}), 
            'ipv6': server.get('ipv6'), 
            'extra_networks': server.get('extra_networks'), 
            'bootscript': server.get('bootscript')},
         server)

    def _orga_info(self, server_orga):
        """ Queries the account API to get info about the organization that
        owns a server.
        """
        response = self.privileged_account_api.query().organizations(server_orga).get()
        organization = response.get('organization', {})
        orga_users = organization.get('users', {})
        users_keys = [ user.get('ssh_public_keys', []) or [] for user in orga_users ]
        all_users_keys = list(itertools.chain(*users_keys))
        return {'ssh_public_keys': all_users_keys, 
           'timezone': organization.get('timezone')}

    @_compat_conf
    @route('/conf')
    def conf(self, ip_addr):
        """ Returns client's metadata.

        By default, a "shell format" is returned to the client. For images
        prior to ~2014/11/01, dictionaries were not rendered properly.

        The following dict:

            >>> {'super_dict': {'x': 1, 'y': 2}}

        Used to be rendered as (bad, note the absence of quotes):

            SUPER_DICT=X Y
            SUPER_DICT_X=1
            SUPER_DICT_Y=2

        And now (good):

            SUPER_DICT='X Y'
            SUPER_DICT_X=1
            SUPER_DICT_Y=2

        Do prevent breaking client's scripts using this endpoint, we keep the
        bad behaviour for old images.
        """
        ret, server = self._server_info(ip_addr)
        ret.update(self._orga_info(ret.get('organization')))
        image = server.get('image')
        if image:
            creation_date = arrow.get(image.get('creation_date'))
            limit = arrow.get('2014-11-01T00:00:00+00:00')
            if creation_date < limit:
                return (compat.select_export(default='sh'), ret)
        return (
         exports.select_export(default='sh'), ret)