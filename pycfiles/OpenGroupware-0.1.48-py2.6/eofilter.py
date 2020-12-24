# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/zogi/eofilter.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import NotImplementedException

def process_eo_filter(results_in, filter_string):
    if not filter_string:
        return results_in
    else:
        results_out = []
        print filter_string
        if filter_string == '(isAccount=1)':
            for result in results_in:
                print result['isAccount']
                if result.get('isAccount', None) == 1:
                    results_out.append(result)

        else:
            raise NotImplementedException('EOFilter support not yet implemented; patches welcome.')
        return results_out