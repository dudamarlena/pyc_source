# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/notebook.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 9502 bytes
"""
IPython/Jupyter Notebook progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.

Usage:
  >>> from tqdm.notebook import trange[, tqdm]
  >>> for i in trange(10): #same as: for i in tqdm(xrange(10))
  ...     ...
"""
from __future__ import division, absolute_import
import sys
from .utils import _range
from .std import tqdm as std_tqdm
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
        warnings.filterwarnings('ignore',
          message='.*The `IPython.html` package has been deprecated.*')
        try:
            import IPython.html.widgets as ipywidgets
        except ImportError:
            pass

try:
    if IPY == 32:
        import IPython.html.widgets as IProgress
        from IPython.html.widgets import HBox, HTML
        IPY = 3
    else:
        from ipywidgets import FloatProgress as IProgress
        from ipywidgets import HBox, HTML
except ImportError:
    try:
        import IPython.html.widgets as IProgress
        import IPython.html.widgets as HBox
        from IPython.html.widgets import HTML
        IPY = 2
    except ImportError:
        IPY = 0

try:
    import IPython.display as display
except ImportError:
    pass

try:
    from html import escape
except ImportError:
    from cgi import escape

__author__ = {'github.com/': ['lrq3000', 'casperdcl', 'alexanderkuk']}
__all__ = ['tqdm_notebook', 'tnrange', 'tqdm', 'trange']

class tqdm_notebook(std_tqdm):
    __doc__ = '\n    Experimental IPython/Jupyter Notebook widget using tqdm!\n    '

    @staticmethod
    def status_printer(_, total=None, desc=None, ncols=None):
        """
        Manage the printing of an IPython/Jupyter Notebook progress bar widget.
        """
        try:
            if total:
                pbar = IProgress(min=0, max=total)
            else:
                pbar = IProgress(min=0, max=1)
                pbar.value = 1
                pbar.bar_style = 'info'
        except NameError:
            raise ImportError('FloatProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html')

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
        return container

    def display(self, msg=None, pos=None, close=False, bar_style=None):
        if not msg:
            if not close:
                msg = self.__repr__()
            else:
                pbar, ptext = self.container.children
                pbar.value = self.n
                if msg:
                    if '<bar/>' in msg:
                        left, right = map(escape, msg.split('<bar/>', 1))
                    else:
                        left, right = '', escape(msg)
                    if left:
                        if left[(-1)] == '|':
                            left = left[:-1]
                    if right:
                        if right[0] == '|':
                            right = right[1:]
                    pbar.description = left
                    if IPYW >= 7:
                        pbar.style.description_width = 'initial'
                    if right:
                        ptext.value = right
            if bar_style:
                pbar.bar_style = pbar.bar_style == 'danger' and bar_style == 'success' or bar_style
        elif close:
            if pbar.bar_style != 'danger':
                try:
                    self.container.close()
                except AttributeError:
                    self.container.visible = False

    def __init__(self, *args, **kwargs):
        file_kwarg = kwargs.get('file', sys.stderr)
        if file_kwarg is sys.stderr or file_kwarg is None:
            kwargs['file'] = sys.stdout
        kwargs['gui'] = True
        kwargs.setdefault('bar_format', '{l_bar}{bar}{r_bar}')
        kwargs['bar_format'] = kwargs['bar_format'].replace('{bar}', '<bar/>')
        kwargs['disable'] = bool(kwargs.get('disable', False))
        (super(tqdm_notebook, self).__init__)(*args, **kwargs)
        if not (self.disable or kwargs['gui']):
            self.sp = lambda *_, **__: None
            return
        self.ncols = '100%' if self.dynamic_ncols else kwargs.get('ncols', None)
        unit_scale = 1 if self.unit_scale is True else self.unit_scale or 1
        total = self.total * unit_scale if self.total else self.total
        self.container = self.status_printer(self.fp, total, self.desc, self.ncols)
        self.sp = self.display
        if not self.disable:
            self.display()

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
            try:
                self.sp(bar_style='danger')
                raise exc
            finally:
                exc = None
                del exc

    def close(self, *args, **kwargs):
        (super(tqdm_notebook, self).close)(*args, **kwargs)
        if self.total and self.n < self.total:
            self.sp(bar_style='danger')
        else:
            if self.leave:
                self.sp(bar_style='success')
            else:
                self.sp(close=True)

    def moveto(self, *args, **kwargs):
        pass

    def reset(self, total=None):
        """
        Resets to 0 iterations for repeated use.

        Consider combining with `leave=True`.

        Parameters
        ----------
        total  : int or float, optional. Total to use for the new bar.
        """
        if total is not None:
            pbar, _ = self.container.children
            pbar.max = total
        return super(tqdm_notebook, self).reset(total=total)


def tnrange(*args, **kwargs):
    """
    A shortcut for `tqdm.notebook.tqdm(xrange(*args), **kwargs)`.
    On Python3+, `range` is used instead of `xrange`.
    """
    return tqdm_notebook(_range(*args), **kwargs)


tqdm = tqdm_notebook
trange = tnrange