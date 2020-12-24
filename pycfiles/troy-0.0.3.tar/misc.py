# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/utils/misc.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import os, sys, glob, radical.utils as ru, troy

def get_config(params):
    """
    This method attempts to obtain configuration settings from a variety of
    sources, depending on the parameter. it can point to an env var, or to
    a directory containing configuration files, or to a single configuration
    file, or to a list of any above, or it is a config dict already, or a list
    of such dicts.  In all cases, the config is obtained from the respective
    source (which is assumed json formatted in the case of config files), and
    a single merged and expanded dict is returned.
    """
    ret = dict()
    if not isinstance(params, list):
        params = [
         params]
    for param in params:
        if not param or None == param:
            continue
        elif isinstance(param, dict):
            ru.dict_merge(ret, param, policy='overwrite')
        elif isinstance(param, basestring):
            if param in os.environ:
                param = os.environ[param]
            if os.path.isdir(param):
                cfg_files = glob.glob('%s/*' % param)
            else:
                if os.path.isfile(param):
                    cfg_files = [param]
                else:
                    troy._logger.warning('cannot handle config location %s' % param)
                    cfg_files = list()
                print 'files: %s' % cfg_files
                for cfg_file in cfg_files:
                    cfg_dict = dict()
                    try:
                        cfg_dict = ru.read_json(cfg_file)
                        troy._logger.info('reading  config in %s' % cfg_file)
                    except Exception as e:
                        troy._logger.critical('skipping config in %s (%s)' % (cfg_file, e))
                        raise

                    ru.dict_merge(ret, cfg_dict, policy='overwrite')

        else:
            raise TypeError('get_config parameter must be (list of) dict or string, not %s' % type(param))

    ru.dict_stringexpand(ret)
    return ret