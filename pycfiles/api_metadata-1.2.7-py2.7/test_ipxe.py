# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/views/test_ipxe.py
# Compiled at: 2019-02-06 12:21:52
from api_metadata.tests.case import APITestCase
from ocs.object_store import cp_backend
from ocs.object_store.cp_backend import ConfiguredEngine as ComputeEngine
from ocs.object_store.cp_backend.unittest import sources as cp_sources

class TestIPXE(APITestCase):

    def test_server_bootscript(self):
        """ Server with a bootscript.
        """
        bootscript = cp_sources.BootscriptFactory()
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(bootscript=bootscript)
        session = cp_sources.SessionFactory(node=node, server=server)
        response = self.client.get('ipxe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])
        self.assertIn('#!ipxe', response.data)
        self.assertIn('kernel %s' % bootscript.kernel, response.data)
        self.assertIn('initrd %s' % bootscript.initrd, response.data)

    def test_server_bootscript_c2_replace_linux_common(self):
        """ Server with a bootscript.
        """
        bootcmdargs = 'LINUX_COMMON args'
        bootscript = cp_sources.BootscriptFactory(bootcmdargs=bootcmdargs)
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(bootscript=bootscript, commercial_type='C2S')
        cp_sources.SessionFactory(node=node, server=server)
        response = self.client.get('ipxe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])
        self.assertIn('#!ipxe', response.data)
        self.assertIn('kernel %s showopts console=ttyS1,9600n8 nousb vga=0 root=/dev/nbd0 args' % bootscript.kernel, response.data)
        self.assertIn('initrd %s' % bootscript.initrd, response.data)

    def test_server_bootscript_vc_replace_linux_common(self):
        """ Server with a bootscript.
        """
        bootcmdargs = 'LINUX_COMMON args'
        bootscript = cp_sources.BootscriptFactory(bootcmdargs=bootcmdargs)
        node = cp_sources.VMNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(bootscript=bootscript, commercial_type='VC1S')
        cp_sources.SessionFactory(node=node, server=server)
        response = self.client.get('ipxe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])
        self.assertIn('#!ipxe', response.data)
        self.assertIn('kernel %s initrd=initrd showopts console=ttyS0,115200 nousb vga=0 root=/dev/vda args' % bootscript.kernel, response.data)
        self.assertIn('initrd %s' % bootscript.initrd, response.data)

    def test_image_bootscript(self):
        """ Server with an image having a default bootscript.
        """
        bootscript = cp_sources.BootscriptFactory()
        image = cp_sources.ImageFactory(default_bootscript=bootscript)
        server = cp_sources.ServerFactory(image=image)
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        session = cp_sources.SessionFactory(node=node, server=server)
        response = self.client.get('ipxe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])
        self.assertIn('#!ipxe', response.data)
        self.assertIn('kernel %s' % bootscript.kernel, response.data)
        self.assertIn('initrd %s' % bootscript.initrd, response.data)

    def test_server_rescue_mode(self):
        """ Server with rescue boot_type.
        """
        krnl = 'rescue me'
        initrd = 'jack'
        bootscript = cp_sources.BootscriptFactory(public=True, architecture='arm', title='armv7l Rescue', kernel=krnl, initrd=initrd)
        session = ComputeEngine.scoped_session()
        session.add(bootscript)
        session.commit()
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(boot_type='rescue')
        session = cp_sources.SessionFactory(node=node, server=server)
        response = self.client.get('ipxe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])
        self.assertIn('#!ipxe', response.data)
        self.assertIn('kernel %s' % krnl, response.data)
        self.assertIn('initrd %s' % initrd, response.data)