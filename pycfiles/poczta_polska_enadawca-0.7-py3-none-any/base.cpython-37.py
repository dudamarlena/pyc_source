# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/shellcodes/base.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 976 bytes


class ShellCode:

    def __init__(self, os_target='', os_target_arch='', connect_back_ip='localhost', connect_back_port=5555, bad_chars=[], prefix='', suffix=''):
        self.os_target = os_target
        self.os_target_arch = os_target_arch
        self.connect_back_ip = connect_back_ip
        self.connect_back_port = connect_back_port
        self.bad_chars = bad_chars
        self.prefix = prefix
        self.suffix = suffix
        self.name = ''

    def format_shellcode(self, code):
        if isinstance(code, str):
            code = code.replace('{{LOCALHOST}}', self.connect_back_ip)
            code = code.replace('{{LOCALPORT}}', str(self.connect_back_port))
        return code

    def get_shellcode(self, inline=False):
        return ''

    def make_inline(self, payload):
        payload = payload.replace('\t', ' ')
        payload = payload.replace('\r', ' ')
        payload = payload.replace('\n', ' ')
        return payload