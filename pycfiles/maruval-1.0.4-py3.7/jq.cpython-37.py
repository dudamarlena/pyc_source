# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maruval/jq.py
# Compiled at: 2019-07-31 05:43:03
# Size of source mod 2**32: 929 bytes
import os, stat, sys
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

WINLINK = 'https://stedolan.github.io/jq/'
RELEASE = 'https://github.com/stedolan/jq/releases/download/jq-1.6'
LINKS = dict(linux=(
 '{}/jq-linux64'.format(RELEASE), '/usr/bin/jq'),
  darwin=(
 '{}/jq-osx-amd64'.format(RELEASE), '/usr/local/bin/jq'))

def configure():
    """
    Installs jq.

    Usage: sudo python -m maruval.jq
    """
    print('Configuring jq...')
    try:
        url, dest = LINKS[sys.platform]
    except KeyError:
        msg = 'Cannot autoinstall jq for {}. Do it yourself via {}'.format(sys.platform, WINLINK)
        raise OSError(msg)

    urlretrieve(url, dest)
    os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
    print('Installed jq to {}'.format(dest))


if __name__ == '__main__':
    configure()