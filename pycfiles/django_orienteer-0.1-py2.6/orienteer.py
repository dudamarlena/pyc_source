# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/orienteer/templatetags/orienteer.py
# Compiled at: 2010-05-15 22:19:25
"""Simple Compass integration for Django"""
__author__ = 'Drew Yeaton <drew@sentineldesign.net>'
__version__ = '0.1'
import os
from commands import getstatusoutput
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def compass(filename):
    proj_dir = settings.COMPASS_PROJECT_DIR
    src_dir = proj_dir + 'src/'
    src_path = src_dir + filename + '.sass'
    output_dir = settings.COMPASS_OUTPUT_DIR
    output_url = settings.COMPASS_OUTPUT_URL
    needs_update = False
    try:
        stat = os.stat(src_path)
        src_file_ts = stat.st_mtime
    except:
        print "Compass source file '%s' not found! Not outputting CSS tag." % src_path
        return ''
    else:
        try:
            stat = os.stat(proj_dir + filename + '.css')
            output_file_ts = stat.st_mtime
        except:
            needs_update = True

        css = "<link rel='stylesheet' href='%s?%s' type='text/css' />" % (output_url + filename + '.css', src_file_ts)
        if not needs_update:
            if src_file_ts <= output_file_ts:
                return css

    cmd_dict = {'bin': settings.COMPASS_BIN, 
       'sass_style': settings.COMPASS_STYLE, 
       'project_dir': proj_dir, 
       'output_dir': output_dir}
    cmd = '%(bin)s compile -s %(sass_style)s --css-dir %(output_dir)s %(project_dir)s' % cmd_dict
    (status, output) = getstatusoutput(cmd)
    print output
    return css