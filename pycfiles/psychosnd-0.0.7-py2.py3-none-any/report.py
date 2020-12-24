# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mindhive/dicarlolab/u/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/report.py
# Compiled at: 2016-06-27 12:48:28
__doc__ = 'Creates reports'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys, glob, os, shutil, seaborn as sns

class Report(object):

    def __init__(self, info=None, rp=None, path='', imgdir='img', imgext='svg', actions='make', output='html'):
        self.info = info
        self.rp = rp
        self.path = path
        self.imgdir = imgdir
        self.imgext = imgext
        self.actions = actions
        self.replist = []
        src = os.path.abspath(os.path.dirname(__file__))
        self.resources = os.path.join(src, 'resources/')

    def open(self, reports=None):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        else:
            for root, dirs, files in os.walk(self.path):
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

        with open(self.resources + 'index.html', 'rb') as (tmp):
            self.temp_begin, self.temp_end = tmp.read().split('####REPLACE####')
        self.htmlfile = open(self.path + 'index.html', 'wb')
        self.write(self.temp_begin)

    def close(self):
        self.write(self.temp_end)
        self.htmlfile.close()

    def write(self, text):
        self.htmlfile.write(text)

    def writeh(self, text, h='h1'):
        if isinstance(h, int):
            h = 'h' + str(h)
        self.htmlfile.write('<%s>%s</%s>\n' % (h, text, h))

    def writeimg(self, names, caption=None, win=None):
        if isinstance(names, (str, unicode)):
            names = [
             names]
        fname = ('_').join(names)
        img_path = os.path.join(self.path, self.imgdir)
        fpath = os.path.join(img_path, fname + '.' + self.imgext)
        relpath = os.path.join(self.imgdir, fname + '.' + self.imgext)
        if not os.path.isdir(img_path):
            os.makedirs(img_path)
        if win is not None:
            win.saveMovieFrames(fpath)
        else:
            sns.plt.savefig(fpath, dpi=300, bbox_inches='tight')
        if caption is None:
            caption = (' ').join(names)
        self.htmlfile.write('<figure>\n    <img src="%s" />\n    <figcaption><strong>Figure.</strong> %s</figcaption>\n</figure>\n' % (
         relpath, caption))
        return

    def writetable(self, agg, caption='', fmt=None):
        if fmt is None:
            fmt = '%.3f'
        fmt_lam = lambda x: fmt % x
        import pandas
        table = pandas.DataFrame(agg).to_html(float_format=fmt_lam)
        table = table.replace('class="dataframe"', 'class="dataframe table"')
        self.htmlfile.write('<figure>\n    <figcaption><strong>Table.</strong> %s</figcaption>\n    <div>%s</div>\n</figure>\n' % (
         caption, table))
        return