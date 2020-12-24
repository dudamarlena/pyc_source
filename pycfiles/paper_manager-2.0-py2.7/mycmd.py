# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cer/Project/pycharm/paper_manager/paper_manager/mycmd.py
# Compiled at: 2018-04-14 05:20:12
from __future__ import print_function
import cmd
from paper_manager.color import Colored, colors
from paper_manager.manager import Manager
logo_str_1 = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
logo_str_2 = '\n%%%      %%%%    %%%%%%%    %%\n%%%%   %%%  %%%   %%%%%%   %%%\n%%%%   %%%  .%%   -%%%% .  %%%\n%%%%   %%%  %%% %  %%%.=.  %%%\n%%%%      -%%%% %   %% %.  %%%\n%%%%   %%%%%%%% %%  = %%.  %%%\n%%%%   %%%%%%%% %%%  %%%.  %%%\n%%%%   %%%%%%%% %%%  %%%   %%%\n'
logo_str_3 = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
help_str = '\n\n     select_rep select or create a repository to operate\n     delete_rep delete a repository\n     cur_rep    show current repository\n     refresh    refresh a repository\n     rec        recommend the papers according to urgency and importance\n     all        show all the papers info\n     tags       show all tags\n     sbt        search by tags, like (sbt tag1 tg2)\n     sbn        search by id nums, like (sbn 1 2)\n     edit       edit one paper info by paper id, like (edit 1)\n     path       find path by paper id, like (path 1 2)\n     open       open paper to read by id, like (open 1)\n     help       help info\n     quit       exit the manager\n     \n     '

class MyCmd(cmd.Cmd):
    """my command processor"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.color = Colored()
        self.manager = Manager(self.color)
        self.prompt = '(manager)>'
        self.intro = self.color.yellow(logo_str_1) + self.color.cyan(logo_str_2) + self.color.yellow(logo_str_3 + '\n') + self.color.red('Paper Manager Usage：') + help_str
        self.manager.refresh()

    def do_select_rep(self, arg):
        self.manager.select_repository()

    def help_select_rep(self):
        print('select or create a repository to operate')

    def do_delete_rep(self, arg):
        self.manager.delete_repository()

    def help_delete_rep(self):
        print('delete a repository')

    def do_cur_rep(self, arg):
        print('current repository, name:', self.manager.cur_rep.name, ' path:', self.manager.cur_rep.path, ' support_suffix:', self.manager.cur_rep.support_suffix)

    def help_cur_rep(self):
        print('show current repository')

    def help_refresh(self):
        print('refresh a repository')

    def do_refresh(self, arg):
        self.manager.refresh()

    def help_refresh(self):
        print('refresh a repository')

    def do_rec(self, arg):
        self.manager.recommend_papers()

    def help_rec(self):
        print('recommend the papers according to urgency and importance')

    def do_all(self, arg):
        recs = self.manager.cursor.execute(('SELECT * FROM {} ').format(self.manager.cur_rep.name)).fetchall()
        self.manager.print_papers(recs)

    def help_all(self):
        print('show all the papers info')

    def do_tags(self, arg):
        self.manager.show_tags()

    def help_tags(self):
        print('show all tags')

    def do_sbt(self, arg):
        self.manager.query_by_tags(arg)

    def help_sbt(self):
        print('search by tags, like (sbt tag1 tg2)')

    def do_sbn(self, arg):
        self.manager.query_by_nums(arg)

    def help_sbn(self):
        print('search by id nums, like (sbn 1 2)')

    def do_edit(self, arg):
        self.manager.edit_one_paper(arg)

    def help_edit(self):
        print("edit one paper info by paper id, like (edit 1),\nuse 'all' or 'tags' to see the id of your paper.")

    def do_path(self, arg):
        self.manager.print_path_by_nums(arg)

    def help_path(self):
        print('find path by paper id, like (path 1 2)')

    def do_open(self, arg):
        self.manager.open_paper_by_num(arg)

    def help_open(self):
        print('open paper to read by id, like (open 1)')

    def do_quit(self, arg):
        print(self.color.yellow('Bye ...'))
        self.manager.quit_manager()
        exit(0)

    def help_quit(self):
        print('exit the manager')