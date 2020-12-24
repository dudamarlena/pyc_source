# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/performance/superdesk/language/impl/language.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 21, 2012

@package: superdesk
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides unit testing for the language module.
"""
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.container import ioc
from profile import Profile
from superdesk.language.api.language import QLanguage
from superdesk.language.impl.language import LanguageServiceBabelAlchemy
import pstats, unittest

class TestLanguage(unittest.TestCase):

    def testPerformance(self):
        from babel import localedata, core
        localedata._dirname = localedata._dirname.replace('.egg', '')
        core._filename = core._filename.replace('.egg', '')
        languageService = LanguageServiceBabelAlchemy()
        ioc.initialize(languageService)
        profile = Profile()
        qlang = QLanguage(name='rom%')
        try:
            profile = profile.runctx("languageService.getAllAvailable(['en'], 0, 10, qlang)", globals(), locals())
        except SystemExit:
            pass

        pstats.Stats(profile).sort_stats('time', 'cum').print_stats()


if __name__ == '__main__':
    unittest.main()