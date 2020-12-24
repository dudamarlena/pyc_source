# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/ginsfsm/ginsfsm/scaffolds/__init__.py
# Compiled at: 2013-04-28 08:37:44
import binascii, os
from ginsfsm.compat import native_
from ginsfsm.scaffolds.template import Template

class GinsFSMTemplate(Template):
    """
     A class that can be used as a base class for GinsFSM scaffolding
     templates.
    """

    def pre(self, command, output_dir, vars):
        """ Overrides :meth:`ginsfsm.scaffold.template.Template.pre`, adding
        several variables to the default variables list (including
        ``random_string``, and ``package_logger``).  It also prevents common
        misnamings (such as naming a package "site" or naming a package
        logger "root".
        """
        if vars['package'] == 'site':
            raise ValueError('Sorry, you may not name your package "site". The package name "site" has a special meaning in Python.  Please name it anything except "site".')
        vars['random_string'] = native_(binascii.hexlify(os.urandom(20)))
        package_logger = vars['package']
        if package_logger == 'root':
            package_logger = 'app'
        vars['package_logger'] = package_logger
        return Template.pre(self, command, output_dir, vars)

    def post(self, command, output_dir, vars):
        """ Overrides :meth:`ginsfsm.scaffold.template.Template.post`, to
        print "Welcome to GinsGSM.  Sorry for the convenience." after a
        successful scaffolding rendering."""
        self.out('Welcome to GinsFSM.  Sorry for the convenience.')
        return Template.post(self, command, output_dir, vars)

    def out(self, msg):
        print msg


class MultipleWsgiTemplate(GinsFSMTemplate):
    _template_dir = 'multiple_wsgi'
    summary = 'Create a multiple WSGI proyect.'


class MultiplePyramidWsgiTemplate(GinsFSMTemplate):
    _template_dir = 'multi_pyramid_wsgi'
    summary = 'Create a multiple WSGI proyect with a Pyramid wsgi application.'


class SimpleGObjTemplate(GinsFSMTemplate):
    _template_dir = 'simple_gobj'
    summary = 'Create a simple GObj proyect.'


class SimpleWsgiTemplate(GinsFSMTemplate):
    _template_dir = 'simple_wsgi'
    summary = 'Create a simple WSGI proyect.'


class SimplePyramidTemplate(GinsFSMTemplate):
    _template_dir = 'simple_pyramid'
    summary = 'Create a simple Pyramid proyect, with sockjs server activated.'


class SimpleWebsocketServerTemplate(GinsFSMTemplate):
    _template_dir = 'simple_websocket_server'
    summary = 'Create a simple Websocket Server proyect'