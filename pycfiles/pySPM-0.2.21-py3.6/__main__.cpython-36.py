# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\__main__.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 1703 bytes
import os, sys
cmd = None
if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    commands = {}

    def run_script(func):
        import importlib
        mod = importlib.import_module('pySPM.tools.' + func)
        sys.argv = [sys.argv[0]] + [x for x in sys.argv[2:]]
        mod.main()


    cmds = {'stability':dict(doc='Run a stability plotter tool in a GUI', script='stability'), 
     'plotter':dict(doc='Display a live graphical display of all the logged parameters (usually the emission current)', alias=['emission_current_plotter', 'parameters_plotter'], script='emission_current_plotter'), 
     'timer':dict(doc='Display informations about the current measurement time. In particular this function estimate the remaining time from the measurement proportion and the elapsed time.', alias=['tof_timer', 'measurement_timer'], script='tof_timer'), 
     'spectra':dict(doc='Spectra plotter and mass calibration GUI', script='spectra')}
    for c in cmds:
        doc = cmds[c].get('doc', '')
        script = cmds[c].get('script', None)
        commands[c] = (script, doc)
        if 'alias' in cmds[c]:
            for a in cmds[c]['alias']:
                commands[a] = (
                 script, doc)

    if cmd is None or cmd in ('help', '--help', '-h', '?', '-?'):
        print('Give as argument the command that pySPM should run. Valid commands are:')
        for c in cmds:
            print('{}: {} (aliases: {})'.format(c, cmds[c].get('doc', ''), ','.join(cmds[c].get('alias', []))))

    else:
        if cmd in commands:
            print('Running command "{}"'.format(cmd))
            run_script(commands[cmd][0])
        else:
            print('Command "{}" not understood'.format(cmd))
            print('Valid commands are:')
            for c in commands:
                print('{}: {}'.format(c, commands[c][1]))