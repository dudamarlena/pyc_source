# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/contrib/services.py
# Compiled at: 2016-06-13 14:11:03
import webob.exc
from vsm.api import extensions
from vsm.api.openstack import wsgi
from vsm.api import xmlutil
from vsm import db
from vsm import exception
from vsm.openstack.common import log as logging
from vsm.openstack.common import timeutils
from vsm import utils
LOG = logging.getLogger(__name__)
authorize = extensions.extension_authorizer('storage', 'services')

class ServicesIndexTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('services')
        elem = xmlutil.SubTemplateElement(root, 'service', selector='services')
        elem.set('binary')
        elem.set('host')
        elem.set('zone')
        elem.set('status')
        elem.set('state')
        elem.set('update_at')
        return xmlutil.MasterTemplate(root, 1)


class ServicesUpdateTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('host')
        root.set('host')
        root.set('service')
        root.set('disabled')
        return xmlutil.MasterTemplate(root, 1)


class ServiceController(object):

    @wsgi.serializers(xml=ServicesIndexTemplate)
    def index(self, req):
        """
        Return a list of all running services. Filter by host & service name.
        """
        context = req.environ['vsm.context']
        authorize(context)
        now = timeutils.utcnow()
        services = db.service_get_all(context)
        host = ''
        if 'host' in req.GET:
            host = req.GET['host']
        service = ''
        if 'service' in req.GET:
            service = req.GET['service']
        if host:
            services = [ s for s in services if s['host'] == host ]
        if service:
            services = [ s for s in services if s['binary'] == service ]
        svcs = []
        for svc in services:
            delta = now - (svc['updated_at'] or svc['created_at'])
            alive = abs(utils.total_seconds(delta))
            art = alive and 'up' or 'down'
            active = 'enabled'
            if svc['disabled']:
                active = 'disabled'
            svcs.append({'binary': svc['binary'], 'host': svc['host'], 'zone': svc['availability_zone'], 
               'status': active, 
               'state': art, 'updated_at': svc['updated_at']})

        return {'services': svcs}

    @wsgi.serializers(xml=ServicesUpdateTemplate)
    def update(self, req, id, body):
        """Enable/Disable scheduling for a service"""
        context = req.environ['vsm.context']
        authorize(context)
        if id == 'enable':
            disabled = False
        else:
            if id == 'disable':
                disabled = True
            else:
                raise webob.exc.HTTPNotFound('Unknown action')
            try:
                host = body['host']
                service = body['service']
            except (TypeError, KeyError):
                raise webob.exc.HTTPBadRequest()

            try:
                svc = db.service_get_by_args(context, host, service)
                if not svc:
                    raise webob.exc.HTTPNotFound('Unknown service')
                db.service_update(context, svc['id'], {'disabled': disabled})
            except exception.ServiceNotFound:
                raise webob.exc.HTTPNotFound('service not found')

        return {'host': host, 'service': service, 'disabled': disabled}


class Services(extensions.ExtensionDescriptor):
    """Services support"""
    name = 'Services'
    alias = 'os-services'
    namespace = 'http://docs.openstack.org/storage/ext/services/api/v2'
    updated = '2012-10-28T00:00:00-00:00'

    def get_resources(self):
        resources = []
        resource = extensions.ResourceExtension('os-services', ServiceController())
        resources.append(resource)
        return resources