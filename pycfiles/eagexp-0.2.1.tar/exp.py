# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: eagexp/exp.py
# Compiled at: 2012-12-03 07:11:01
import os

def export_command(output, output_type, timeout=60, commands=[], showgui=False, resolution=None):

    def normpath(f):
        return os.path.abspath(os.path.expandvars(os.path.expanduser(f)))

    output = normpath(output)
    if resolution:
        resolution = int(resolution)
        if resolution > 2400 or resolution < 50:
            raise ValueError('resolution should be inrange 50-2400! current=' + str(resolution))
    else:
        resolution = ''
    if not commands:
        commands = []
    if os.path.exists(output):
        os.remove(output)
    undo = len(commands)
    commands += ['WINDOW']
    commands += [
     ('EXPORT {output_type} {output} {resolution}').format(output_type=output_type, output=output, resolution=resolution)]
    commands += ['UNDO'] * undo
    commands += ['QUIT']
    return commands