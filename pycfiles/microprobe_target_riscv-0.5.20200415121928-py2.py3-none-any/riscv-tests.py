# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rbertra/workspace/repos/github.com/IBM/microprobe/targets/riscv/wrappers/riscv-tests.py
# Compiled at: 2020-03-29 13:02:20
from __future__ import absolute_import
from microprobe.code import get_wrapper
from microprobe.utils.logger import get_logger
LOG = get_logger(__name__)
__all__ = ['RiscvTestsP']

class RiscvTestsP(get_wrapper('Assembly')):

    def __init__(self, endless=False, reset=False):
        self._endless = endless
        self._reset = reset
        super(RiscvTestsP, self).__init__()

    def headers(self):
        return '\n/* Headers */\n#include "riscv_test.h"\n#include "riscv-tests/isa/macros/scalar/test_macros.h"\n\n'

    def start_main(self):
        return '\n/* Start Main */\nRVTEST_RV64UF\nRVTEST_CODE_BEGIN\n\n'

    def outputname(self, name):
        """

        :param name:

        """
        if not name.endswith('.S'):
            return '%s.S' % name
        return name

    def post_var(self):
        return ('').join('reset:')

    def start_loop(self, instr, instr_reset, dummy_aligned=True):
        """

        :param instr:
        :param instr_reset:
        :param dummy_aligned:  (Default value = True)

        """
        start_loop = [
         '/* Building block start */\n']
        if not self._endless:
            return ('\n').join(start_loop)
        if self._reset:
            instr_reset.add_comment('Loop start reseting')
            if not instr_reset.label:
                instr_reset.set_label('reset')
                self._loop_label = 'reset'
            else:
                self._loop_label = instr_reset.label
        else:
            instr.add_comment('Loop start')
            if not instr.label:
                instr.set_label('infloop')
                self._loop_label = 'infloop'
            else:
                self._loop_label = instr.label
        return ('\n').join(start_loop)

    def end_loop(self, dummy_instr):
        """
        """
        if not self._endless:
            return '/* Loop End */'
        loop = ['/* Loop End */']
        loop.append(self.wrap_ins('j %s' % self._loop_label))
        return ('\n').join(loop)

    def end_main(self):
        return '\n/* End Main */\n  TEST_CASE( 1, x0, 0, nop )\n  TEST_PASSFAIL\n\nRVTEST_CODE_END\n\n  .data\nRVTEST_DATA_BEGIN\n\n  TEST_DATA\n\nRVTEST_DATA_END\n\n'

    def declare_global_var(self, var):
        if var.align:
            return '.comm %s, %d, %d\n' % (var.name, var.size, var.align)
        else:
            return '.comm %s, %d\n' % (var.name, var.size)