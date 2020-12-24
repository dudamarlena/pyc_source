# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/tools/PackageLabel.py
# Compiled at: 2014-08-15 03:55:24
# Size of source mod 2**32: 1095 bytes
import logging, traceback, subprocess
COMMASPACE = ', '

class PackageLabel:
    fop_exec = None
    fop_config = None
    noosh_monitor = None

    def __init__(self, fop_exec, fop_config, noosh_monitor):
        self.logger = logging.getLogger('pf3')
        self.fop_exec = fop_exec
        self.fop_config = fop_config
        self.noosh_monitor = noosh_monitor

    def generate(self, fo_file, specification):
        self.logger.info('Generating package lable for PIC Cde: ' + specification['reference_number'])
        try:
            cmd = ['"' + self.fop_exec + '"', '-c=' + self.fop_config,
             '"' + specification['reference_number'] + '"']
            cmd_str = ' '.join(cmd)
            p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processResult = p.communicate()
        except subprocess.CalledProcessError:
            self.logger.error('Problem calling command: ' + str(cmd))
            self.logger(traceback.format_exc())