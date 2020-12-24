# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/reportingplugins/simplereport.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 1987 bytes
import os
from fastr import version
from fastr.helpers import log
from fastr.execution.networkrun import NetworkRun
from fastr.plugins.reportingplugin import ReportingPlugin

class SimpleReport(ReportingPlugin):

    def run_finished(self, run: NetworkRun):
        log.info('===== RESULTS =====')
        result = True
        for sink_node, sink_data in sorted(run.sink_results.items()):
            nr_failed = sum((len(x[1]) > 0 for x in sink_data.values()))
            nr_success = len(sink_data) - nr_failed
            if nr_failed > 0:
                result = False
            log.info('{}: {} success / {} failed'.format(sink_node, nr_success, nr_failed))

        log.info('===================')
        if not result:
            sink_result_file = os.path.join(run.tmpdir, run.SINK_DUMP_FILE_NAME)
            log.warning('There were failed samples in the run, to start debugging you can run:\n\n    fastr trace {sink_data_file} --sinks\n\nsee the debug section in the manual at https://fastr.readthedocs.io/en/{branch}/static/user_manual.html#debugging for more information.'.format(sink_data_file=sink_result_file,
              branch=('default' if version.hg_branch == 'default' else 'develop')))