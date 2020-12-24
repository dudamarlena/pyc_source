# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/tests/test_kraut.py
# Compiled at: 2013-06-02 13:05:33
# Size of source mod 2**32: 950 bytes
import os, logging, os.path as op
try:
    from testkraut.testcase import TestFromSPEC, discover_specs, template_case, TemplateTestCase
    if 'TESTKRAUT_LOGGER_VERBOSE' in os.environ:
        lgr = logging.getLogger('testkraut')
        console = logging.StreamHandler()
        lgr.addHandler(console)
        cfg = os.environ['TESTKRAUT_LOGGER_VERBOSE']
        if cfg == 'debug':
            lgr.setLevel(logging.DEBUG)
        else:
            lgr.setLevel(logging.INFO)

    class TestKrautTests(TestFromSPEC):
        __metaclass__ = TemplateTestCase
        search_dirs = [os.path.join(os.path.dirname(__file__), 'data')]

        @template_case(discover_specs([
         op.join(op.dirname(__file__), 'kraut')]))
        def _run_spec_test(self, spec_filename):
            return TestFromSPEC._run_spec_test(self, spec_filename)


except ImportError:
    pass