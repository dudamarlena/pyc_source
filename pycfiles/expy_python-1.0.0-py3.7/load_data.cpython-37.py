# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yousei takei\dir_ep\expy\data\load_data.py
# Compiled at: 2019-10-28 06:05:22
# Size of source mod 2**32: 1793 bytes
import os, shutil
from tqdm import tqdm
HTMLLIST = [
 'basic.tpl', 'full.tpl', 'mathjax.tpl', 'slides_reveal.tpl']
LATEXLIST = ['article.tplx', 'base.tplx', 'style_jupyter.tplx', 'style_notebook.tplx']

class DataLoader:

    def __init__(self):
        self.dir = os.path.abspath(os.path.dirname(__file__))
        self.home = os.environ['USERPROFILE']
        self.expy = os.path.join(os.environ['USERPROFILE'], '.expy')
        self.dir_list = [self.expy] + [os.path.join(self.expy, d) for d in ('html',
                                                                            'latex')]
        self.html_list = [os.path.join('html', f) for f in HTMLLIST]
        self.latex_list = [os.path.join('latex', f) for f in LATEXLIST]
        self.html_temp = os.path.join(self.dir, os.path.join('html', 'basic.tpl'))
        self.latex_temp = os.path.join(self.dir, os.path.join('latex', 'article.tplx'))
        self.file_list = self.html_list + self.latex_list
        self.nofile_list = [f for f in self.file_list if not os.path.isfile(os.path.join(self.expy, f))]

    def __call__(self):
        for d in self.dir_list:
            if os.path.isdir(d) is False:
                os.mkdir(d)

        if self.nofile_list != []:
            for f in self.nofile_list:
                print('\t%s' % f)

            print('already create this file in\t%s?\t[y/n]' % self.expy)
            val = input()
            if val in ('y', 'yes'):
                for f in tqdm(self.nofile_list):
                    shutil.copyfile(os.path.join(self.dir, f), os.path.join(self.expy, f))
                    print('Successfully created %s\tin\t%s' % (f, self.expy))