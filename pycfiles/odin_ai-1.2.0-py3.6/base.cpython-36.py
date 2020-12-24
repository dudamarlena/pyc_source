# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/visual/base.py
# Compiled at: 2019-09-19 06:51:53
# Size of source mod 2**32: 3121 bytes
from __future__ import absolute_import, division, print_function
import os
from collections import defaultdict
from typing import Dict, Text
_FIGURE_LIST = defaultdict(dict)

class Visualizer(object):
    __doc__ = ' Visualizer '

    def assert_figure(self, fig):
        from matplotlib import pyplot as plt
        assert isinstance(fig, plt.Figure), 'fig must be instance of matplotlib.Figure, but given: %s' % str(type(fig))
        return fig

    def assert_axis(self, ax):
        from matplotlib import pyplot as plt
        from odin.visual.figures import to_axis
        ax = to_axis(ax)
        assert isinstance(ax, plt.Axes), 'ax must be instance of matplotlib.Axes, but given: %s' % str(type(ax))
        return ax

    def get_figures(self) -> Dict[(Text, 'Figure')]:
        return _FIGURE_LIST[id(self)]

    def add_figure(self, name, fig):
        from matplotlib import pyplot as plt
        self.assert_figure(fig)
        _FIGURE_LIST[id(self)][name] = fig
        return self

    def save_figures(self, path='/tmp/tmp.pdf', dpi=None, separate_files=True, clear_figures=True, verbose=False):
        from odin.utils import ctext
        from matplotlib import pyplot as plt
        if os.path.isfile(path) or '.pdf' == path[-4:].lower():
            separate_files = False
            if not '.pdf' == path[-4:].lower():
                raise AssertionError('If a file is given, it must be PDF file')
        figures = _FIGURE_LIST[id(self)]
        n_figures = len(figures)
        if n_figures == 0:
            return self
        else:
            if verbose:
                print('Saving %s figures to path: ' % ctext(n_figures, 'lightcyan'), ctext(path, 'lightyellow'))
            if not separate_files:
                if dpi is None:
                    dpi = 48
                if '.pdf' not in path:
                    path = path + '.pdf'
                from matplotlib.backends.backend_pdf import PdfPages
                pp = PdfPages(path)
                for key, fig in figures.items():
                    try:
                        fig.savefig(pp, dpi=dpi, format='pdf', bbox_inches='tight')
                        if verbose:
                            print(" - Saved '%s' to pdf file" % ctext(key, 'cyan'))
                    except Exception as e:
                        if verbose:
                            print(" - Error '%s'" % ctext(key, 'cyan'))
                            print('  ', e)

                pp.close()
            else:
                if dpi is None:
                    dpi = 160
                else:
                    if not os.path.exists(path):
                        os.mkdir(path)
                    assert os.path.isdir(path), "'%s' must be path to a folder" % path
                kwargs = dict(dpi=dpi, bbox_inches='tight')
                for key, fig in figures.items():
                    out_path = os.path.join(path, key + '.png')
                    try:
                        (fig.savefig)(out_path, **kwargs)
                        if verbose:
                            print(" - Saved '%s' to %s" % (
                             ctext(key, 'cyan'), ctext(out_path, 'yellow')))
                    except Exception as e:
                        if verbose:
                            print(" - Error '%s'" % ctext(key, 'cyan'))
                            print('  ', e)

            if clear_figures:
                for fig in figures.values():
                    plt.close(fig)

                figures.clear()
            return self