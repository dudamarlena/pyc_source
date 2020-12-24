# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/licenses.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 3100 bytes
from collections import namedtuple
License = namedtuple('License', ['abbreviation', 'name', 'uri'])
SORTED_LICENSES = [
 License('All rights reserved', 'No license specified', ''),
 License('CC BY 3.0', 'Creative Commons Attribution Unported 3.0', 'http://creativecommons.org/licenses/by/3.0/'),
 License('CC BY-SA 3.0', 'Creative Commons Attribution-ShareAlike Unported 3.0', 'http://creativecommons.org/licenses/by-sa/3.0/'),
 License('CC BY-ND 3.0', 'Creative Commons Attribution-NoDerivs 3.0 Unported', 'http://creativecommons.org/licenses/by-nd/3.0/'),
 License('CC BY-NC 3.0', 'Creative Commons Attribution-NonCommercial Unported 3.0', 'http://creativecommons.org/licenses/by-nc/3.0/'),
 License('CC BY-NC-SA 3.0', 'Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported', 'http://creativecommons.org/licenses/by-nc-sa/3.0/'),
 License('CC BY-NC-ND 3.0', 'Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported', 'http://creativecommons.org/licenses/by-nc-nd/3.0/'),
 License('CC0 1.0', 'Creative Commons CC0 1.0 Universal', 'http://creativecommons.org/publicdomain/zero/1.0/'),
 License('Public Domain', 'Public Domain', 'http://creativecommons.org/publicdomain/mark/1.0/')]
SUPPORTED_LICENSES = dict((l.uri, l) for l in SORTED_LICENSES)

def get_license_by_url(url):
    """Look up a license by its url and return the License object"""
    try:
        return SUPPORTED_LICENSES[url]
    except KeyError:
        return License(url, url, url)


def licenses_as_choices():
    """List of (uri, abbreviation) tuples for HTML choice field population

    The data seems to be consumed/deleted during usage, so hand over a
    throwaway list, rather than just a generator.
    """
    return [(lic.uri, lic.abbreviation) for lic in SORTED_LICENSES]