# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/startup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2475 bytes
import sys, boto
from boto.utils import find_class
from boto import config
from boto.pyami.scriptbase import ScriptBase

class Startup(ScriptBase):

    def run_scripts(self):
        scripts = config.get('Pyami', 'scripts')
        if scripts:
            for script in scripts.split(','):
                script = script.strip(' ')
                try:
                    pos = script.rfind('.')
                    if pos > 0:
                        mod_name = script[0:pos]
                        cls_name = script[pos + 1:]
                        cls = find_class(mod_name, cls_name)
                        boto.log.info('Running Script: %s' % script)
                        s = cls()
                        s.main()
                    else:
                        boto.log.warning('Trouble parsing script: %s' % script)
                except Exception as e:
                    boto.log.exception('Problem Running Script: %s. Startup process halting.' % script)
                    raise e

    def main(self):
        self.run_scripts()
        self.notify('Startup Completed for %s' % config.get('Instance', 'instance-id'))


if __name__ == '__main__':
    if not config.has_section('loggers'):
        boto.set_file_logger('startup', '/var/log/boto.log')
    sys.path.append(config.get('Pyami', 'working_dir'))
    su = Startup()
    su.main()