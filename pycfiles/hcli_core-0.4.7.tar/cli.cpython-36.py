# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jeff/Windows/Documents/workspace/hcli/hcli_core/hcli_core/sample/hfm/cli/cli.py
# Compiled at: 2019-10-21 14:11:40
# Size of source mod 2**32: 1499 bytes
import json, io, os, chroot as ch
from functools import partial
import subprocess

class CLI:
    commands = None
    inputstream = None
    chroot = None

    def __init__(self, commands, inputstream):
        self.commands = commands
        self.inputstream = inputstream
        self.chroot = ch.Chroot()

    def execute(self):
        print(self.commands)
        if self.commands[1] == 'cp':
            if self.inputstream != None:
                if self.commands[2] == '-l':
                    self.upload()
                    return
            if self.inputstream == None:
                if self.commands[2] == '-r':
                    return self.download()
        if self.commands[1] == 'ls':
            content = bytearray(b'')
            ls = subprocess.Popen(['ls', '-la', self.chroot.pwd], stdout=(subprocess.PIPE))
            pipe = ls.stdout
            for line in pipe:
                content.extend(line)

            return io.BytesIO(content)

    def upload(self):
        unquoted = self.commands[3].replace("'", '').replace('"', '')
        jailed = self.chroot.translate(unquoted)
        with io.open(jailed, 'wb') as (f):
            for chunk in iter(partial(self.inputstream.read, 16384), b''):
                f.write(chunk)

    def download(self):
        unquoted = self.commands[3].replace("'", '').replace('"', '')
        jailed = self.chroot.translate(unquoted)
        f = open(jailed, 'rb')
        return io.BytesIO(f.read())