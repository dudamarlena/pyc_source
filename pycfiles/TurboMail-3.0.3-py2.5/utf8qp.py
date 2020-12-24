# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/extensions/utf8qp.py
# Compiled at: 2009-11-05 11:33:46
"""TurboMail UTF-8 quoted-printable encoding extension."""
import logging
from turbomail.api import Extension
from turbomail.compat import charset
__all__ = [
 'interface', 'UTF8QuotedPrintable']
log = logging.getLogger('turbomail.extension.utf8qp')

class UTF8QuotedPrintable(Extension):
    name = 'utf8qp'

    def start(self):
        super(UTF8QuotedPrintable, self).start()
        log.info('Configuring UTF-8 character set to use Quoted-Printable encoding.')
        charset.add_charset('utf-8', charset.SHORTEST, charset.QP, 'utf-8')
        charset.add_charset('utf8', charset.SHORTEST, charset.QP, 'utf8')

    def stop(self):
        super(UTF8QuotedPrintable, self).stop()
        log.info('Configuring UTF-8 character set to use Base-64 encoding.')
        charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')
        charset.add_charset('utf8', charset.SHORTEST, charset.BASE64, 'utf8')


interface = UTF8QuotedPrintable()