# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/bp/convert/movie/handbrake.py
# Compiled at: 2010-10-08 06:47:55
"""
handbrake.py

Created by Andreas Kaiser on 2010-10-08.
Copyright (c) 2010 Xo7 GmbH. All rights reserved.
"""
import subprocess
HANDBRAKE = 'HandBrakeCLI'

class Handbrake(object):
    """Simple wrapper for HandBrakeCLI for use in the command line script"""

    @property
    def presets(self):
        """Return a dictionary containing the presets supported by the locally installed HandBrakeCLI"""
        presets = {}
        cmd_stdout = subprocess.Popen([HANDBRAKE, '-z'], stdout=subprocess.PIPE).stdout
        for l in cmd_stdout:
            if l in ('', '\n', '>\n'):
                continue
            l = l.replace('\n', '')
            if l.startswith('<'):
                preset_group = l[2:]
                presets[preset_group] = {}
            elif l.startswith('   + '):
                preset = l[5:].split(':  ')
                presets[preset_group][preset[0]] = preset[1]

        return presets