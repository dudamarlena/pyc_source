# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/vcard/parse.py
# Compiled at: 2012-10-12 07:02:39
import logging, vobject
from coils.core import *
from parse_vcard import parse_vcard

class Parser(object):

    @staticmethod
    def _fix_card(data):
        data = data.strip()
        card = []
        for line in data.splitlines():
            if line[0:8] == 'PROFILE:':
                continue
            else:
                card.append(line)

        return ('\r\n').join(card)

    @staticmethod
    def Parse(data, ctx, **params):
        print 'begin parse'
        log = logging.getLogger('parse')
        result = []
        if data is None:
            raise CoilsException('Attempt to parse a None')
        elif isinstance(data, basestring):
            try:
                data = Parser._fix_card(data)
                log.debug(('VCARD DATA:\n\n{{{0}}}\n\n').format(data))
                card = vobject.readOne(data)
                result.append(parse_vcard(card, ctx, log, **params))
            except Exception, e:
                log.exception(e)
                raise CoilsException('Unable to parse vcard data into components.')

        else:
            raise CoilsException('Non-text data received by vcard parser.')
        print 'end Parse'
        return result