# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/primitives/tcpdump.py
# Compiled at: 2017-02-28 08:29:54
from base64 import b64encode
import logging, os, tempfile, centinel
from centinel import command

class Tcpdump:
    """Class to interface between tcpdump and Python"""

    def __init__(self, filename=None, pcap_args=None):
        if filename is None:
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.close()
            filename = temp_file.name
        self.filename = filename
        if pcap_args is None:
            if 'tcpdump_params' in centinel.conf['experiments']:
                pcap_args = centinel.conf['experiments']['tcpdump_params']
            else:
                pcap_args = ['-i', 'any']
                logging.warning('Global config not available, so falling back on -i any pcap args')
        self.pcap_args = pcap_args
        return

    def start(self):
        cmd = ['sudo', 'tcpdump', '-w', self.filename]
        cmd.extend(self.pcap_args)
        self.caller = command.Command(cmd, _tcpdump_callback)
        self.caller.start()

    def stop(self):
        if self.caller is not None:
            self.caller.stop()
        return

    def post_processing(self, out_filter, out_file=None):
        if out_file is None:
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.close()
            out_file = temp_file.name
        cmd = [
         'tcpdump', '-r', self.filename, '-w', out_file]
        caller = command.Command(cmd, _tcpdump_callback)
        caller.start()
        return

    def b64_output(self):
        with open(self.filename, 'r') as (file_p):
            return b64encode(file_p.read())

    def pcap(self):
        with open(self.filename, 'r') as (file_p):
            return file_p.read()

    def pcap_filename(self):
        return self.filename

    def delete(self):
        os.remove(self.filename)


def _tcpdump_callback(self, line, kill_switch):
    """Callback function to handle tcpdump"""
    line = line.lower()
    if 'listening' in line or 'reading' in line:
        self.started = True
    if 'no suitable device' in line:
        self.error = True
        self.kill_switch()
    if 'by kernel' in line:
        self.stopped = True