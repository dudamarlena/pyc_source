# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/converter.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import datetime

class Converter(object):
    """
    変換
    """

    def __init__(self, config, quiet=False, indent=1):
        u"""
        :param quiet: 処理状況を出力しない
        :type quiet: bool
        """
        self.config = config
        self.quiet = quiet
        self.indent = indent

    def echo(self, message, start_at=None):
        if self.quiet:
            return
        text = (b'{}{} {}').format(b'--' * self.indent, self.config.name, message)
        if start_at:
            delta = datetime.datetime.now() - start_at
            text += (b' ({}.{}s)').format(delta.seconds, delta.microseconds)
        print(text)

    def run(self):
        self.save(self.convert())

    def convert(self):
        u"""
        データの変換を行う
        :rtype: list of dict
        """
        if self.config.has_cache():
            self.echo(b'hit cache')
            return self.config.get_cache()
        self.echo(b'load sheet start')
        start_at = datetime.datetime.now()
        sheet = self.config.get_sheet()
        self.echo(b'load sheet end', start_at=start_at)
        self.echo(b'convert start')
        start_at = datetime.datetime.now()
        _data = self.config.convert(sheet)
        self.echo(b'convert end', start_at=start_at)
        return _data

    def save(self, data):
        self.echo(b'save start')
        start_at = datetime.datetime.now()
        self.config.save(data)
        self.echo(b'save end', start_at=start_at)