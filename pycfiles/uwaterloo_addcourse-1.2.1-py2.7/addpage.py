# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/addpage.py
# Compiled at: 2015-05-05 13:59:22
"""Class that interacts with the QUEST course add page."""
import re
from .browser import QuestBrowser

class AddPage(QuestBrowser):
    """Interact with the course add page."""

    def get_add(self):
        """Go to the enrollment page."""
        self.do_action('DERIVED_SSS_SCR_SSS_LINK_ANCHOR3')
        add_link = self.page.find(text='add').parent
        self.make_request(add_link['href'])
        self.get_page()
        t = self.page.find(text=term_regex)
        if t and t.parent.name == 'span':
            self.do_action('DERIVED_SSS_SCT_SSR_PB_GO', {'SSR_DUMMY_RECV1$sels$0': '1'})

    def setup_post(self):
        """Setup a POST request from QUEST."""
        for n in self.page.find_all(name='input', attrs={'type': 'hidden'}):
            self.add_form(n['name'], n['value'])

    def do_action(self, action, d={}):
        """Do a POST action on the add class page."""
        self.make_request(enroll_add_page)
        self.setup_post()
        self.add_form('ICAction', action)
        self.add_forms(d)
        self.get_page()


enroll_add_page = '/psc/AS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL'
term_regex = re.compile('^(Winter|Spring|Fall) [[:digit:]]{4}$')