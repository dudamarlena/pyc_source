# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/log_patterns.py
# Compiled at: 2016-05-04 07:56:27
from . import utils
__all__ = ('patterns', )
_patterns_old = {'resource': (
              ('lrmd.*%% (?:start|stop|promote|demote|migrate)', 'lrmd.*RA output: .%%:.*:stderr',
 'lrmd.*WARN: Managed %%:.*exited', 'lrmd.*WARN: .* %% .*timed out$', 'crmd.*LRM operation %%_(?:start|stop|promote|demote|migrate)_.*confirmed=true',
 'crmd.*LRM operation %%_.*Timed Out', '[(]%%[)][[]'),
              ('lrmd.*%% (?:probe|notify)', 'lrmd.*Managed %%:.*exited')), 
   'node': (
          (' %% .*Corosync.Cluster.Engine', ' %% .*Executive.Service.RELEASE', ' %% .*Requesting.shutdown',
 ' %% .*Shutdown.complete', ' %% .*Configuration.validated..Starting.heartbeat',
 'pengine.*Scheduling Node %% for STONITH', 'crmd.* of %% failed', "stonith-ng.*host '%%'",
 'Exec.*on %% ', 'Node %% will be fenced', 'stonith-ng.*for %% timed', 'stonith-ng.*can not fence %%:',
 'stonithd.*Succeeded.*node %%:', '(?:lost|memb): %% ', 'crmd.*(?:NEW|LOST):.* %% ',
 'Node return implies stonith of %% '),
          ()), 
   'quorum': (
            ('crmd.*Updating.quorum.status', 'crmd.*quorum.(?:lost|ac?quir)'),
            ()), 
   'events': (
            ('CRIT:', 'ERROR:'),
            ('WARN:', ))}
_patterns_118 = {'resource': (
              ('crmd.*Initiating.*%%_(?:start|stop|promote|demote|migrate)_', 'lrmd.*operation_finished: %%_',
 'lrmd.*executing - rsc:%% action:(?:start|stop|promote|demote|migrate)', 'lrmd.*finished - rsc:%% action:(?:start|stop|promote|demote|migrate)',
 'crmd.*LRM operation %%_(?:start|stop|promote|demote|migrate)_.*confirmed=true',
 'crmd.*LRM operation %%_.*Timed Out', '[(]%%[)][[]'),
              ('crmd.*Initiating.*%%_(?:monitor_0|notify)', 'lrmd.*executing - rsc:%% action:(?:monitor_0|notify)',
 'lrmd.*finished - rsc:%% action:(?:monitor_0|notify)')), 
   'node': (
          (' %% .*Corosync.Cluster.Engine', ' %% .*Executive.Service.RELEASE', ' %% .*crm_shutdown:.Requesting.shutdown',
 ' %% .*pcmk_shutdown:.Shutdown.complete', ' %% .*Configuration.validated..Starting.heartbeat',
 'pengine.*Scheduling Node %% for STONITH', 'pengine.*Node %% will be fenced', 'crmd.*for %% failed',
 "stonith-ng.*host '%%'", 'Exec.*on %% ', 'Node %% will be fenced', 'stonith-ng.*on %% for.*timed out',
 'stonith-ng.*can not fence %%:', 'stonithd.*Succeeded.*node %%:', '(?:lost|memb): %% ',
 'crmd.*(?:NEW|LOST|new|lost):.* %% ', 'Node return implies stonith of %% '),
          ()), 
   'quorum': (
            ('crmd.*Updating.(quorum).status', 'crmd.*quorum.(?:lost|ac?quir[^\\s]*)'),
            ()), 
   'events': (
            ('(CRIT|crit|ERROR|error|UNCLEAN|unclean):', ),
            ('(WARN|warning):', ))}

def patterns(cib_f=None):
    is118 = utils.is_pcmk_118(cib_f=cib_f)
    if is118:
        return _patterns_118
    else:
        return _patterns_old