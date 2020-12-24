# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/customBurndownChart/config.py
# Compiled at: 2011-09-19 06:47:40
"""
Created on Tue 16 Aug 2011

@author: leewei
"""
URL_CDN_JQUERY = 'http://code.jquery.com/jquery-latest.min.js'
URL_CDN_QTIP2 = 'http://craigsworks.com/projects/qtip2/packages/latest'
SECTION_NAME = 'estimation-tools'
DEFAULT_CHART_DISPLAY = {'unit': 'hours'}

def init_config(env, estimation_field):
    config_options = {'trac': [
              ('permission_store', 'DefaultPermissionStore')], 
       'components': [
                    ('estimationtools.*', 'enabled')], 
       'estimation-tools': [
                          (
                           'estimation_field', estimation_field)], 
       'ticket-custom': [
                       ('estimatedtime', 'text'),
                       ('estimatedtime.label', 'Remaining Time'),
                       ('estimatedtime.value', 0)]}
    config = env.config
    for section, kvs in config_options.iteritems():
        [ config.set(section, key, value) for key, value in kvs ]

    config.save()