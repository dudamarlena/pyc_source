# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/confiture/__init__.py
# Compiled at: 2014-05-11 06:19:13
__doc__ = ' Confiture is an advanced configuration parser for Python.\n'
from confiture.parser import ConfitureParser, yacc

class Confiture(object):

    def __init__(self, config, schema=None, input_name='<unknown>'):
        self._config = config
        self._schema = schema
        self._input_name = input_name

    @classmethod
    def from_filename(cls, filename, **kwargs):
        fconf = open(filename, 'Ur')
        kwargs['input_name'] = filename
        return cls(fconf.read(), **kwargs)

    def _parse(self):
        parser = ConfitureParser(self._config, debug=False, write_tables=False, errorlog=yacc.NullLogger(), input_name=self._input_name)
        return parser.parse()

    def parse(self):
        config = self._parse()
        if self._schema is not None:
            config = self._schema.validate(config)
        return config