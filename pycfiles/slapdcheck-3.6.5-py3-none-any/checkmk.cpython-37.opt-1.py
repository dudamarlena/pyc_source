# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdcheck/checkmk.py
# Compiled at: 2020-01-22 10:55:43
# Size of source mod 2**32: 2243 bytes
"""
slapdcheck.checkmk - local check for check_mk
"""
import os, sys
from slapdcheck import MonitoringCheck, SlapdCheck
from slapdcheck.cnf import CHECK_RESULT_ERROR, CHECK_RESULT_OK, CHECK_RESULT_UNKNOWN, CHECK_RESULT_WARNING

class CheckMkSlapdCheck(SlapdCheck, MonitoringCheck):
    __doc__ = '\n    slapd check for checkmk\n    '
    checkmk_status = {CHECK_RESULT_OK: 'OK', 
     CHECK_RESULT_WARNING: 'WARNING', 
     CHECK_RESULT_ERROR: 'ERROR', 
     CHECK_RESULT_UNKNOWN: 'UNKNOWN'}
    output_format = '{status_code} {name} {perf_data} {status_text} - {msg}\n'

    def __init__(self, output_file, state_filename=None):
        SlapdCheck.__init__(self, output_file, state_filename)

    def serialize_perf_data(self, pdat):
        if not pdat:
            return '-'
        return '|'.join(['%s=%s' % (pkey, pval) for pkey, pval in pdat.items()])

    def output(self):
        """
        Outputs all check_mk results registered before with method result()
        """
        MonitoringCheck.output(self)
        for i in sorted(self._item_dict.keys()):
            status, check_name, perf_data, check_msg = self._item_dict[i]
            sys.stdout.write(self.output_format.format(status_code=status,
              perf_data=(self.serialize_perf_data(perf_data)),
              name=(self.subst_item_name_chars(check_name)),
              status_text=(self.checkmk_status[status]),
              msg=check_msg))


def run():
    """
    run as check_mk local check
    """
    slapd_check = CheckMkSlapdCheck(output_file=(sys.stdout),
      state_filename=(os.path.basename(sys.argv[0][:-3])))
    slapd_check.run()


if __name__ == '__main__':
    run()