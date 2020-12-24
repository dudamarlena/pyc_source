# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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