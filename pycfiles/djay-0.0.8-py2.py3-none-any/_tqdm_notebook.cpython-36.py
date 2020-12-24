# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tqdm/tqdm/_tqdm_notebook.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 9938 bytes
"""
IPython/Jupyter Notebook progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.

Usage:
  >>> from tqdm import tnrange[, tqdm_notebook]
  >>> for i in tnrange(10): #same as: for i in tqdm_notebook(xrange(10))
  ...     ...
"""
from __future__ import division, absolute_import
import sys
from ._utils import _range
from ._tqdm import tqdm
IPY = 0
IPYW = 0
try:
    import ipywidgets
    IPY = 4
    try:
        IPYW = int(ipywidgets.__version__.split('.')[0])
    except AttributeError:
        pass

except ImportError:
    IPY = 32
    import warnings
    with warnings.catch_warnings():
        ipy_deprecation_msg = 'The `IPython.html` package has been deprecated'
        warnings.filterwarnings('error', message=('.*' + ipy_deprecation_msg + '.*'))
        try:
            import IPython.html.widgets as ipywidgets
        except Warning as e:
            if ipy_deprecation_msg not in str(e):
                raise
            warnings.simplefilter('ignore')
            try:
                import IPython.html.widgets as ipywidgets
            except ImportError:
                pass

        except ImportError:
            pass

try:
    if IPY == 32:
        from IPython.html.widgets import IntProgress, HBox, HTML
        IPY = 3
    else:
        from ipywidgets import IntProgress, HBox, HTML
except ImportError:
    try:
        from IPython.html.widgets import IntProgressWidget as IntProgress
        from IPython.html.widgets import ContainerWidget as HBox
        from IPython.html.widgets import HTML
        IPY = 2
    except ImportError:
        IPY = 0

try:
    from IPython.display import display
except ImportError:
    pass

try:
    from html import escape
except ImportError:
    from cgi import escape

__author__ = {'github.com/': ['lrq3000', 'casperdcl', 'alexanderkuk']}
__all__ = ['tqdm_notebook', 'tnrange']

class tqdm_notebook(tqdm):
    __doc__ = '\n    Experimental IPython/Jupyter Notebook widget using tqdm!\n    '

    @staticmethod
    def status_printer(_, total=None, desc=None, ncols=None):
        """
        Manage the printing of an IPython/Jupyter Notebook progress bar widget.
        """
        try:
            if total:
                pbar = IntProgress(min=0, max=total)
            else:
                pbar = IntProgress(min=0, max=1)
                pbar.value = 1
                pbar.bar_style = 'info'
        except NameError:
            raise ImportError('IntProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html')

        if desc:
            pbar.description = desc
            if IPYW >= 7:
                pbar.style.description_width = 'initial'
        ptext = HTML()
        container = HBox(children=[pbar, ptext])
        if ncols is not None:
            ncols = str(ncols)
            try:
                if int(ncols) > 0:
                    ncols += 'px'
            except ValueError:
                pass

            pbar.layout.flex = '2'
            container.layout.width = ncols
            container.layout.display = 'inline-flex'
            container.layout.flex_flow = 'row wrap'
        display(container)

        def print_status(s='', close=False, bar_style=None, desc=None):
            if total:
                if s:
                    npos = s.find('/|/')
                    if npos >= 0:
                        n = float(s[:npos])
                        s = s[npos + 3:]
                        if n is not None:
                            pbar.value = n
                    if s:
                        s = s.replace('||', '')
                        s = escape(s)
                        ptext.value = s
                    if bar_style:
                        pbar.bar_style = pbar.bar_style == 'danger' and bar_style == 'success' or bar_style
                else:
                    if close:
                        if pbar.bar_style != 'danger':
                            try:
                                container.close()
                            except AttributeError:
                                container.visible = False

            else:
                if desc:
                    pbar.description = desc
                    if IPYW >= 7:
                        pbar.style.description_width = 'initial'

        return print_status

    def __init__(self, *args, **kwargs):
        if kwargs.get('file', sys.stderr) is sys.stderr:
            kwargs['file'] = sys.stdout
        else:
            if not kwargs.get('bar_format', None):
                kwargs['bar_format'] = '{n}/|/{l_bar}{r_bar}'
            kwargs['gui'] = True
            (super(tqdm_notebook, self).__init__)(*args, **kwargs)
            if self.disable or not kwargs['gui']:
                return
            self.ncols = '100%' if self.dynamic_ncols else kwargs.get('ncols', None)
            unit_scale = 1 if self.unit_scale is True else self.unit_scale or 1
            total = self.total * unit_scale if self.total else self.total
            self.sp = self.status_printer(self.fp, total, self.desc, self.ncols)
            self.desc = None
            if not self.disable:
                self.sp(self.__repr__())

    def __iter__(self, *args, **kwargs):
        try:
            for obj in (super(tqdm_notebook, self).__iter__)(*args, **kwargs):
                yield obj

        except:
            self.sp(bar_style='danger')
            raise

    def update(self, *args, **kwargs):
        try:
            (super(tqdm_notebook, self).update)(*args, **kwargs)
        except Exception as exc:
            self.sp(bar_style='danger')
            raise exc

    def close(self, *args, **kwargs):
        (super(tqdm_notebook, self).close)(*args, **kwargs)
        if hasattr(self, 'sp'):
            if self.total:
                if self.n < self.total:
                    self.sp(bar_style='danger')
            else:
                if self.leave:
                    self.sp(bar_style='success')
                else:
                    self.sp(close=True)

    def moveto(self, *args, **kwargs):
        pass

    def set_description(self, desc=None, **_):
        """
        Set/modify description of the progress bar.

        Parameters
        ----------
        desc  : str, optional
        """
        self.sp(desc=desc)


def tnrange(*args, **kwargs):
    """
    A shortcut for tqdm_notebook(xrange(*args), **kwargs).
    On Python3+ range is used instead of xrange.
    """
    return tqdm_notebook(_range(*args), **kwargs)