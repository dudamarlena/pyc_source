# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\evasion\web\websetup.py
# Compiled at: 2010-05-18 09:51:55
"""Setup the evasion.web application"""
import logging
from evasion.web.config.environment import load_environment

def get_log():
    return logging.getLogger('evasion.web.websetup')


def setup_app(command, conf, vars):
    """
    Load the environment then run each modules setup_app 
    if one was recovered.
    
    """
    set_up = load_environment(conf.global_conf, conf.local_conf, websetup=True)
    setup_app_list = set_up['setup_app_list']
    for setupapp in setup_app_list:
        try:
            get_log().debug("setup_app: calling for '%s'." % setupapp)
            setupapp(command, conf, vars)
        except SystemExit, e:
            raise
        except:
            get_log().exception("Error when calling '%s' - " % setupapp)