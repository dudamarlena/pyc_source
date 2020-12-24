# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matthew/Documents/rets/env/lib/python3.8/site-packages/rets/utils/get_object.py
# Compiled at: 2020-05-12 16:31:32
# Size of source mod 2**32: 1178 bytes
import re

class GetObject(object):
    __doc__ = 'Handles various formatting for the GetObject metadata request'

    def ids(self, content_ids, object_ids):
        """Appends the content and object ids how RETS expects them"""
        content_ids = self.split(content_ids, False)
        object_ids = self.split(object_ids)
        for cid in content_ids:
            yield '{}:{}'.format(cid, ':'.join(object_ids))

    @staticmethod
    def split(value, dash_ranges=True):
        """Splits """
        if isinstance(value, list):
            value = [str(v) for v in value]
        else:
            str_value = str(value)
            dash_matches = re.match(pattern='(\\d+)\\-(\\d+)', string=str_value)
            if ':' in str_value or ',' in str_value:
                value = [v.strip() for v in str_value.replace(',', ':').split(':')]
            else:
                if dash_ranges and dash_matches:
                    start_range = int(dash_matches.group(1))
                    end_range = int(dash_matches.group(2)) + 1
                    rng = range(start_range, end_range)
                    value = [str(r) for r in rng]
                else:
                    value = [
                     str_value]
        return value