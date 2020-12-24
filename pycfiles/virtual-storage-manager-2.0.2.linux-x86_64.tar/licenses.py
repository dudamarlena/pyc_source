# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/v1/licenses.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api.openstack import wsgi
from vsm.api import xmlutil
from vsm import flags
from vsm.openstack.common import log as logging
from vsm.api.views import license as license_views
from vsm import conductor
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

def make_license(elem, detailed=False):
    elem.set('license_accept')
    if detailed:
        pass


license_nsmap = {None: xmlutil.XMLNS_V11, 'atom': xmlutil.XMLNS_ATOM}

class LicenseTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('license', selector='license')
        make_license(root, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=license_nsmap)


class LicensesTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('licenses')
        elem = xmlutil.SubTemplateElement(root, 'licenses', selector='licenses')
        make_license(elem, detailed=True)
        return xmlutil.MasterTemplate(root, 1, nsmap=license_nsmap)


class LicenseController(wsgi.Controller):
    """The License controller for the OpenStack API."""
    _view_builder_class = license_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(LicenseController, self).__init__()

    def license_status_get(self, req):
        context = req.environ['vsm.context']
        ret = self.conductor_api.license_status_get(context)
        return ret

    def license_status_create(self, req, body=None):
        context = req.environ['vsm.context']
        kargs = {'id': 1, 'license_accept': body['value']}
        ret = self.conductor_api.license_status_create(context, values=kargs)
        return ret

    def license_status_update(self, req, body=None):
        context = req.environ['vsm.context']
        value = body['value']
        ret = self.conductor_api.license_status_update(context, value)
        return ret


def create_resource(ext_mgr):
    return wsgi.Resource(LicenseController(ext_mgr))