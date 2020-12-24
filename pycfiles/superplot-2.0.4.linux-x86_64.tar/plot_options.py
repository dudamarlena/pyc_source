# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/plot_options.py
# Compiled at: 2017-08-19 22:58:02
"""
This module provides a named tuple plot_options to represent the options as
selected in the UI. Also loads default values from config.yml and makes them available.

TODO: This module should also do a reasonable amount of validation
      of config variables.
"""
import os, appdirs
from collections import namedtuple
import simpleyaml as yaml, numpy as np
plot_options = namedtuple('plot_options', ('xindex', 'yindex', 'zindex', 'logx', 'logy',
                                           'logz', 'plot_limits', 'bin_limits', 'nbins',
                                           'xticks', 'yticks', 'alpha', 'tau', 'xlabel',
                                           'ylabel', 'zlabel', 'plot_title', 'title_position',
                                           'leg_title', 'leg_position', 'show_best_fit',
                                           'show_posterior_mean', 'show_posterior_median',
                                           'show_posterior_mode', 'show_conf_intervals',
                                           'show_credible_regions', 'show_posterior_pdf',
                                           'show_prof_like', 'kde_pdf', 'bw_method'))

def get_config(yaml_file='config.yml'):
    """
    Load the config file, either from the user data
    directory, or if that is not available, the installed
    copy.
    
    :param yaml_file: Name of yaml file
    :type yaml_file: str
    
    :returns: config
    :rtype: dict
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    home_dir_locfile = os.path.join(script_dir, 'user_home.txt')
    config_path = None
    if os.path.exists(home_dir_locfile):
        with open(home_dir_locfile, 'rb') as (f):
            home_dir_path = f.read()
            config_path = os.path.join(home_dir_path, yaml_file)
    if config_path is None or not os.path.exists(config_path):
        config_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], yaml_file)
    with open(config_path) as (cfile):
        return yaml.load(cfile)
    return


CONFIG = get_config()

def default(option):
    """
    Retrieve the default value of a plot option.

    If no default is available, prints an error message and raises
    a KeyError.

    :param option: Name of the option
    :type option: string

    :returns: Default value of specified option.
    """
    _defaults = CONFIG['plot_options']
    if _defaults['alpha'] is not None:
        _defaults['alpha'] = np.array(_defaults['alpha'])
        _defaults['alpha'].sort()
    if _defaults['plot_limits'] is not None:
        _defaults['plot_limits'] = np.array(_defaults['plot_limits'])
    try:
        return _defaults[option]
    except KeyError:
        print ('plot_options: No default specified for option: {}').format(option)
        raise

    return