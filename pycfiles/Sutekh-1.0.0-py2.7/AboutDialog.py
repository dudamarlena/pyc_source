# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/AboutDialog.py
# Compiled at: 2019-12-11 16:37:54
"""Simple about dialog for Sutekh"""
import gtk
from sutekh.base.Utility import get_database_url
from sutekh.gui import SutekhIcon
from sutekh.SutekhInfo import SutekhInfo

class SutekhAboutDialog(gtk.AboutDialog):
    """About dialog for Sutekh."""

    def __init__(self, *aArgs, **kwargs):
        super(SutekhAboutDialog, self).__init__(*aArgs, **kwargs)
        self.set_name(SutekhInfo.NAME)
        self.set_version(SutekhInfo.VERSION_STR)
        self.set_copyright(SutekhInfo.LICENSE)
        self.set_comments(SutekhInfo.DESCRIPTION)
        self.set_license(SutekhInfo.LICENSE_TEXT)
        self.set_wrap_license(False)
        self.set_website(SutekhInfo.SOURCEFORGE_URL)
        self.set_website_label('Website')
        self.set_authors([ tAuth[0] for tAuth in SutekhInfo.AUTHORS ])
        self.set_documenters([ tAuth[0] for tAuth in SutekhInfo.DOCUMENTERS ])
        self.set_artists([ tAuth[0] for tAuth in SutekhInfo.ARTISTS ])
        self.set_logo(SutekhIcon.SUTEKH_ICON)
        oUrlText = gtk.Label('Database URI: %s' % get_database_url())
        self.vbox.pack_end(oUrlText, False, False)
        oUrlText.show()