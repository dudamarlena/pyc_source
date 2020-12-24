# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/config.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import logging
from pyogp.lib.client.settings import Settings
settings = Settings()
debug = settings.ENABLE_LOGGING_IN_TESTS
if debug:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)-30s%(name)-15s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)
    logger = logging.getLogger('pyogp.lib.base.tests.helpers')
    logger.debug('setting debug to True')