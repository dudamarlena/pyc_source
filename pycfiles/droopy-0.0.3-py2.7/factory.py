# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\factory.py
# Compiled at: 2011-10-24 15:37:44
from droopy import Droopy
from droopy.static import Static
from droopy.readability import Readability
from droopy.filters import TextFilter

class DroopyFactory(object):

    @staticmethod
    def create_full_droopy(text, lang_bundle=None):
        """Creates droopy with all available bundles"""
        droopy = Droopy(text)
        for bundle in DroopyFactory.get_all_available_bundles():
            droopy.add_bundles(bundle)

        if lang_bundle:
            droopy.add_bundles(lang_bundle)
        return droopy

    @staticmethod
    def get_all_available_bundles():
        return [Static(), Readability(), TextFilter()]