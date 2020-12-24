# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldmudefuns/startup.py
# Compiled at: 2019-05-18 11:36:10
# Size of source mod 2**32: 825 bytes


def startup():
    """ Loads all registered packages that offer the ldmud_efun entry point.

    In the configuration file ~/.ldmud-efuns single efuns can be deactivated
    with entries like:

        [efuns]
        name_of_the_efun = off
    """
    import pkg_resources, traceback, sys, os, configparser, ldmud
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']
    for entry_point in pkg_resources.iter_entry_points('ldmud_efun'):
        if efunconfig.getboolean(entry_point.name, True):
            try:
                print('Registering Python efun', entry_point.name)
                ldmud.register_efun(entry_point.name, entry_point.load())
            except:
                traceback.print_exc()