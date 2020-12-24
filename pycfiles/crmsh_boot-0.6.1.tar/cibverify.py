# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/cibverify.py
# Compiled at: 2016-05-04 07:56:27
import re
from . import utils
from .msg import err_buf
cib_verify = 'crm_verify --verbose -p'
VALIDATE_RE = re.compile('^Entity: line (\\d)+: element (\\w+): ' + 'Relax-NG validity error : (.+)$')

def _prettify(line, indent=0):
    m = VALIDATE_RE.match(line)
    if m:
        return '%s%s (%s): %s' % (indent * ' ', m.group(2), m.group(1), m.group(3))
    return line


def verify(cib):
    rc, _, stderr = utils.get_stdout_stderr(cib_verify, cib)
    for i, line in enumerate(line for line in stderr.split('\n') if line):
        if i == 0:
            err_buf.error(_prettify(line, 0))
        else:
            err_buf.writemsg(_prettify(line, 7))

    return rc