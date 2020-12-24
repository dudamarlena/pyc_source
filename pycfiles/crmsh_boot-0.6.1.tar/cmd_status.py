# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/cmd_status.py
# Compiled at: 2016-05-11 07:39:05
import re
from . import clidisplay
from . import utils
_crm_mon = None
_WARNS = [
 'pending',
 'complete',
 'Timed Out',
 'NOT SUPPORTED',
 'Error',
 'Not installed',
 'UNKNOWN\\!',
 'Stopped',
 'standby']
_OKS = ['Online', 'online', 'ok', 'master', 'Started', 'Master', 'Slave']
_ERRORS = ['not running',
 'unknown error',
 'invalid parameter',
 'unimplemented feature',
 'insufficient privileges',
 'not installed',
 'not configured',
 'not running',
 'master \\(failed\\)',
 'OCF_SIGNAL',
 'OCF_NOT_SUPPORTED',
 'OCF_TIMEOUT',
 'OCF_OTHER_ERROR',
 'OCF_DEGRADED',
 'OCF_DEGRADED_MASTER',
 'unknown',
 'Unknown',
 'OFFLINE',
 'Failed actions']

class CrmMonFilter(object):
    _OK = re.compile('(%s)' % ('|').join(_OKS))
    _WARNS = re.compile('(%s)' % ('|').join(_WARNS))
    _ERROR = re.compile('(%s)' % ('|').join(_ERRORS))
    _NODES = re.compile('(\\d+ Nodes configured)')
    _RESOURCES = re.compile('(\\d+ Resources configured)')
    _RESOURCE = re.compile('(\\S+)(\\s+)\\((\\S+:\\S+)\\):')
    _GROUP = re.compile('(Resource Group|Clone Set): (\\S+)')

    def _filter(self, line):
        line = self._RESOURCE.sub('%s%s(%s):' % (clidisplay.help_header('\\1'),
         '\\2',
         '\\3'), line)
        line = self._NODES.sub(clidisplay.help_header('\\1'), line)
        line = self._RESOURCES.sub(clidisplay.help_header('\\1'), line)
        line = self._GROUP.sub('\\1: ' + clidisplay.help_header('\\2'), line)
        line = self._WARNS.sub(clidisplay.warn('\\1'), line)
        line = self._OK.sub(clidisplay.ok('\\1'), line)
        line = self._ERROR.sub(clidisplay.error('\\1'), line)
        return line

    def __call__(self, text):
        return ('\n').join([ self._filter(line) for line in text.splitlines() ]) + '\n'


def crm_mon(opts=''):
    """
    Run 'crm_mon -1'
    opts: Additional options to pass to crm_mon
    returns: rc, stdout
    """
    global _crm_mon
    if _crm_mon is None:
        prog = utils.is_program('crm_mon')
        if not prog:
            raise IOError('crm_mon not available, check your installation')
        _, out = utils.get_stdout('%s --help' % prog)
        if '--pending' in out:
            _crm_mon = '%s -1 -j' % prog
        else:
            _crm_mon = '%s -1' % prog
    status_cmd = '%s %s' % (_crm_mon, opts)
    return utils.get_stdout(utils.add_sudo(status_cmd))


def cmd_status(args):
    """
    Calls crm_mon -1, passing optional extra arguments.
    Displays the output, paging if necessary.
    Raises IOError if crm_mon fails.
    """
    opts = {'bynode': '-n', 
       'inactive': '-r', 
       'ops': '-o', 
       'timing': '-t', 
       'failcounts': '-f', 
       'verbose': '-V', 
       'quiet': '-Q', 
       'html': '--as-html', 
       'xml': '--as-xml', 
       'simple': '-s', 
       'tickets': '-c', 
       'noheaders': '-D', 
       'detail': '-R', 
       'brief': '-b', 
       'full': '-ncrft'}
    extra = (' ').join(opts.get(arg, arg) for arg in args)
    if not args:
        extra = '-r'
    rc, s = crm_mon(extra)
    if rc != 0:
        raise IOError('crm_mon (rc=%d): %s' % (rc, s))
    utils.page_string(CrmMonFilter()(s))
    return True


def cmd_verify(args):
    """
    Calls crm_verify -LV; ptest -L -VVVV
    """
    from . import config
    if 'ptest' in config.core.ptest:
        cmd1 = 'crm_verify -LV; %s -L -VVVV' % config.core.ptest
    else:
        cmd1 = 'crm_verify -LV; %s -LjV' % config.core.ptest
        if 'scores' in args:
            cmd1 += ' -s'
    cmd1 = utils.add_sudo(cmd1)
    rc, s, e = utils.get_stdout_stderr(cmd1)
    e = ('\n').join(clidisplay.error(l) for l in e.split('\n')).strip()
    utils.page_string(('\n').join((s, e)))
    return rc == 0 and not e