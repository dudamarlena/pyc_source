# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/sphsettings.py
# Compiled at: 2012-03-17 12:42:14
from django.conf import settings
sph_settings_defaults = {'django096compatibility': False, 
   'community_avatar_default': settings.STATIC_URL + 'sphene/community/default_avatar.png', 
   'community_avatar_default_width': 48, 
   'community_avatar_default_height': 48, 
   'community_avatar_max_width': 150, 
   'community_avatar_max_height': 150, 
   'community_avatar_max_size': 153600, 
   'community_avatar_upload_to': 'var/sphene/sphwiki/attachment/%Y/%m/%d', 
   'community_groupaware_template_dir': None, 
   'community_groups_in_url': False, 
   'community_groupaware_startpage': None, 
   'community_email_show_only_public': False, 
   'community_email_anonymous_require_captcha': False, 
   'community_register_require_captcha': False, 
   'community_email_anonymous_require_captcha_timeout': 600, 
   'community_user_get_displayname': None, 
   'community_user_get_avatar': None, 
   'community_user_displayname_fallback': 'fullname', 
   'default_group_name': 'example'}

def add_setting_defaults(newdefaults):
    """
    This method can be used by other applications to define their
    default values.
    
    newdefaults has to be a dictionary containing name -> value of
    the settings.
    """
    sph_settings_defaults.update(newdefaults)


def set_sph_setting(name, value):
    if not hasattr(settings, 'SPH_SETTINGS'):
        settings.SPH_SETTINGS = {}
    settings.SPH_SETTINGS[name] = value


def get_sph_setting(name, default_value=None):
    if not hasattr(settings, 'SPH_SETTINGS'):
        return sph_settings_defaults.get(name, default_value)
    return settings.SPH_SETTINGS.get(name, sph_settings_defaults.get(name, default_value))