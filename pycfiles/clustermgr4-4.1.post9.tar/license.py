# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/data/projects/gluu/cluster-mgr/clustermgr/core/license.py
# Compiled at: 2020-05-09 08:47:08
import ConfigParser, json, os, time
from datetime import datetime
from datetime import timedelta
from functools import wraps
import requests
from flask import _app_ctx_stack
from flask import flash
from flask import g as fg
from flask import redirect
from flask import url_for
from flask import current_app
from flask import request
from clustermgr.core.utils import exec_cmd
from clustermgr.core.utils import get_mac_addr

def current_date_millis():
    """Gets Unix timestamp in milliseconds.

    :returns: An integer of Unix timestamp in milliseconds.
    """
    return int(time.time() * 1000)


class LicenseManager(object):

    def __init__(self, app=None, redirect_endpoint=''):
        self.redirect_endpoint = redirect_endpoint
        self.app = app
        if app:
            self.init_app(app, redirect_endpoint)

    def init_app(self, app, redirect_endpoint):
        self.app = app
        self.redirect_endpoint = redirect_endpoint
        app.config.setdefault('LICENSE_CONFIG_FILE', '/usr/share/oxlicense-validator/license.ini')
        app.config.setdefault('LICENSE_SIGNED_FILE', '/usr/share/oxlicense-validator/signed_license')
        app.config.setdefault('LICENSE_VALIDATOR', '/usr/share/oxlicense-validator/oxlicense-validator.jar')
        app.config.setdefault('LICENSE_PRODUCT_NAME', 'cluster_manager')
        app.config.setdefault('LICENSE_ENFORCEMENT_ENABLED', True)
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['license_manager'] = self

    def license_required(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            app = self._get_app()
            if app.config['LICENSE_ENFORCEMENT_ENABLED']:
                license_data, err = self.validate_license()
                now = current_date_millis()
                invalid = license_data['valid'] is not True
                expired = now > license_data['metadata'].get('expiration_date')
                inactive = license_data['metadata'].get('active', False) is False
                if err or invalid or expired or inactive:
                    flash('The previously requested URL requires a valid license. Please make sure you have a valid license.', 'warning')
                    if not self.redirect_endpoint:
                        redirect_url = '/'
                    else:
                        redirect_url = url_for(self.redirect_endpoint)
                    return redirect(redirect_url)
            return func(*args, **kwargs)

        return wrapper

    def _get_app(self):
        if self.app:
            return self.app
        ctx = _app_ctx_stack.top
        if ctx:
            return ctx.app
        raise RuntimeError('application not registered on license_manager instance and no application bound to current context')

    def validate_license(self):
        """Validates the license.

        The process involves 3 steps:
        1. load the license settings to get the config needed for next steps
        2. get the signed license
        3. decode the signed license to extract its data

        :returns: A tuple of the data and error message from validation process.
        """
        license_data = {'valid': False, 'metadata': {}}
        err = ''
        cfg = self.load_license_config()
        signed_license, err = self.get_signed_license(cfg.get('license_id'))
        if err:
            return (license_data, err)
        license_data, err = self.decode_signed_license(signed_license, cfg.get('public_key'), cfg.get('public_password'), cfg.get('license_password'))
        if err:
            err = 'Your license is invalid. Try again, or contact sales@gluu.org for assistance.'
        return (
         license_data, err)

    def dump_license_config(self, data):
        """Writes a config file.

        Example of config file contents:

            [license]
            license_id = 1
            license_password = lpasswd
            public_password = ppasswd
            public_key = pkey
            accepted = true

        :param data: A ``dict`` of data to save to config file.
        """
        section = 'license'
        options = ('license_id', 'license_password', 'public_password', 'public_key',
                   'accepted')
        parser = ConfigParser.SafeConfigParser()
        parser.add_section(section)
        for opt, val in data.iteritems():
            if opt not in options:
                continue
            parser.set(section, opt, val)

        app = self._get_app()
        with open(app.config['LICENSE_CONFIG_FILE'], 'wb') as (fw):
            parser.write(fw)

    def load_license_config(self):
        """Reads the config file and extract the data.

        :returns: A ``dict`` of configuration items.
        """
        app = self._get_app()
        parser = ConfigParser.SafeConfigParser()
        parser.read(app.config['LICENSE_CONFIG_FILE'])
        try:
            cfg = dict(parser.items('license'))
        except ConfigParser.NoSectionError:
            cfg = {}

        return cfg

    def get_signed_license(self, license_id):
        """Gets signed license either from file. If it can't get the signed
        license from a file, download it first.

        :param license_id: License ID.
        """
        err = ''
        sig = ''
        app = self._get_app()
        if not os.path.isfile(app.config['LICENSE_SIGNED_FILE']):
            resp = requests.post('https://license.gluu.org/oxLicense/rest/generate', data={'licenseId': license_id, 
               'count': 1, 
               'macAddress': get_mac_addr()}, verify=True)
            if resp.ok:
                sig = resp.json()[0]['license']
            else:
                err = resp.text
            with open(app.config['LICENSE_SIGNED_FILE'], 'w') as (fw):
                fw.write(sig)
            return (sig, err)
        with open(app.config['LICENSE_SIGNED_FILE']) as (fr):
            return (
             fr.read(), err)

    def decode_signed_license(self, signed_license, public_key, public_password, license_password):
        """Decodes signed license.

        Signed license is encoded using Java object serialization, hence
        we need external program to decode it.

        :param signed_license: Encoded signed license.
        :param public_key: Public key needed to validate the license.
        :param public_password: Public password needed to validate the license.
        :param license_password: License password needed to validate
                                 the license.
        :param product: Product name as defined in license.
        :returns: A tuple of ``dict`` contains license data and
                  error message (if any).
        """
        app = self._get_app()
        data = {'valid': False, 'metadata': {}}
        if public_key:
            public_key = public_key.replace(' ', '').replace('\n', '')
        cmd = ('java -jar {} {} {} {} {} {} {}').format(app.config['LICENSE_VALIDATOR'], signed_license, public_key, public_password, license_password, app.config['LICENSE_PRODUCT_NAME'], current_date_millis())
        out, err, code = exec_cmd(cmd)
        if code != 0:
            return (data, err)
        meta = out.splitlines()[(-1)]
        data = json.loads(meta)
        return (data, err)


license_manager = LicenseManager()

def license_reminder():
    """Sets human-readable expiration date.

    The value will be stored in ``flask.g`` object, so template can
    obtain the value.
    """
    if not current_app.config['LICENSE_ENFORCEMENT_ENABLED']:
        return
    msg = ''
    license_data, _ = license_manager.validate_license()
    exp_date = license_data['metadata'].get('expiration_date')
    if exp_date:
        exp_date = datetime.utcfromtimestamp(int(exp_date) / 1000)
        exp_date_str = exp_date.strftime('%Y-%m-%d %H:%M:%S')
        exp_threshold = exp_date - timedelta(days=90)
        now = datetime.utcfromtimestamp(current_date_millis() / 1000)
        if now > exp_date:
            msg = ('Your license has been expired since {} GMT.').format(exp_date_str)
            current_app.jinja_env.globals['evaluation_period'] = 'Your license has expired. Contact sales@gluu.org to renew your license.'
        elif now > exp_threshold:
            msg = ('Your license will be expired at {} GMT.').format(exp_date_str)
    fg.license_reminder_msg = msg


def prompt_license():
    if not current_app.config['LICENSE_ENFORCEMENT_ENABLED']:
        return
    if request.endpoint == 'license.prompt':
        return
    cfg = license_manager.load_license_config()
    if cfg.get('accepted', 'false').lower() == 'true':
        return
    return redirect(url_for('license.prompt'))


def license_required():
    if not current_app.config['LICENSE_ENFORCEMENT_ENABLED']:
        return
    license_data, err = license_manager.validate_license()
    aday = 86400
    if not license_data['valid']:
        dot_start = os.path.join(current_app.config['DATA_DIR'], '.start')
        if not os.path.exists(dot_start):
            with open(dot_start, 'w') as (w):
                w.write(str(int(time.time())))
        start_time = time.time() - 31 * aday
        try:
            with open(dot_start) as (f):
                start_time = int(f.read().strip())
        except:
            pass

        date_left = (30 * aday - (time.time() - start_time)) // aday
        if date_left <= 0:
            current_app.jinja_env.globals['evaluation_period'] = 'Your evaluation version EXPIRED. To get a license, please contact sales@gluu.org.'
            return redirect(url_for('license.settings'))
        current_app.jinja_env.globals['evaluation_period'] = ('Thanks for trying Cluster Manager! Your evaluation period expires in {} days. Contact sales@gluu.org to purchase a license.').format(int(date_left))
        return
    now = current_date_millis()
    invalid = license_data['valid'] is not True
    expired = now > license_data['metadata'].get('expiration_date')
    inactive = license_data['metadata'].get('active', False) is False
    license_date_left = (60 * aday - (time.time() - license_data['metadata'].get('expiration_date', 0) / 1000)) // aday
    if license_date_left <= 60:
        current_app.jinja_env.globals['evaluation_period'] = ('Your license will expire in {x} days. Contact sales@gluu.org to renew your license.').format(int(license_date_left))
    if any([err, invalid, expired, inactive]):
        flash(('The previously requested URL ({}) requires a valid license. Please make sure you have a valid license.').format(request.url), 'warning')
        return redirect(url_for('license.index'))