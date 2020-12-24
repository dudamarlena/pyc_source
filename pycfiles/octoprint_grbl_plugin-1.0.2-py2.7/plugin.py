# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/octoprint_grbl_plugin/plugin.py
# Compiled at: 2018-04-19 09:46:10
import re, logging
log = logging.getLogger(__name__)

def unsupported_commands(comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    """
    Suppress certain commands, because Grbl cant handle them.
    """
    if cmd.startswith('M110 '):
        return (None, )
    else:
        if cmd == 'M105':
            return '?$G'
        if cmd == 'M400':
            return 'G4 P0'
        if cmd == 'M114':
            return '?'
        return


def translate_ok(comm_instance, line, *args, **kwargs):
    """
    This plugin moves Grbl's ok from the end to the start.
    OctoPrint needs the 'ok' to be at the start of the line.
    """
    if 'MPos' in line:
        match = re.search('MPos:(-?[\\d\\.]+),(-?[\\d\\.]+),(-?[\\d\\.]+)', line)
        if match is None:
            log.warning('Bad data %s', line.rstrip())
            return line
        return ('ok X:{0} Y:{1} Z:{2} E:0 {original}').format(original=line, *match.groups())
    else:
        if line.startswith('Grbl'):
            return 'ok ' + line
        else:
            if not line.rstrip().endswith('ok'):
                return line
            if line.startswith('{'):
                return 'ok'
            if '{' in line:
                before, _, _ = line.partition('{')
                return 'ok ' + before
            return 'ok'

        return