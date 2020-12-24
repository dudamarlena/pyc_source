# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/BastionX509Generator.py
# Compiled at: 2012-03-06 02:26:51
__doc__ = '$id$'
__version__ = '$Revision: 67 $'[11:-2]
import AccessControl, commands, logging
from array import *
from DateTime import DateTime
from AccessControl.Permissions import view, change_configuration
from OFS.SimpleItem import SimpleItem
try:
    from Products.CMFPlone.PloneFolder import PloneFolder as ObjectManager
except:
    from OFS.ObjectManager import ObjectManager

import os, string, time, atexit
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PythonScripts.standard import structured_text
LOG = logging.getLogger('BastionX509Generator')
manage_addBastionX509GeneratorForm = PageTemplateFile('zpt/add_cert', globals())

def manage_addBastionX509Generator(self, id, title='', directory='/tmp', REQUEST=None):
    """ wrapper for an OpenSSL X509 X509Generator """
    self._setObject(id, BastionX509Generator(id, title, directory))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)
    else:
        return


class BastionX509Generator(ObjectManager, SimpleItem):
    """
    wrapper for an OpenSSL X509 X509Generator 

    derives of ObjectManager to get all the App.Management mgmt tab stuff ...
    """
    meta_type = portal_type = 'BastionX509Generator'
    do_pks12 = False
    _properties = ObjectManager._properties + ({'id': 'directory', 'type': 'string', 'mode': 'w'}, {'id': 'dont_transmit', 'type': 'boolean', 'mode': 'w'})
    manage_options = ({'label': 'Generate', 'action': 'manage_generate'}, {'label': 'View', 'action': ''}, {'label': 'Format', 'action': 'manage_format'}, {'label': 'Properties', 'action': 'manage_propertiesForm'}) + SimpleItem.manage_options
    __ac_permissions__ = (
     (
      view, ('manage_generate', 'manage_format', 'generate', 'format', 'downloadOptions')),)

    def __init__(self, id, title='', directory='/tmp', dont_transmit=0):
        self.id = id
        self.title = title
        self.directory = directory
        self.dont_transmit = dont_transmit

    manage_generate = PageTemplateFile('zpt/generate_cert', globals())
    manage_format = PageTemplateFile('zpt/x509formatter', globals())

    def generate(self, passphrase1, passphrase2, city, province, country, company, division, email, cn, expires, size, output=2, pwd1='', pwd2='', REQUEST=None):
        """ go generate the key, defaulted to PEM-only format (BastionSecureApache friendly ...) """
        if output in ('1', '3'):
            if pwd1 == '' or pwd2 == '':
                if REQUEST:
                    REQUEST.set('manage_tabs_message', 'A password is required for PKCS12 generation.')
                    return self.manage_generate(self, REQUEST)
                raise AttributeError, 'A password is required for PKCS12 generation.'
            if pwd1 != pwd2:
                if REQUEST:
                    REQUEST.set('manage_tabs_message', "Passwords don't match.")
                    return self.manage_generate(self, REQUEST)
                raise AttributeError, 'A password is required for PKCS12 generation.'
        if output in ('1', 1):
            files = ('x509.key', 'x509.keydec', 'x509.pub', 'x509.crt', 'x509.req',
                     'x509.p12')
        elif output in ('2', 2, ''):
            files = ('x509.key', 'x509.keydec', 'x509.pub', 'x509.crt', 'x509.req')
        elif output in ('3', 3):
            files = ('x509.p12', )
        else:
            if REQUEST:
                REQUEST.set('manage_tabs_message', 'Output parameter must be 1-3!')
                return self.manage_generate(self, REQUEST)
            raise AttributeError, 'Output parameter must be 1-3!'
        if len(passphrase1) < 5:
            if REQUEST:
                REQUEST.set('manage_tabs_message', 'Passphrase must be at least 5 characters.')
                return self.manage_generate(self, REQUEST)
            raise AttributeError, 'Passphrase must be at least 5 characters.'
        if not passphrase1 == passphrase2:
            if REQUEST:
                REQUEST.set('manage_tabs_message', 'Passphrase does not match.')
                return self.manage_generate(self, REQUEST)
            raise AttributeError, 'Passphrase does not match.'
        if self.dont_transmit:
            dir = self.directory
        else:
            if not REQUEST:
                REQUEST = self.REQUEST
            dir = '%s/%s' % (self.directory, REQUEST.SESSION.getId())
        try:
            os.mkdir(dir)
        except:
            pass

        command = "mkdir -p %s && %s/x509.exp %s/x509 '%s' '%s' '%s' %s '%s' '%s' %s '%s' %s %s 2>/dev/null" % (dir, os.path.dirname(__file__), dir, passphrase1, city, province, country, company, division, email, cn, expires, size)
        LOG.debug(command)
        (status, output) = commands.getstatusoutput(command)
        for file in files:
            if not os.access('%s/%s' % (dir, file), os.F_OK) or not os.stat('%s/%s' % (dir, file))[6] > 0:
                if REQUEST:
                    REQUEST.set('manage_tabs_message', structured_text('Keys not created (missing %s)!' % file))
                    return self.manage_generate(self, REQUEST)
                raise IOError, 'keys not created (missing %s)' % file

        if self.dont_transmit:
            if REQUEST:
                REQUEST.set('manage_tabs_message', 'keys written')
                return self.manage_generate(self, REQUEST)
            return 0
        if not REQUEST:
            REQUEST = self.REQUEST
        syscall = os.popen('cd %s && tar cf - %s && rm -rf %s' % (dir, string.join(files, ' '), dir), 'r')
        REQUEST.RESPONSE.setHeader('Content-Type', 'application/x-tar')
        REQUEST.RESPONSE.setHeader('Content-Disposition', 'inline; filename=x509.tar')
        REQUEST.RESPONSE.write(syscall.read())
        syscall.close()
        return 0

    def format(self, inform, outform, key_file, REQUEST):
        """
        utility to format certificate for different purposes...
        """
        filename = '%s/%s' % (self.directory, REQUEST.SESSION.getId())
        file = open(filename, 'w')
        file.write(key_file.read())
        file.close()
        command = 'openssl x509 -in %s -inform %s -out %s.x509 -outform %s' % (
         filename, inform, filename, outform)
        (stdin, stdouterr) = os.popen4(command, 'r')
        rc = stdouterr.read()
        stdin.close()
        stdouterr.close()
        if os.access('%s.x509' % filename, os.F_OK) and os.stat('%s.x509' % filename)[6] > 0:
            file = open('%s.x509' % filename, 'r')
            REQUEST.RESPONSE.setHeader('Content-Type', 'application/octetstream')
            REQUEST.RESPONSE.write(file.read())
            file.close()
            os.unlink(filename)
            os.unlink('%s.x509' % filename)
            return 0
        REQUEST.set('manage_tabs_message', structured_text('Error formatting certificate - the problem may be highlighted below\n:%s' % rc))
        return self.manage_format(self, REQUEST)

    def _getPortalTypeName(self):
        """
        needed for the portal type view mechanism ...
        """
        return self.meta_type

    def downloadOptions(self):
        """
        returns a list of tuples of supported download options
        """
        if self.do_pks12:
            return (('All', 1), ('PEM Keys only', 2), ('PKCS12 only', 3))
        else:
            return (('PEM Keys only', 2), )


AccessControl.class_init.InitializeClass(BastionX509Generator)