# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/registry.py
# Compiled at: 2014-04-28 05:34:58


class CTRegistry(object):
    """ Global registry for content types

    The registry can take any attrivutes per content type, but the following
    attributes have active use so far:

      class            Actual class for ct
      app              App id
      label            Front end name of CT
      global_add       Whether the ct should show in the add menu
      global_filter    Whether the ct should show in the search filters
      add_permission   Permission to determine whether a user can add the CT
      view_permission  Permission to determine whether a user can use the CT in
                       search filters.
      del_permission   Permission to determine whether a user can delete the CT
      edit_permission  Permission to check whether a user can edit the CT
      name_plural      well...
      filter_label     Label to show in filter. If empty, not shown at all.
      group_add        Whether the CT can be added to group context

    """
    content_types = {}

    @staticmethod
    def register(name, register_dict):
        CTRegistry.content_types[name] = register_dict
        CTRegistry.content_types['%s.%s' % (register_dict['app'], name)] = register_dict

    @staticmethod
    def get(name):
        """
        Fetch all details for contenttype with name as a dict.
        """
        return CTRegistry.content_types.get(name, {})

    @staticmethod
    def get_attr(name, attr, default=None):
        """ Fetch given attr. Return default if not set"""
        return CTRegistry.content_types.get(name, {}).get(attr, default)

    @staticmethod
    def list_types(excludes=[]):
        """ Only list the 'full' keys: those with the app id and model id """
        return filter(lambda x: x not in excludes and '.' in x, CTRegistry.content_types.keys())