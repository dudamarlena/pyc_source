# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/constants.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 5558 bytes
"""
Settings which is able to set from admin by user.
"""
from collections import OrderedDict
from django.utils.safestring import mark_safe
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
CONSTANCE_ADDITIONAL_FIELDS = {'short_str': ['django.forms.fields.CharField', {'required': False}]}
GOOGLE_ANALYTICS_CONSTANCE_CONFIG = (
 ('GOOGLE_ANALYTICS_PROPERTY_ID', ('', 'Every website you track with Google Analytics gets its own property ID.\nYou can find the web property ID on the overview page of your account.\n', 'short_str')),
 (
  'GOOGLE_ANALYTICS_DISPLAY_ADVERTISING',
  (
   False,
   'Display Advertising allows you to view Demographics and Interests reports,\nadd Remarketing Lists and support DoubleClick Campain Manager integration.',
   bool)),
 (
  'GOOGLE_ANALYTICS_SITE_SPEED',
  (
   False,
   mark_safe('Allow you view page load times in the <a href="https://support.google.com/analytics/answer/1205784">Site Speed</a> report.'),
   bool)),
 (
  'GOOGLE_ANALYTICS_ANONYMIZE_IP',
  (
   False,
   mark_safe('<a href="https://support.google.com/analytics/answer/2763052?hl=en">IP Anonymization</a>'),
   bool)),
 (
  'GOOGLE_ANALYTICS_SAMPLE_RATE',
  (
   '',
   mark_safe('<a href="https://developers.google.com/analytics/devguides/collection/gajs/methods/gaJSApiBasicConfiguration#_setsamplerate">Sample Rate </a>'),
   'short_str')),
 (
  'GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE',
  (
   '',
   mark_safe('<a href="https://developers.google.com/analytics/devguides/collection/gajs/methods/gaJSApiBasicConfiguration#_setsitespeedsamplerate">Site Speed Sample Rate</a>\nThe value is a percentage and can be between 0 and 100'),
   'short_str')),
 (
  'GOOGLE_ANALYTICS_SESSION_COOKIE_TIMEOUT',
  (
   '',
   mark_safe('<a href="https://developers.google.com/analytics/devguides/collection/gajs/methods/gaJSApiBasicConfiguration#_setsessioncookietimeout">Session cookie timeout</a> in milliseconds.'),
   'short_str')),
 (
  'GOOGLE_ANALYTICS_VISITOR_COOKIE_TIMEOUT',
  (
   '',
   mark_safe('<a href="https://developers.google.com/analytics/devguides/collection/gajs/methods/gaJSApiBasicConfiguration#_setvisitorcookietimeout">Google Analytics visitor cookie expiration </a>in milliseconds.'),
   'short_str')))
PIWIK_CONSTANCE_CONFIG = (('PIWIK_DOMAIN_PATH', ('', 'URL of your Piwik server. Typically, you’ll have Piwik installed on a subdomain or subdirectory\n (e.g. piwik.your_site.com or www.your_site.com/piwik).', 'short_str')),
                          ('PIWIK_SITE_ID', ('', 'Your Piwik server can track several websites.\n Each website has its site ID (this is the idSite parameter in the query string of your browser’s address bar when you visit the Piwik Dashboard). ', 'short_str')))
DJANGOCMS_GOOGLEMAP_CONSTANCE_CONFIG = (('DJANGOCMS_GOOGLEMAP_API_KEY', ('', 'API key of your project to use Google maps. You can generate key here:\nhttps://developers.google.com/maps/documentation/javascript/get-api-key')), )
MAILCHIMP_CONSTANCE_CONFIG = (('MAILCHIMP_API_KEY', ('', 'API key of your app to synchronize mail lists with MailChimp. More about MailChimp API keys:http://kb.mailchimp.com/integrations/api-integrations/about-api-keys')),
                              ('MAILCHIMP_USERNAME', ('', 'Your username on MailChimp. You can find or change the username in profile settings:https://admin.mailchimp.com/account/profile/')))
CONSTANCE_CONFIG = OrderedDict(GOOGLE_ANALYTICS_CONSTANCE_CONFIG + PIWIK_CONSTANCE_CONFIG + DJANGOCMS_GOOGLEMAP_CONSTANCE_CONFIG + MAILCHIMP_CONSTANCE_CONFIG)
CONSTANCE_CONFIG_FIELDSETS = {'General options':('DJANGOCMS_GOOGLEMAP_API_KEY', ), 
 'Google analytics options':dict(GOOGLE_ANALYTICS_CONSTANCE_CONFIG).keys(), 
 'Piwik options':dict(PIWIK_CONSTANCE_CONFIG).keys(), 
 'Mailchimp options':dict(MAILCHIMP_CONSTANCE_CONFIG).keys()}

def _lazy_constance(constance_name):
    """
    Config from library constance cannot be imported in settings
    because it already need initialized settings. That's why it
    has to be done lazily.
    """

    def get_constance_value():
        from constance import config
        return getattr(config, constance_name)

    class Template:
        __doc__ = "\n        Simple objcet wrapping real value. It's just proxy to real\n        value. It works only with values which are not validated\n        against realy base data types.\n        "

        def __getattr__(self, item):
            return getattr(get_constance_value(), item)

        def __str__(self):
            return str(get_constance_value())

    return Template()


DJANGOCMS_GOOGLEMAP_API_KEY = _lazy_constance('DJANGOCMS_GOOGLEMAP_API_KEY')