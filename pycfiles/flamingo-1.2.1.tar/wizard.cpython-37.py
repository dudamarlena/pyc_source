# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/wizard.py
# Compiled at: 2020-04-05 11:37:36
# Size of source mod 2**32: 3563 bytes
from dialog import Dialog
from flamingo.core.context import Context
import flamingo

class Wizard:
    EXIT = 0
    BACK = 1

    def __init__(self, settings):
        self.settings = settings
        self._context = None
        self.dialog = Dialog(dialog='dialog')
        self.dialog.set_background_title('flamingo {} wizard'.format(flamingo.VERSION_STRING))
        self.menu = [
         [
          'Add new content',
          [
           [
            'Create a page', self.create_page],
           [
            'Create a blog post', self.create_blog_post]]],
         [
          'Edit content', self.edit_content],
         [
          'Start an interactive shell', self.start_shell],
         [
          'Exit', self.EXIT]]
        self.menu_title = [
         'Menu']
        self.cursor = [self.menu]

    def menu_back(self):
        self.cursor = self.cursor[:-1]
        self.menu_title = self.menu_title[:-1]

    def main_menu(self):
        while 1:
            choices = []
            actions = {}
            for item in self.cursor[(-1)]:
                choice = item[0]
                if not isinstance(choice, tuple):
                    choice = (
                     choice, '')
                choices.append(choice)
                actions[choice[0]] = item[1]

            if len(self.cursor) > 1:
                choices.append(('Back', ''))
                actions['Back'] = self.BACK
            else:
                code, tag = self.dialog.menu((' > '.join(self.menu_title)), choices=choices)
                if code in 'cancel':
                    if self.cursor == [self.menu]:
                        return
                    self.menu_back()
            if code == 'esc' or actions[tag] is self.BACK:
                self.menu_back()
            elif actions[tag] is self.EXIT:
                return
                if isinstance(actions[tag], list):
                    self.menu_title.append(tag)
                    self.cursor.append(actions[tag])
                    continue
            elif callable(actions[tag]):
                actions[tag]()

    def run(self):
        self.main_menu()

    @property
    def context(self):
        if not self._context:
            self.dialog.infobox('Setting up flamingo context',
              title='Please wait')
            self._context = Context(self.settings)
        return self._context

    def find_content_by_url(self):
        choices = []
        for content in self.context.contents:
            title = content['title'] or content['content_title']
            url = content['url'] or ''
            if not title:
                continue
            choices.append((url, ''))

        code, tag = self.dialog.menu('Choose URL', choices=choices)

    def start_shell(self):
        import IPython
        IPython.embed()

    def create_page(self):
        self.context
        self.dialog.msgbox('create page')

    def create_blog_post(self):
        self.dialog.msgbox('create blog post')

    def edit_content(self):
        self.find_content_by_url()