# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/tools/tools.py
# Compiled at: 2013-11-25 12:16:12
__author__ = 'yarnaid'
import os, subprocess as sp, tempfile, time, glespy.tools.logger as lg
glesp_exec = '/usr/local/bin'
glesp = dict()
glesp['mappat'] = os.path.join(glesp_exec, 'mappat')
glesp['cl2map'] = os.path.join(glesp_exec, 'cl2map')
glesp['difmap'] = os.path.join(glesp_exec, 'difmap')
glesp['alm2dl'] = os.path.join(glesp_exec, 'alm2dl')
glesp['f2fig'] = os.path.join(glesp_exec, 'f2fig')
glesp['rsalm'] = os.path.join(glesp_exec, 'rsalm')
glesp['difalm'] = os.path.join(glesp_exec, 'difalm')
GIF_VIEWER = 'feh'
binaries = dict()
binaries.update(glesp)
binaries['viewer'] = os.path.join('/usr/bin', 'eog')
info = lg.logger.info
warn = lg.logger.warn
error = lg.logger.error
critical = lg.logger.critical
log = lg.logger.log
exception = lg.logger.exception
debug = lg.logger.debug
__all__ = [
 'run_cmd', 'get_out_name', 'glesp', 'binaries',
 'info', 'warn', 'debug', 'error', 'critical', 'log', 'exception']

def run_cmd(args, debug_msg=None, shell=None, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs):
    args = map(str, args)
    proc = sp.Popen(list(args), stdout=stdout, stderr=stderr, shell=shell)
    proc.wait()
    res = proc.communicate()
    if debug_msg:
        debug(debug_msg)
    if len(res[0]):
        debug(args)
        debug(res[0])
    if len(res[1]):
        debug([res[1]])
    return res


def get_out_name(out_name=None, suffix='tmp', dir='/tmp', **kwargs):
    res = out_name
    if not res:
        tmp_file = tempfile.NamedTemporaryFile(dir=dir, suffix='_' + ('_').join([
         str(time.time()), suffix]), delete=kwargs.get('delete', True))
        res = tmp_file.name
    return res