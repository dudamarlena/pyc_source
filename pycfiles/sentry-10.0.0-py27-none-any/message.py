# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/grouping/strategies/message.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import re, six
from itertools import islice
from sentry.grouping.component import GroupingComponent
from sentry.grouping.strategies.base import strategy
_irrelevant_re = re.compile("(?x)\n    (?P<email>\n        [a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*\n    ) |\n    (?P<url>\n        \\b(wss?|https?|ftp)://[^\\s/$.?#].[^\\s]*\n    ) |\n    (?P<ip>\n        (\n            ([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|\n            ([0-9a-fA-F]{1,4}:){1,7}:|\n            ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|\n            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|\n            ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|\n            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|\n            ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|\n            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|\n            :((:[0-9a-fA-F]{1,4}){1,7}|:)|\n            fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|\n            ::(ffff(:0{1,4}){0,1}:){0,1}\n            ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}\n            (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|\n            ([0-9a-fA-F]{1,4}:){1,4}:\n            ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}\n            (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\b\n        ) |\n        (\n            \\b((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}\n            (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\b\n        )\n    ) |\n    (?P<uuid>\n        \\b\n            [0-9a-fA-F]{8}-\n            [0-9a-fA-F]{4}-\n            [0-9a-fA-F]{4}-\n            [0-9a-fA-F]{4}-\n            [0-9a-fA-F]{12}\n        \\b\n    ) |\n    (?P<sha1>\n        \\b[0-9a-fA-F]{40}\\b\n    ) |\n    (?P<md5>\n        \\b[0-9a-fA-F]{32}\\b\n    ) |\n    (?P<date>\n        (\n            (\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d:[0-5]\\d\\.\\d+([+-][0-2]\\d:[0-5]\\d|Z))|\n            (\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d:[0-5]\\d([+-][0-2]\\d:[0-5]\\d|Z))|\n            (\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d([+-][0-2]\\d:[0-5]\\d|Z))\n        ) |\n        (\n            \\b(?:(Sun|Mon|Tue|Wed|Thu|Fri|Sat)\\s+)?\n            (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+\n            ([\\d]{1,2})\\s+\n            ([\\d]{2}:[\\d]{2}:[\\d]{2})\\s+\n            [\\d]{4}\n        ) |\n        (\n            \\b(?:(Sun|Mon|Tue|Wed|Thu|Fri|Sat),\\s+)?\n            (0[1-9]|[1-2]?[\\d]|3[01])\\s+\n            (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+\n            (19[\\d]{2}|[2-9][\\d]{3})\\s+\n            (2[0-3]|[0-1][\\d]):([0-5][\\d])\n            (?::(60|[0-5][\\d]))?\\s+\n            ([-\\+][\\d]{2}[0-5][\\d]|(?:UT|GMT|(?:E|C|M|P)(?:ST|DT)|[A-IK-Z]))\n        )\n    ) |\n    (?P<float>\n        -\\d+\\.\\d+\\b |\n        \\b\\d+\\.\\d+\\b\n    ) |\n    (?P<int>\n        -\\d+\\b |\n        \\b\\d+\\b\n    )\n")

def trim_message_for_grouping(string):
    s = ('\n').join(islice((x for x in string.splitlines() if x.strip()), 2)).strip()
    if s != string:
        s += '...'

    def _handle_match(match):
        for key, value in six.iteritems(match.groupdict()):
            if value is not None:
                return '<%s>' % key

        return ''

    return _irrelevant_re.sub(_handle_match, s)


@strategy(id='message:v1', interfaces=['message'], variants=['default'], score=0)
def message_v1(message_interface, **meta):
    return GroupingComponent(id='message', values=[message_interface.message or message_interface.formatted])


@strategy(id='message:v2', interfaces=['message'], variants=['default'], score=0)
def message_v2(message_interface, **meta):
    message_in = message_interface.message or message_interface.formatted
    message_trimmed = trim_message_for_grouping(message_in)
    hint = 'stripped common values' if message_in != message_trimmed else None
    return GroupingComponent(id='message', values=[message_trimmed], hint=hint)