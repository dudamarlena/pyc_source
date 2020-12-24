# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/ipxe.py
# Compiled at: 2019-02-06 12:21:57
from flask import current_app
from jinja2 import Environment, PackageLoader
from ocs.api.exceptions import NotFound
from . import MetadataAPIBaseView, client_ip

class IPXEView(MetadataAPIBaseView):
    """ Generates the iPXE configuration for a client.

    At the moment, bootscripts aren't tied to an architecture. A C1 (arm)
    server could generate its iPXE configuration - which is useless ; and a C2
    server could use a C1 bootscript - but it won't boot.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SECURITY NOTE: we must be extra cautious and not let the kernel, initrd and
    bootcmdargs be user defined without validation.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    route_base = '/'

    def _get_rescue_bootscript(self, arch):
        response = self.privileged_compute_api.query().bootscripts.get(arch=arch, title='rescue', public='true')
        bootscripts = response.get('bootscripts', [])
        if len(bootscripts) == 0:
            raise NotFound('No rescue bootscript for %s' % arch)
        if len(bootscripts) > 1:
            raise NotFound('More than one rescue bootscript for %s' % arch)
        return bootscripts[0]

    def ipxe(self):
        ip_addr = client_ip()
        server = self._get_server_by_ip(ip_addr)
        server_boot_type = server.get('boot_type')
        if server_boot_type == 'rescue':
            bootscript = self._get_rescue_bootscript(server.get('arch'))
        else:
            bootscript = server.get('bootscript')
        if bootscript is None:
            image = server.get('image')
            if image:
                bootscript = image.get('default_bootscript')
        if bootscript is None:
            return current_app.response_class('Bootscript not found', status=404, mimetype='text/plain')
        else:
            module_name = ('.').join(__name__.split('.')[:-1])
            jinja_env = Environment(loader=PackageLoader(module_name, 'templates'))
            template = jinja_env.get_template('boot.ipxe')
            bootcmdargs = bootscript.get('bootcmdargs', '')
            commercial_type = server['commercial_type']
            if commercial_type.startswith('VC') or commercial_type.startswith('ST') or commercial_type.startswith('X64') or commercial_type.startswith('ARM') or commercial_type.startswith('RENDER'):
                bootcmdargs = bootcmdargs.replace('LINUX_COMMON', 'initrd=initrd showopts console=ttyS0,115200 nousb vga=0 root=/dev/vda')
                if commercial_type.startswith('ARM'):
                    bootcmdargs = bootcmdargs.replace('ttyS0', 'ttyAMA0')
            elif commercial_type.startswith('C2'):
                bootcmdargs = bootcmdargs.replace('LINUX_COMMON', 'showopts console=ttyS1,9600n8 nousb vga=0 root=/dev/nbd0')
            result = template.render(kernel=bootscript.get('kernel'), initrd=bootscript.get('initrd'), bootcmdargs=bootcmdargs)
            return current_app.response_class(result, mimetype='text/plain')