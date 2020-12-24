# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/interfaces.py
# Compiled at: 2012-02-27 07:41:53


class IAppInstall(object):
    """
    The interface for objects in the entry point group
    ``paste.app_install``
    """

    def __init__(distribution, entry_group, entry_name):
        """
        An object representing a specific application (the
        distribution is a pkg_resource.Distribution object), for the
        given entry point name in the given group.  Right now the only
        group used for this is ``'paste.app_factory'``.
        """
        pass

    def description(sys_config):
        """
        Return a text description of the application and its
        configuration.  ``sys_config`` is a dictionary representing
        the system configuration, and can be used for giving more
        explicit defaults if the application preparation uses the
        system configuration.  It may be None, in which case the
        description should be more abstract.

        Applications are free to ignore ``sys_config``.
        """
        pass

    def write_config(command, filename, sys_config):
        """
        Write a fresh config file to ``filename``.  ``command`` is a
        ``paste.script.command.Command`` object, and should be used
        for the actual operations.  It handles things like simulation
        and verbosity.

        ``sys_config`` is (if given) a dictionary of system-wide
        configuration options.
        """
        pass

    def setup_config(command, config_filename, config_section, sys_config):
        """
        Set up the application, using ``command`` (to ensure simulate,
        etc).  The application is described by the configuration file
        ``config_filename``.  ``sys_config`` is the system
        configuration (though probably the values from it should have
        already been encorporated into the configuration file).
        """
        pass