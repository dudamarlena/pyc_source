# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/tg.py
# Compiled at: 2014-07-07 15:44:50
from jinja2 import Template
import sys

class TestGenerator(object):

    def gen(self, tests=[]):
        template = Template("#!/usr/bin/env python\nimport difflib\nimport unittest\nimport shlex, subprocess\nimport os\n\nclass TestScript(unittest.TestCase):\n\n    def setUp(self):\n        self.base = ['python', '{{ script_name }}']\n        self.tests = {{ tests }}\n    def test_run(self):\n        for test_case in self.tests:\n            failed_test = False\n            try:\n                current_command = self.base + \\\n                    shlex.split(test_case['command_line'])\n                # Should probably be wrapped in an assert as well\n                subprocess.check_call(current_command)\n\n                for fileset in test_case['outputs']:\n                    failed_test = self.file_comparison(\n                            test_case['outputs'][fileset][0],\n                            test_case['outputs'][fileset][1])\n            except:\n                raise\n            self.assertFalse(failed_test)\n\n    def file_comparison(self, test_file, comp_file):\n        failed_test = False\n        diff=difflib.unified_diff(open(test_file).readlines(),\n                           open(comp_file).readlines())\n        try:\n            while True:\n                print diff.next(),\n                failed_test = True\n        except:\n            pass\n        try:\n            # Attempt to remove the generated file to cut down on\n            # clutter/other bad things\n            os.unlink(test_file)\n        except:\n            pass\n        return failed_test\n\nif __name__ == '__main__':\n    unittest.main()\n")
        for test in tests:
            cli = ''
            for param in test['params']:
                cli += '--' + param + ' ' + test['params'][param]

            try:
                del test['params']
            except:
                pass

            test['command_line'] = cli

        return template.render({'tests': tests, 'script_name': sys.argv[0]})