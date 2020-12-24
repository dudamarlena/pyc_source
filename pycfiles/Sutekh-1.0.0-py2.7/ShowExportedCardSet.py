# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ShowExportedCardSet.py
# Compiled at: 2019-12-11 16:37:54
"""Plugin for displaying the exported version of a card set in a gtk.TextView.
   Intended to make cutting and pasting easier."""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.plugins.BaseShowExported import BaseShowExported
from sutekh.io.WriteJOL import WriteJOL
from sutekh.io.WriteLackeyCCG import WriteLackeyCCG
from sutekh.io.WriteELDBDeckFile import WriteELDBDeckFile
from sutekh.io.WriteArdbText import WriteArdbText
from sutekh.io.WritePmwiki import WritePmwiki
from sutekh.io.WriteVEKNForum import WriteVEKNForum
from sutekh.io.WriteSLDeck import WriteSLDeck

class ShowExported(SutekhPlugin, BaseShowExported):
    """Display the various exported versions of a card set."""
    EXPORTERS = BaseShowExported.EXPORTERS.copy()
    EXPORTERS.update({'Export to JOL format': WriteJOL, 
       'Export to Lackey CCG format': WriteLackeyCCG, 
       'Export to ARDB Text': WriteArdbText, 
       'BBcode output for the V:EKN Forums': WriteVEKNForum, 
       'Export to ELDB ELD Deck File': WriteELDBDeckFile, 
       'Export to pmwiki': WritePmwiki, 
       'Export for SL import form': WriteSLDeck})


plugin = ShowExported