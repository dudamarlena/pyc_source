# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/conf.py
# Compiled at: 2013-11-22 18:12:08
from django.conf import settings
from appconf import AppConf

class DJOAuth2Conf(AppConf):
    """ Default OAuth-related implementation settings.

  Implementation-specific settings. Each of the settings can be overridden in
  your own ``setup.py`` with a ``DJOAUTH2_`` prefix like so:

  .. code:: python

      settings.DJOAUTH2_SETTING_NAME = <Value>

  That said, in order to maintain the highest level of security and to avoid
  breaking the specification's rules or recommendations, we **strongly
  recommend that you do not change these values** Doing so can break compliance
  with the OAuth specification, and/or introduce large security flaws into the
  authentication process. Please read through the `Security Considerations
  <http://tools.ietf.org/html/rfc6749#section-10>`_ and convince yourself that
  you really know what you're doing before changing any of these values.

  """

    class Meta:
        prefix = 'djoauth2'

    ACCESS_TOKEN_LENGTH = 30
    ACCESS_TOKEN_LIFETIME = 3600
    ACCESS_TOKENS_REFRESHABLE = True
    AUTHORIZATION_CODE_LENGTH = 30
    AUTHORIZATION_CODE_LIFETIME = 600
    CLIENT_KEY_LENGTH = 30
    CLIENT_SECRET_LENGTH = 30
    REFRESH_TOKEN_LENGTH = 30
    REALM = ''
    REQUIRE_STATE = True
    SSL_ONLY = True