# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/docs/settings.py
# Compiled at: 2017-01-30 10:34:06
# Size of source mod 2**32: 8014 bytes
"""
Set-up for ini documentation list of dicts

In the ini_doc list, only use 'yes' or 'no' for the required field,
as this is used in the code to check if all required settings are set.
"""
from spynl.main.exceptions import SpynlException
ini_description = '\nThese are the settings that can be added to the ini file under the heading\n[app:main]. This table only lists settings specific to Spynl. Pyramid settings\nand Pyramid Mail configuration should also be put in [app:main], but are not\nlisted here.  Spynl will not start if one of the required settings is not\npresent in the ini file. <br>\nThe pyramid asbool function returns the boolean value True if the case-lowered\nvalue of string input s is any of t, true, y, on, or 1, otherwise return the\nboolean value False. If s is the value None, return False. If s is already one\nof the boolean values True or False, return it. <br>\nN.B. It is not possible to add comments after the setting,\ncomments should be on their own line.\n'
ini_doc = [
 {'name': 'spynl.date_systemtz', 
  'plugin': '', 
  'required': 'no', 
  'default': 'UTC', 
  'info': 'Timezone that is used if no time zone is explicitly given and also no time zone is found in or to be used from the user object.'},
 {'name': 'spynl.date_format', 
  'plugin': '', 
  'required': 'no', 
  'default': '%Y-%m-%dT%H:%M:%S%z', 
  'info': 'Format for dates.'},
 {'name': 'spynl.languages', 
  'plugin': '', 
  'required': 'no', 
  'default': 'en', 
  'info': 'A csv string describing the languages supported by the application. Spynl has no dialect support, so only two-letter language codes should be provided. The first language is considered to be the preferred language.'},
 {'name': 'spynl.domain', 
  'plugin': '', 
  'required': 'no', 
  'default': 'localhost', 
  'info': 'Used for setting the cookie-domain, and for a default no-reply emailaddress.'},
 {'name': 'spynl.languages', 
  'plugin': '', 
  'required': 'no', 
  'default': 'nl', 
  'info': 'Languages (e.g. de,nl) which Spynl should translate to (other than english). This affects how the task <spynl dev.translate> works. Use a comma-separated  list for more than one.'},
 {'name': 'spynl.tld_origin_whitelist', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'Comma-separated whitelist for allowed origins. It is expected to hold only the top-level domains,  e.g. "google.com".'},
 {'name': 'spynl.dev_origin_whitelist', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'Comma separated whitelist for allowed origins which is usable for a development context. It is expected to hold either complete domains or mere protocols, e.g. "chrome-extension://"..'},
 {'name': 'spynl.pretty', 
  'plugin': '', 
  'required': 'no', 
  'default': 'false', 
  'info': 'Pretty printing for development. Is read with Pyramid asbool function.'},
 {'name': 'spynl.session', 
  'plugin': '', 
  'required': 'no', 
  'default': 'Pyramid', 
  'info': 'Sets the name of the session class to use. Spynl will look this class up under settings[<name>]. The class should conform to the interface pyramid.interfaces.ISession. The value "Pyramid" or omitting this setting will result in the use of the Session class from beaker.session'},
 {'name': 'spynl.ops.environment', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The environment Spynl is running in. This is quite useful for things like error log aggregation.'},
 {'name': 'spynl.ops.function', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The function this Spynl node is performing. This can be useful for error log aggregation if you  employ more than one Spynl applications.'},
 {'name': 'spynl.ops.jenkins_url', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The URL of your Jenkins server.'},
 {'name': 'spynl.ops.dev_url', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The URL where your development app can be accessed. Needed to run smoke tests after deploys.'},
 {'name': 'spynl.ops.dev_domain', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The top level domain on which your development app resides. This is used to get the cookie domain correct.'},
 {'name': 'spynl.ops.ecr.dev_tasks', 
  'plugin': '', 
  'required': 'no', 
  'default': 'dev', 
  'info': 'The tasks supported in your development AWS ECR.'},
 {'name': 'spynl.ops.ecr.dev_url', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The URL of your AWS ECR used for development. Include AWS profile name like this: profile@ecr-url.'},
 {'name': 'spynl.ops.ecr.prod_url', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The URL of your AWS ECR used for production. Include AWS profile name like this: profile@ecr-url.'},
 {'name': 'spynl.sentry.key', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The key used to connect to Sentry. Leave empty if you are not using Sentry.'},
 {'name': 'spynl.sentry.project', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The project identifier Spynl reports to in Sentry.'},
 {'name': 'spynl.newrelic.key', 
  'plugin': '', 
  'required': 'no', 
  'default': '', 
  'info': 'The key used to connect to NewRelic. Leave empty if you are not usig NewRelic.'}]

def get_ini_doc_setting(name):
    """
    Returns the documentation entry of a specific setting or None

    Because ini_doc is a list, this function is needed to get the documentation
    of a specific setting.
    """
    for setting in ini_doc:
        if setting['name'] == name:
            return setting


def check_required_settings(config):
    """check whether all required ini settings are set"""
    for setting in ini_doc:
        if setting['required'] == 'yes' and setting['name'] not in config.registry.settings:
            msg = 'Please set {} in the Pyramid ini file'.format(setting['name'])
            raise SpynlException(msg)
        if setting['required'] not in ('no', 'yes'):
            msg = 'The value for required in ini_doc can only be yes or no, please change this for setting: {}'.format(setting['name'])
            raise SpynlException(msg)