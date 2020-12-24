# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/wsgram.py
# Compiled at: 2010-04-29 16:01:18
"""
Simplified Globus Toolkit GT4 WS-GRAM log parser

Typical input line:
-----------------------------------------------------------------------
2008-02-05 11:16:04,071 WARN  utils.JavaUtils [main,isAttachmentSupported:1218] Unable to find required classes (javax.activation.DataHandler and javax.mail.internet.MimeMultipart). Attachment support is disabled.
-----------------------------------------------------------------------
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: wsgram.py 24755 2010-04-29 20:01:18Z dang $'
import re
from netlogger.parsers.base import BaseParser, parseDate

def _ns(e):
    return 'globus.ws-gram.%s' % e


class Parser(BaseParser):
    """Globus Toolkit GT4 WS-GRAM log parser
    See also http://www.globus.org/toolkit/docs/4.0/execution/wsgram/developer-index.html.
    """
    RE = re.compile('(?P<date>\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d,\\d\\d\\d)\\s+(?P<level>\\w+)\\s+(?P<class>\\S+)\\s+\\[(?P<thread>[^,]+),(?P<file>[^:]+):(?P<line>\\d+)\\]\\s+(?P<msg>.*)')
    MSG_RE = {'auth.invoke': 'Authorized "(?P<DN>.*?)" to invoke "(?P<target>.*?)"', 
       'auth.user': 'Peer "(?P<DN>.*)" authorized as "(?P<user>.*)"', 
       'service': '[Ss]ervice (?P<name>.*)', 
       'read.registration.default': 'Reading default registration.*?: (?P<file>.*)', 
       'job.start': 'Job (?P<job__id>\\S+) accepted for local user ' + "'(?P<user>\\S+)'", 
       'job.end': 'Job (?P<job__id>\\S+) (finished successfully|failed)'}
    for k in MSG_RE.keys():
        MSG_RE[k] = re.compile(MSG_RE[k])

    def __init__(self, f, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)

    def process(self, line):
        m = self.RE.match(line)
        if not m:
            return (dict(event=_ns('unknown'), msg=line),)
        d = m.groupdict()
        d['ts'] = _parseDate(d['date'])
        del d['date']
        d['level'] = d['level'].title()
        d['msg'] = d['msg'].replace('\\"', '"').replace("\\'", "'")
        msg = d['msg']
        for (suffix, regex) in self.MSG_RE.items():
            m = regex.match(msg)
            if m:
                for (n, v) in m.groupdict().items():
                    k = n.replace('__', '.')
                    if suffix == 'job.end':
                        status_msg = m.group(2)
                        if status_msg == 'finished successfully':
                            d['status'] = 0
                        else:
                            d['status'] = -1
                    d[k] = v

                d['event'] = _ns(suffix)
                del d['msg']
                break

        return (
         d,)


def _parseDate(s):
    bp_ts = s[:10] + 'T' + s[11:19] + '.' + s[20:] + 'Z'
    return parseDate(bp_ts)