# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tickettree/model.py
# Compiled at: 2011-05-27 11:25:57
import re
from operator import itemgetter
from genshi.builder import tag
from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from trac.ticket.query import Query, TicketQueryMacro
from trac.web.chrome import add_script
from trac.wiki.macros import WikiMacroBase
from trac.wiki.api import WikiSystem, parse_args, IWikiMacroProvider
from trac.wiki.model import WikiPage

class TicketTreeModel(Component):
    """
    Upgrades the environment and creates the initial wiki page containing the TicketTreeMacro.
    """
    implements(IEnvironmentSetupParticipant)

    def environment_created(self):
        self.upgrade_environment()

    def environment_needs_upgrade(self, db=None):
        return self._need_initialization(db) or self._need_upgrade(db)

    def upgrade_environment(self, db=None):
        if self._need_initialization(db):
            try:
                tc_page = WikiPage(self.env, 'TicketTree')
                tc_page.text = '\n= Tickets Tree =\n[[TicketTree()]]\n[[BR]][[BR]][[BR]][[BR]][[BR]][[BR]][[BR]][[BR]]\n                '
                tc_page.save('System', '', '127.0.0.1')
            except:
                db.rollback()
                self.env.log.debug('Exception during upgrade')
                raise

    def _need_initialization(self, db):
        page = WikiPage(self.env, 'TicketTree')
        if page.exists:
            return False
        return True

    def _need_upgrade(self, db):
        return False