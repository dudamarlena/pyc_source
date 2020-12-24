# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nick/Dev/mopidy-dev/mopidy-websettings/mopidy_websettings/__init__.py
# Compiled at: 2018-01-14 08:42:35
from __future__ import unicode_literals
import logging, os, sys
from configobj import ConfigObj, ConfigObjError
import jinja2
from mopidy import config, ext
import tornado.web
__version__ = b'0.2.2'
logger = logging.getLogger(__name__)
spec_file = os.path.join(os.path.dirname(__file__), b'settingsspec.ini')
template_file = os.path.join(os.path.dirname(__file__), b'index.html')

def mask(password):
    return b'*' * len(password)


def is_secret(subitem):
    return subitem.endswith(b'password') or subitem.endswith(b'secret')


def restart_program():
    """
    DOES NOT WORK WELL WITH MOPIDY
    Hack from
    https://www.daniweb.com/software-development/python/code/260268/restart-your-python-program
    to support updating the settings, since mopidy is not able to do that yet
    Restarts the current program
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


class Extension(ext.Extension):
    dist_name = b'Mopidy-WebSettings'
    ext_name = b'websettings'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), b'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema[b'musicbox'] = config.Boolean()
        schema[b'config_file'] = config.String()
        return schema

    def setup(self, registry):
        registry.add(b'http:app', {b'name': b'settings', 
           b'factory': websettings_app_factory})


class WebSettingsRequestHandler(tornado.web.RequestHandler):

    def initialize(self, config):
        self.config_file = config[b'websettings'][b'config_file']

    def get(self):
        templateLoader = jinja2.FileSystemLoader(searchpath=b'/')
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template_file)
        error = b''
        try:
            iniconfig = ConfigObj(self.config_file, configspec=spec_file, file_error=True, encoding=b'utf8')
        except (ConfigObjError, IOError) as e:
            error = b'Could not load ini file! %s' % e
            logger.error(error)

        templateVars = {b'error': error}
        validItems = ConfigObj(spec_file, encoding=b'utf8')
        for item in validItems:
            for subitem in validItems[item]:
                configValue = iniconfig.get(item, {}).get(subitem, None)
                if configValue is not None:
                    if is_secret(subitem):
                        configValue = mask(configValue)
                    itemName = item + b'__' + subitem
                    templateVars[itemName] = configValue

        self.write(template.render(templateVars))
        return


class WebPostRequestHandler(tornado.web.RequestHandler):

    def initialize(self, config):
        self.config_file = config.get(b'websettings')[b'config_file']

    def needs_reboot(self, item, subItem):
        reboot_sections = [
         b'network', b'musicbox']
        restart_subsections = [b'webclient']
        if item in reboot_sections:
            if subItem not in restart_subsections:
                return True
        return False

    def post(self):
        apply_html = b''
        apply_string = b'restart Mopidy'
        status = b''
        try:
            iniconfig = ConfigObj(self.config_file, configspec=spec_file, file_error=True, encoding=b'utf8')
            validItems = ConfigObj(spec_file, encoding=b'utf8')
            for item in validItems:
                for subitem in validItems[item]:
                    itemName = item + b'__' + subitem
                    value = self.get_argument(itemName, default=b'')
                    if value:
                        if is_secret(subitem) and value == mask(value):
                            continue
                        oldItem = iniconfig.setdefault(item, {}).setdefault(subitem, b'')
                        if oldItem != value and self.needs_reboot(item, subitem):
                            apply_string = b'reboot system'
                        iniconfig[item][subitem] = value

            try:
                if iniconfig[b'audio'][b'mixer'] == b'alsamixer':
                    iniconfig[b'alsamixer'][b'enabled'] = b'true'
                else:
                    iniconfig[b'alsamixer'][b'enabled'] = b'false'
                for subitem in [b'client_id', b'client_secret']:
                    iniconfig[b'spotify'][subitem] = iniconfig[b'spotify'][subitem] or iniconfig[b'spotify_web'][subitem]
                    iniconfig[b'spotify_web'][subitem] = iniconfig[b'spotify'][subitem]

            except KeyError as e:
                logger.error(b'Error making config consistent %s', e)

            iniconfig.write()
            status = b'Settings Saved!'
            apply_html = b'<form action="apply" method="post"><input type="submit" name="method" value="Apply changes now (' + apply_string + b')" />'
        except (ConfigObjError, IOError) as e:
            status = b'Could not load ini file! %s' % e
            logger.error(status)

        message = b'<html><body><h1>' + status + b'</h1><p>' + apply_html + b'<br/><br/><a href="/">Home</a><br/></p></body></html>'
        self.write(message)


class WebApplyRequestHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    def post(self):
        method = self.get_argument(b'method', None)
        if method is not None:
            if b'reboot' in method:
                status = b'Rebooting Musicbox system...'
                os.system(b'sudo shutdown -r now')
            elif b'restart' in method:
                status = b'Restarting Mopidy service...'
                os.system(b'sudo /etc/init.d/mopidy restart')
            else:
                status = b'Error while applying ' + method
        logger.info(status)
        message = b'<html><body><h1>' + status + b'</h1><br/><br/><a href="/">Home</a><br/></p></body></html>'
        self.write(message)
        return


class WebRebootRequestHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    def post(self):
        logger.info(b'Halting system')
        os.system(b'sudo shutdown -r now')
        os.system(b'shutdown -r now')


class WebShutdownRequestHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    def post(self):
        logger.info(b'Halting system')
        os.system(b'sudo shutdown -h now')
        os.system(b'shutdown -h now')


def websettings_app_factory(config, core):
    from mopidy.http.handlers import StaticFileHandler
    path = os.path.join(os.path.dirname(__file__), b'js')
    return [
     (
      b'/', WebSettingsRequestHandler, {b'config': config}),
     (
      b'/save', WebPostRequestHandler, {b'config': config}),
     (
      b'/apply', WebApplyRequestHandler),
     (
      b'/reboot', WebRebootRequestHandler),
     (
      b'/shutdown', WebShutdownRequestHandler),
     (
      b'/js/(.*)', StaticFileHandler, {b'path': path})]