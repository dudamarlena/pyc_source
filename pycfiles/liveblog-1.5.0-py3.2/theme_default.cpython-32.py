# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/livedesk_embed/theme_default.py
# Compiled at: 2013-10-02 09:54:57
""",
Created on Jan 25, 2013

@package: superdesk media archive
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Publish the theme files.
"""
from ..gui_core.gui_core import cdmGUI, publish
from .theme import theme_folder_format, getThemePath
import logging
log = logging.getLogger(__name__)

def publishThemes(name):
    """
    Publishes themes files
    """
    assert isinstance(name, str), 'Invalid name: %s' % name
    log.info("Published themes '%s'", theme_folder_format() % name)
    cdmGUI().publishFromDir(theme_folder_format() % name, getThemePath())


@publish
def publishDefaultThemes():
    publishThemes('livedesk-embed')