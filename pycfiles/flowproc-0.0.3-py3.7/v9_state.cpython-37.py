# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/v9_state.py
# Compiled at: 2019-08-04 00:27:09
# Size of source mod 2**32: 2173 bytes
"""
The stateful parts of NetFlow V9 parsing - i.e. templates and
exporter attributes and options.
"""
import logging
logger = logging.getLogger(__name__)

class Template:
    __doc__ = '\n    Responsibility: represent Template Record\n    '
    tdict = {}

    def __init__(self, tid, tdata):
        self.tid = tid
        self.tdata = tdata
        try:
            try:
                template = Template.tdict[tid]
                if self.__repr__() == template.__repr__():
                    logger.info('Renewing template {:d}'.format(tid))
                else:
                    logger.warning('Replacing template {:d}'.format(tid))
            except KeyError:
                logger.info('Creating template {:d}'.format(tid))

        finally:
            Template.tdict[tid] = self

    @classmethod
    def get(cls, tid):
        """
        Return:
            `Template` or raise `KeyError`
        """
        return cls.tdict[tid]

    @classmethod
    def discard_all(cls):
        """
        Discard all templates
        """
        cls.tdict = {}

    @property
    def types(self):
        return self.tdata[0::2]

    @property
    def lengths(self):
        return self.tdata[1::2]

    def __repr__(self):
        return (
         self.tid, self.tdata)


class OptionsTemplate(Template):
    __doc__ = '\n    Responsibility: represent Options Template Record attributes\n    '

    def __init__(self, tid, tdata, scopelen, optionlen):
        self.tid = tid
        self.tdata = tdata
        self.scopelen = scopelen
        self.optionlen = optionlen
        try:
            try:
                template = Template.tdict[tid]
                if self.__repr__() == template.__repr__():
                    logger.info('Renewing options template {:d}'.format(tid))
                else:
                    logger.warning('Replacing options template {:d}'.format(tid))
            except KeyError:
                logger.info('Creating options template {:d}'.format(tid))

        finally:
            Template.tdict[tid] = self

    def __repr__(self):
        return (self.tid, self.tdata, self.scopelen, self.optionlen)