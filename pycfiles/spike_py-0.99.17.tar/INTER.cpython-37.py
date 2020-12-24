# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/Notebooks/spike/Interactive/INTER.py
# Compiled at: 2020-03-02 15:48:27
# Size of source mod 2**32: 55480 bytes
"""
A set of utilities to use spike in NMR or FTMS within jupyter

First version MAD june 2017
definitive ? version MAD october 2019

"""
from __future__ import print_function, division
import unittest, sys, os
import os.path as op
import glob
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import MultiCursor
from ipywidgets import fixed, Layout, HBox, VBox, Label, Output, Button, Tab
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import numpy as np
from File.BrukerNMR import Import_1D
from .. import NPKData
from ..NMR import NMRData
try:
    import spike.plugins.bcorr as bcorr
except:
    print('Baseline correction plugins not installed !')

REACTIVE = True
HEAVY = False

def hidecode(initial='show', message=True):
    """
    this func adds a button to hide/show the code on a jupyter page
    initial is either 'show' or 'hide'
    inspired from: https://stackoverflow.com/questions/27934885/how-to-hide-code-from-cells-in-ipython-notebook-visualized-with-nbviewer/28073228#28073228
    """
    from IPython.display import display, HTML, Markdown
    if initial == 'show':
        init = 'false'
    else:
        if initial == 'hide':
            init = 'true'
        elif message:
            msg = '<i>usefull to show/print a clean screen when processing is finished</i>'
        else:
            msg = ''
        display(HTML('\n<style>hr {height: 2px; border: 0;border-top: 1px solid #ccc;margin: 1em 0;padding: 0; }</style>\n<script>\ncode_show=%s; \nfunction code_toggle()\n    { if (code_show)\n        { $(\'div.input\').hide(); $(\'#but\').val("show python code");\n        } else { $(\'div.input\').show(); $(\'#but\').val("hide python code");\n    }\n    code_show = !code_show } \n$(document).ready(code_toggle);\n</script>\n<form action="javascript:code_toggle()">\n<input id="but" type="submit" style="border:1px solid black; background-color:#DDD">\n%s\n</form>' % (init, msg)))


def jsalert(msg):
    """send a javascript alert"""
    display(Javascript("alert('%s')" % msg))


class FileChooser:
    __doc__ = 'a simple file chooser for Jupyter - obsolete - not used'

    def __init__(self, base=None, filetype=['fid', 'ser'], mode='r', show=True):
        if base is None:
            self.curdir = '/'
        else:
            self.curdir = base
        self.filetype = filetype
        self.mode = mode
        self.wfile = widgets.Text(layout=Layout(width='70%'), description='File to load')
        self.ldir = widgets.Label(value=('Chosen dir:  ' + self.curdir))
        self.wdir = widgets.Select(options=(self.dirlist()),
          description='Choose Dir',
          layout=Layout(width='70%'))
        if mode == 'r':
            self.wchooser = widgets.Select(options=(self.filelist()),
              description='Choose File',
              layout=Layout(width='70%'))
            self.wchooser.observe(self.wob)
            self.wfile.disabled = True
        else:
            if mode == 'w':
                self.wfile.description = 'File to create'
                self.wfile.disabled = False
                self.wchooser = widgets.Select(options=(self.filelist()),
                  description='Files',
                  layout=Layout(width='70%'))
            else:
                raise Exception('Only "r" and  "w" modes supported')
        self.wsetdir = Button(description='❯', layout=Layout(width='20%'), button_style='success',
          tooltip='descend in directory')
        self.wup = Button(description='❮', layout=Layout(width='20%'), button_style='success',
          tooltip='up to previous directory')
        self.wsetdir.on_click(self.setdir)
        self.wup.on_click(self.updir)
        if show:
            self.show()

    def filelist--- This code section failed: ---

 L. 117         0  BUILD_LIST_0          0 
                2  STORE_FAST               'fl'

 L. 118         4  LOAD_FAST                'self'
                6  LOAD_ATTR                mode
                8  LOAD_STR                 'r'
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE   122  'to 122'

 L. 119        14  LOAD_GLOBAL              type
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                filetype
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_GLOBAL              str
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    52  'to 52'

 L. 120        28  LOAD_GLOBAL              glob
               30  LOAD_METHOD              glob
               32  LOAD_GLOBAL              op
               34  LOAD_METHOD              join
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                curdir
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                filetype
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  STORE_FAST               'fl'
               50  JUMP_ABSOLUTE       172  'to 172'
             52_0  COME_FROM            26  '26'

 L. 121        52  LOAD_GLOBAL              type
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                filetype
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  LOAD_GLOBAL              tuple
               62  LOAD_GLOBAL              list
               64  BUILD_TUPLE_2         2 
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE   112  'to 112'

 L. 122        70  SETUP_LOOP          120  'to 120'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                filetype
               76  GET_ITER         
               78  FOR_ITER            108  'to 108'
               80  STORE_FAST               'f'

 L. 123        82  LOAD_FAST                'fl'
               84  LOAD_GLOBAL              glob
               86  LOAD_METHOD              glob
               88  LOAD_GLOBAL              op
               90  LOAD_METHOD              join
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                curdir
               96  LOAD_FAST                'f'
               98  CALL_METHOD_2         2  '2 positional arguments'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  INPLACE_ADD      
              104  STORE_FAST               'fl'
              106  JUMP_BACK            78  'to 78'
              108  POP_BLOCK        
              110  JUMP_ABSOLUTE       172  'to 172'
            112_0  COME_FROM            68  '68'

 L. 125       112  LOAD_GLOBAL              Exception
              114  LOAD_STR                 'TypeError, filetype should be either a string or a list'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM_LOOP       70  '70'
              120  JUMP_FORWARD        172  'to 172'
            122_0  COME_FROM            12  '12'

 L. 127       122  LOAD_LISTCOMP            '<code_object <listcomp>>'
              124  LOAD_STR                 'FileChooser.filelist.<locals>.<listcomp>'
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              128  LOAD_GLOBAL              glob
              130  LOAD_METHOD              glob
              132  LOAD_GLOBAL              op
              134  LOAD_METHOD              join
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                curdir
              140  LOAD_STR                 '*'
              142  CALL_METHOD_2         2  '2 positional arguments'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  GET_ITER         
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  STORE_FAST               'fl'

 L. 128       152  LOAD_GLOBAL              op
              154  LOAD_METHOD              join
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                curdir
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                filetype
              164  CALL_METHOD_2         2  '2 positional arguments'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                wfile
              170  STORE_ATTR               value
            172_0  COME_FROM           120  '120'

 L. 129       172  LOAD_FAST                'fl'
              174  BUILD_LIST_0          0 
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   186  'to 186'

 L. 130       180  LOAD_STR                 ' '
              182  BUILD_LIST_1          1 
              184  STORE_FAST               'fl'
            186_0  COME_FROM           178  '178'

 L. 131       186  LOAD_FAST                'fl'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 120_0

    def dirlist(self):
        base = self.curdir
        return [d for d in glob.glob(op.joinbase'*') if op.isdir(d) if not d.endswith('__pycache__')]

    def wob(self, e):
        self.wfile.value = self.wchooser.value

    def updir(self, e):
        self.curdir = op.dirname(self.curdir)
        self.ldir.value = 'Chosen dir:  ' + self.curdir
        self.wdir.options = self.dirlist()
        self.wchooser.options = self.filelist()

    def setdir(self, e):
        self.curdir = self.wdir.value
        self.ldir.value = 'Chosen dir:  ' + self.curdir
        self.wdir.options = self.dirlist()
        self.wchooser.options = self.filelist()

    def show(self):
        display(VBox([
         self.ldir,
         HBox([self.wdir, VBox([self.wup, self.wsetdir])]),
         self.wchooser,
         self.wfile]))
        return self

    @property
    def file(self):
        """the chosen complete filename"""
        return self.wfile.value

    @property
    def dirname(self):
        """the final dirname containing the chosen file"""
        if op.isdir(self.wfile.value):
            return op.basename(self.wfile.value)
        return op.basename(op.dirname(self.wfile.value))

    @property
    def nmrname(self):
        """the final dirname containing the chosen file for TopSpin files"""
        if op.isdir(self.wfile.value):
            return op.joinop.basename(op.dirname(self.wfile.value))self.dirname
        return op.joinop.basename(op.dirname(op.dirname(self.wfile.value)))self.dirname

    @property
    def basename(self):
        """the basename of the chosen file"""
        return op.basename(self.wfile.value)


class Show1D(HBox):
    __doc__ = '\n    An interactive display, 1D NMR\n        Show1D(spectrum)\n    to be developped for peaks and integrals\n    '

    def __init__(self, data, title=None, figsize=None, reverse_scroll=False, show=True):
        """
        data : to be displayed
        title : text for window
        figsize : size in inches (x,y)
        reverse_scroll : if True, reverses direction of mouse scroll
        """
        super().__init__()
        self.data = data
        self.title = title
        if figsize is None:
            figsize = (10, 5)
        elif reverse_scroll:
            self.reverse_scroll = -1
        else:
            self.reverse_scroll = 1
        self.blay = Layout(width='80px')
        self.done = Button(description='Done', button_style='success', layout=(self.blay))
        self.done.on_click(self.on_done)
        self.reset = Button(description='Reset', button_style='success', layout=(self.blay), tooltip='Reset to full spectrum')
        self.reset.on_click(self.on_reset)
        self.scale = widgets.FloatSlider(description='scale:', value=1.0, min=1.0, max=200, step=0.1, layout=Layout(width='80px', height=(str(2.032 * figsize[1]) + 'cm')),
          continuous_update=REACTIVE,
          orientation='vertical')
        for widg in (self.scale,):
            widg.observe(self.ob)

        plt.ioff()
        fi, ax = plt.subplots(figsize=figsize)
        self.ax = ax
        self.fig = fi
        self.xb = self.ax.get_xbound()
        self.blank = widgets.HTML('&nbsp;', layout=(self.blay))
        self.children = [VBox([self.blank, self.reset, self.scale, self.done]), self.fig.canvas]
        self.set_on_redraw()
        plt.ion()
        if show:
            display(self)
            self.data.display(figure=(self.ax), title=(self.title))

    def on_done(self, b):
        self.close()
        display(self.fig)

    def on_reset(self, b):
        self.scale.value = 1.0
        self.ax.set_xbound((self.data.axis1.itop(0), self.data.axis1.itop(self.data.size1)))

    def ob(self, event):
        """observe events and display"""
        if event['name'] == 'value':
            self.disp()

    def scale_up(self, step):
        self.scale.value *= 1.1892 ** (self.reverse_scroll * step)

    def set_on_redraw(self):

        def on_scroll(event):
            self.scale_up(event.step)

        cids = self.fig.canvas.mpl_connect'scroll_event'on_scroll

    def disp(self):
        self.xb = self.ax.get_xbound()
        self.ax.clear()
        self.data.display(scale=(self.scale.value), new_fig=False, figure=(self.ax), title=(self.title))
        self.ax.set_xbound(self.xb)


class baseline1D(Show1D):

    def __init__(self, data, figsize=None, reverse_scroll=False, show=True):
        super().__init__(data, figsize=figsize, reverse_scroll=reverse_scroll, show=False)
        self.data.real()
        ppos = self.data.axis1.itop(self.data.axis1.size / 2)
        self.select = widgets.FloatSlider(description='select:', min=0.0,
          max=(self.data.size1),
          layout=Layout(width='100%'),
          value=(0.5 * self.data.size1),
          readout=False,
          continuous_update=REACTIVE)
        self.smooth = widgets.IntSlider(description='smooth:', min=0, max=20, layout=Layout(width='70%'), tooltip='apply a local smoothing for pivot points',
          value=1,
          readout=True,
          continuous_update=REACTIVE)
        self.bsl_points = []
        for w in [self.select, self.smooth]:
            w.observe(self.ob)

        bsize = '15%'
        self.cancel = widgets.Button(description='Cancel', button_style='warning', layout=Layout(width='10%'))
        self.cancel.on_click(self.on_cancel)
        self.auto = widgets.Button(description='Auto', button_style='success', layout=Layout(width=bsize), tooltip='Automatic set of points')
        self.auto.on_click(self.on_auto)
        self.set = widgets.Button(description='Add', button_style='success', layout=Layout(width=bsize), tooltip='Add a baseline point at the selector position')
        self.set.on_click(self.on_set)
        self.unset = widgets.Button(description='Rem', button_style='warning', layout=Layout(width=bsize), tooltip='Remove the baseline point closest to the selector')
        self.unset.on_click(self.on_unset)
        self.toshow = widgets.Dropdown(options=['baseline', 'corrected', 'points'], description='Display:')
        self.toshow.observe(self.ob)
        self.Box = VBox([
         HBox([self.done, self.cancel, self.toshow,
          widgets.HTML('Choose baseline points')]),
         HBox([self.select, self.set, self.unset, self.auto, self.smooth]),
         self])

        def on_press(event):
            v = self.data.axis1.ptoi(event.xdata)
            self.select.value = abs(v)

        cids = self.fig.canvas.mpl_connect'button_press_event'on_press
        if show:
            self.show()

    def show(self):
        """create the widget and display the spectrum"""
        display(self.Box)
        self.data.display(figure=(self.ax))
        self.xb = self.ax.get_xbound()
        ppos = self.data.axis1.itop(self.select.value)
        self.ax.plot[ppos, ppos]self.ax.get_ybound()

    def close(self):
        for w in [self.select, self.auto, self.set, self.unset, self.cancel, self.toshow, self.smooth, self.Box]:
            w.close()

        super().close()

    def on_done(self, e):
        if self.bsl_points == []:
            jsalert('Please define control points before applying baseline correction')
            return
        self.close()
        print('Applied correction:\n', sorted(self.bsl_points))
        self.data.set_buffer(self.data.get_buffer() - self.correction())
        super().disp()
        display(self.fig)

    def on_auto(self, e):
        """automatically set baseline points"""
        self.bsl_points = [self.data.axis1.itop(x) for x in bcorr.autopoints(self.data)]
        self.disp()

    def on_cancel(self, e):
        self.close()
        super().disp()
        display(self.fig)

    def on_set(self, e):
        """add baseline points at selector"""
        self.bsl_points.append(self.selpos())
        self.disp()

    def on_unset(self, e):
        """remove baseline points closest from selector"""
        here = self.selpos()
        distclose = np.inf
        pclose = np.NaN
        for i, p in enumerate(self.bsl_points):
            if abs(p - here) < distclose:
                pclose = p
                distclose = abs(p - here)

        self.bsl_points.remove(pclose)
        self.disp()

    def selpos(self):
        """returns selector pos in ppm"""
        return self.data.axis1.itop(self.select.value)

    def smoothed(self):
        """returns a smoothed version of the data"""
        from scipy.signal import fftconvolve
        buf = self.data.get_buffer()
        mask = np.array([1, 1, 1, 1, 1])
        return fftconvolve(buf, mask, mode='same')

    def correction(self):
        """returns the correction to apply as a numpy array"""
        ibsl_points = self.data.axis1.ptoi(np.array(self.bsl_points)).astype(int)
        x = np.arange(self.data.size1)
        yy = self.data.get_buffer()
        if len(self.bsl_points) == 0:
            return 0.0
        if len(self.bsl_points) == 1:
            value = self.data[ibsl_points[0]] * np.ones(self.data.size1)
        else:
            if len(self.bsl_points) < 4:
                corr = bcorr._linear_interpolate(yy, ibsl_points, nsmooth=(self.smooth.value))
                value = corr(x)
            else:
                corr = bcorr._spline_interpolate(yy, ibsl_points, nsmooth=(self.smooth.value))
                value = corr(x)
        return value

    def corrected(self):
        value = self.data.copy()
        value.set_buffer(value.get_buffer() - self.correction())
        return value

    def disp(self):
        self.xb = self.ax.get_xbound()
        super().disp()
        if len(self.bsl_points) > 0:
            if self.toshow.value == 'baseline':
                (self.data.copy() - self.corrected()).display(new_fig=False, figure=(self.ax), color='r')
            else:
                if self.toshow.value == 'corrected':
                    self.ax.clear()
                    self.corrected().display(new_fig=False, figure=(self.ax), color='r', scale=(self.scale.value))
        ppos = self.selpos()
        self.ax.plot[ppos, ppos]self.ax.get_ybound()
        y = bcorr.get_ypoints((self.data.get_buffer()), (self.data.axis1.ptoi(np.array(self.bsl_points))),
          nsmooth=(self.smooth.value))
        self.ax.scatter((self.bsl_points), y, c='r', marker='o')
        self.ax.set_xbound(self.xb)


Colors = ('black', 'red', 'blue', 'green', 'orange', 'blueviolet', 'crimson', 'turquoise',
          'indigo', 'magenta', 'gold', 'pink', 'purple', 'salmon', 'darkblue', 'sienna')

class SpforSuper(object):
    __doc__ = 'a holder for SuperImpose'

    def __init__(self, i, name):
        j = i % len(Colors)
        self.name = widgets.Text(value=name, layout=Layout(width='40em'))
        self.color = widgets.Dropdown(options=Colors, value=(Colors[j]), layout=Layout(width='80px'))
        self.direct = widgets.Dropdown(options=['up', 'down', 'off'], value='off', layout=Layout(width='70px'))
        self.offset = widgets.FloatText(value=0.0, layout=Layout(width='70px'), tooltip='offset')
        self.me = HBox([widgets.HTML(value=('<b>%d</b>' % i)), self.name, self.offset, self.color, self.direct])
        self.fig = False

    def display(self, unit='ppm'):
        if self.name != 'None':
            if self.direct.value != 'off':
                scale = 1
                if self.direct.value == 'up':
                    mult = 1
                else:
                    if self.direct.value == 'down':
                        mult = -1
                    else:
                        return
                NMRData(name=(self.name.value)).set_unit(unit).mult(mult).display(new_fig=(self.fig),
                  scale=scale,
                  color=(self.color.value),
                  label=(op.basename(op.dirname(self.name.value))))


class _Show1Dplus(Show1D):

    def __init__(self, data, figsize=None, title=None, reverse_scroll=False):
        super().__init__(data, figsize=figsize, title=title, reverse_scroll=reverse_scroll)
        self.scaleint = widgets.FloatSlider(value=0.5, min=0.1, max=10, step=0.05, layout=Layout(width='20%'),
          continuous_update=REACTIVE)
        self.offset = widgets.FloatSlider(value=0.3, min=0.0, max=1.0, step=0.01, layout=Layout(width='20%'),
          continuous_update=REACTIVE)
        self.peaks = widgets.Checkbox(value=False, layout=Layout(width='15%'))
        self.integ = widgets.Checkbox(value=False, layout=Layout(width='15%'))
        for widg in (self.scaleint, self.offset, self.peaks, self.integ):
            widg.observe(self.ob)

        self.fullBox = VBox([HBox([Label('Integral scale:'), self.scaleint, Label('offset:'), self.offset]),
         HBox([Label('Show Peaks'), self.peaks, Label('integrals'), self.integ])])
        display(self.fullBox)

    def on_done(self, e):
        self.fullBox.close()
        super().close()
        self.disp(zoom=True)
        display(self.fig)

    def disp(self, zoom=False):
        """refresh display - if zoom is True, display only in xbound"""
        self.xb = self.ax.get_xbound()
        if zoom:
            zoom = self.xb
        else:
            zoom = None
        self.ax.clear()
        self.data.display(scale=(self.scale.value), new_fig=False, figure=(self.ax), title=(self.title), zoom=zoom)
        if self.integ.value:
            try:
                self.data.display_integral(label=True, integscale=(self.scaleint.value), integoff=(self.offset.value),
                  figure=(self.ax),
                  zoom=zoom)
            except:
                print('no or wrong integrals')

        if self.peaks.value:
            try:
                self.data.display_peaks(peak_label=True, figure=(self.ax), scale=(self.scale.value), zoom=zoom)
            except:
                print('no or wrong peaklist')

        self.ax.set_xbound(self.xb)


class Show1Dplus(Show1D):

    def __init__(self, data, base='/DATA', N=9, figsize=None, title=None, reverse_scroll=False):
        from spike.Interactive.ipyfilechooser import FileChooser
        super().__init__(data, figsize=figsize, title=title, reverse_scroll=reverse_scroll)
        self.scaleint = widgets.FloatSlider(value=0.5, min=0.1, max=10, step=0.05, layout=Layout(width='20%'),
          continuous_update=REACTIVE)
        self.offset = widgets.FloatSlider(value=0.3, min=0.0, max=1.0, step=0.01, layout=Layout(width='20%'),
          continuous_update=REACTIVE)
        self.peaks = widgets.Checkbox(value=False, layout=Layout(width='15%'))
        self.integ = widgets.Checkbox(value=False, layout=Layout(width='15%'))
        self.Chooser = FileChooser(base=base, filetype='*.gs1', mode='r', show=False)
        self.bsel = widgets.Button(description='Copy', layout=(self.blay), button_style='info',
          tooltip='copy selected data-set to entry below')
        self.to = widgets.IntText(value=1, min=1, max=N, layout=Layout(width='10%'))
        self.bsel.on_click(self.copy)
        self.DataList = [SpforSuper(i + 1, 'None') for i in range(N)]
        self.DataList[0].color.value = 'red'
        self.DataList[0].fig = True
        for widg in (self.scaleint, self.offset, self.peaks, self.integ):
            widg.observe(self.ob)

        self.tabs = Tab()
        self.tabs.children = [
         VBox([HBox([Label('Integral scale:'), self.scaleint, Label('offset:'), self.offset]),
          HBox([Label('Show Peaks'), self.peaks, Label('integrals'), self.integ]),
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])]),
         VBox([Label('Choose spectra to superimpose'),
          HBox([self.Chooser, self.bsel, self.to])] + [sp.me for sp in self.DataList])]
        self.tabs.set_title0'Spectrum'
        self.tabs.set_title1'Data-List'
        self.children = [
         self.tabs]

    def copy(self, event):
        if self.to.value < 1 or self.to.value > len(self.DataList):
            print('Destination is out of range !')
        else:
            self.DataList[(self.to.value - 1)].name.value = self.Chooser.selected
            self.DataList[(self.to.value - 1)].direct.value = 'up'
        self.to.value = min(self.to.value, len(self.DataList)) + 1

    def on_done(self, e):
        self.close()
        self.disp(zoom=True)
        display(self.fig)

    def disp(self, zoom=False):
        """refresh display - if zoom is True, display only in xbound"""
        self.xb = self.ax.get_xbound()
        if zoom:
            zoom = self.xb
        else:
            zoom = None
        self.ax.clear()
        self.data.display(scale=(self.scale.value), new_fig=False, figure=(self.ax), title=(self.title), zoom=zoom)
        if self.integ.value:
            try:
                self.data.display_integral(label=True, integscale=(self.scaleint.value), integoff=(self.offset.value),
                  figure=(self.ax),
                  zoom=zoom)
            except:
                print('no or wrong integrals')

        if self.peaks.value:
            try:
                self.data.display_peaks(peak_label=True, figure=(self.ax), scale=(self.scale.value), zoom=zoom)
            except:
                print('no or wrong peaklist')

        self.ax.set_xbound(self.xb)


class baseline2D_F2(baseline1D):

    def __init__(self, data, figsize=None):
        print('WARNING this tool is not functional/tested yet')
        self.data2D = data
        super().__init__((self.data2D.projF2), figsize=figsize)

    def on_done(self, e):
        super().on_done(e)
        ibsl_points = [int(self.data2D.axis2.ptoi(x)) for x in self.bsl_points]
        self.data2D.bcorr(method='spline', xpoints=ibsl_points)


class Show2D(object):
    __doc__ = '\n    A display for 2D NMR with a scale cursor\n    Show2D(spectrum) where spectrum is a NPKData object\n    - special display for DOSY.\n    '

    def __init__(self, data, title=None, figsize=None):
        self.data = data
        self.isDOSY = isinstance(data.axis1, NPKData.LaplaceAxis)
        try:
            self.proj2 = data.projF2
        except:
            self.proj2 = data.proj(axis=2).real()

        try:
            self.proj1 = data.projF1
        except:
            self.proj1 = data.proj(axis=1).real()

        self.title = title
        self.scale = widgets.FloatLogSlider(description='scale:', value=1.0, min=(-1), max=3, base=10, step=0.01, layout=Layout(width='80%'),
          continuous_update=HEAVY)
        self.posview = widgets.Checkbox(value=True, description='Positive', tooltip='Display Positive levels')
        self.negview = widgets.Checkbox(value=False, description='Negative', tooltip='Display Negative levels')
        self.cursors = widgets.Checkbox(value=False, description='Cursors', tooltip='show cursors (cpu intensive !)')
        for w in (self.scale, self.posview, self.negview, self.cursors):
            w.observe(self.ob)

        grid = {'height_ratios':[
          1, 4], 
         'hspace':0,  'wspace':0}
        if self.isDOSY:
            fsize = (10, 5)
            grid['width_ratios'] = [7, 1]
        else:
            fsize = (8, 8)
            grid['width_ratios'] = [4, 1]
        self.fig = plt.figure(figsize=fsize, constrained_layout=False)
        spec2 = (gridspec.GridSpec)(ncols=2, nrows=2, figure=self.fig, **grid)
        axarr = np.empty((2, 2), dtype=object)
        axarr[(0, 0)] = self.fig.add_subplot(spec2[(0, 0)])
        axarr[(1, 0)] = self.fig.add_subplot((spec2[(1, 0)]), sharex=(axarr[(0, 0)]))
        axarr[(1, 1)] = self.fig.add_subplot((spec2[(1, 1)]), sharey=(axarr[(1, 0)]))
        self.top_ax = axarr[(0, 0)]
        self.spec_ax = axarr[(1, 0)]
        self.side_ax = axarr[(1, 1)]
        self.multitop = None
        self.multiside = None
        self.Box = HBox([self.scale, self.posview, self.negview, self.cursors])
        display(self.Box)
        self.disp(new=True)

    def on_done(self, b):
        self.scale.close()

    def ob(self, event):
        """observe events and display"""
        if event['name'] != 'value':
            return
        self.disp()

    def disp(self, new=False):
        if new:
            self.proj2.display(figure=(self.top_ax), title=(self.title))
            xb = self.top_ax.get_xbound()
            dataxis = self.proj1.axis1.itoc(self.proj1.axis1.points_axis())
            self.side_ax.plotself.proj1.get_buffer()dataxis
            yb = self.side_ax.get_ybound()
        else:
            yb = self.side_ax.get_ybound()
            xb = self.top_ax.get_xbound()
            self.spec_ax.clear()
        if self.cursors.value:
            self.multitop = MultiCursor((self.fig.canvas), (self.spec_ax, self.top_ax), color='r', lw=1, horizOn=False, vertOn=True)
            self.multiside = MultiCursor((self.fig.canvas), (self.spec_ax, self.side_ax), color='r', lw=1, horizOn=True, vertOn=False)
        else:
            self.multitop = None
            self.multiside = None
        if self.posview.value:
            self.data.display(scale=(self.scale.value), new_fig=False, figure=(self.spec_ax))
        if self.negview.value:
            self.data.display(scale=(-self.scale.value), new_fig=False, figure=(self.spec_ax),
              mpldic={'cmap': 'Wistia'})
        self.spec_ax.set_xbound(xb)
        self.spec_ax.set_ybound(yb)


class Phaser1D(Show1D):
    __doc__ = '\n    An interactive phaser in 1D NMR\n\n        Phaser1D(spectrum)\n\n    requires %matplotlib widget\n\n    '

    def __init__(self, data, figsize=None, title=None, reverse_scroll=False, show=True):
        data.check1D()
        if data.itype == 0:
            jsalert('Data is Real - Please redo Fourier Transform')
            return
        super().__init__(data, figsize=figsize, title=title, reverse_scroll=reverse_scroll, show=False)
        self.p0 = widgets.FloatSlider(description='P0:', min=(-180), max=180, step=0.1, layout=Layout(width='100%'),
          continuous_update=REACTIVE)
        self.p1 = widgets.FloatSlider(description='P1:', min=(-360), max=360, step=1.0, layout=Layout(width='100%'),
          continuous_update=REACTIVE)
        self.pivot = widgets.FloatSlider(description='pivot:', min=0.0,
          max=(self.data.size1),
          step=1,
          layout=Layout(width='80%'),
          value=(0.5 * self.data.size1),
          readout=False,
          continuous_update=REACTIVE)
        self.cancel = widgets.Button(description='Cancel', button_style='warning')
        self.cancel.on_click(self.on_cancel)
        self.done.close()
        self.apply = widgets.Button(description='Done', button_style='success')
        self.apply.on_click(self.on_Apply)
        self.children = [
         VBox([
          HBox([self.apply, self.cancel, self.pivot, widgets.HTML('<i>set by clicking on spectrum</i>')]),
          self.p0,
          self.p1,
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])])]
        for w in [self.p0, self.p1, self.scale]:
            w.observe(self.ob)

        self.pivot.observe(self.on_movepivot)

        def on_press(event):
            self.pivot.value = self.data.axis1.ptoi(event.xdata)

        cids = self.fig.canvas.mpl_connect'button_press_event'on_press
        self.lp0, self.lp1 = self.ppivot()
        if show:
            self.show()

    def show(self):
        self.data.display(figure=(self.ax))
        self.xb = self.ax.get_xbound()
        ppos = self.data.axis1.itop(self.pivot.value)
        self.ax.plot[ppos, ppos]self.ax.get_ybound()
        display(self)

    def on_cancel(self, b):
        self.close()
        print('no applied phase')

    def on_Apply(self, b):
        self.close()
        lp0, lp1 = self.ppivot()
        self.data.phaselp0lp1
        self.disp()
        self.on_done(b)
        print('Applied: phase(%.1f,  %.1f)' % (lp0, lp1))

    def ppivot(self):
        """converts from pivot values to centered ones"""
        pp = 1.0 - self.pivot.value / self.data.size1
        return (self.p0.value + (pp - 0.5) * self.p1.value, self.p1.value)

    def ctopivot(self, p0, p1):
        """convert from centered to pivot values"""
        pp = 1.0 - self.pivot.value / self.data.size1
        return (p0 - (pp - 0.5) * p1, p1)

    def on_movepivot(self, event):
        if event['name'] == 'value':
            self.p0.value, self.p1.value = self.ctopivotself.lp0self.lp1
            self.phase()

    def ob(self, event):
        """observe changes and start phasing"""
        if event['name'] == 'value':
            self.phase()

    def phase(self):
        """apply phase and display"""
        self.xb = self.ax.get_xbound()
        self.ax.clear()
        self.lp0, self.lp1 = self.ppivot()
        self.data.copy().phaseself.lp0self.lp1.display(scale=(self.scale.value), new_fig=False, figure=(self.ax))
        ppos = self.data.axis1.itop(self.pivot.value)
        self.ax.plot[ppos, ppos]self.ax.get_ybound()
        self.ax.set_xbound(self.xb)


class Phaser2D(object):
    __doc__ = '\n    An interactive phaser in 2D NMR\n\n        Phaser2D(spec)\n\n    best when in %matplotlib inline\n\n    '

    def __init__(self, data):
        print('WARNING this tool is not functional/tested yet')
        self.data = data
        self.scale = widgets.FloatLogSlider(description='scale:', value=1.0, min=(-1), max=2, base=10, step=0.01, layout=Layout(width='80%'),
          continuous_update=HEAVY)
        self.F1p0 = widgets.FloatSlider(min=(-180), max=180, step=0.1, description='F1 p0', continuous_update=HEAVY)
        self.F1p1 = widgets.FloatSlider(min=(-250), max=250, step=1.0, description='F1 p1', continuous_update=HEAVY)
        self.F2p0 = widgets.FloatSlider(min=(-180), max=180, step=0.1, description='F2 p0', continuous_update=HEAVY)
        self.F2p1 = widgets.FloatSlider(min=(-250), max=250, step=1.0, description='F2 p1', continuous_update=HEAVY)
        for w in [self.F1p0, self.F1p1, self.F2p0, self.F2p1, self.scale]:
            w.observe(self.ob)

        self.button = widgets.Button(description='Apply correction', button_style='success')
        self.button.on_click(self.on_Apply)
        self.cancel = widgets.Button(description='Cancel', button_style='warning')
        self.cancel.on_click(self.on_cancel)
        display(VBox([self.scale,
         HBox([VBox([self.F1p0, self.F1p1], layout=Layout(width='40%')), VBox([self.F2p0, self.F2p1], layout=Layout(width='40%'))], layout=Layout(width='80%'))],
          layout=Layout(width='100%')))
        display(HBox([self.button, self.cancel]))
        fi, ax = plt.subplots()
        self.ax = ax
        self.display()

    def ob(self, event):
        """observe changes and start phasing"""
        if event['name'] == 'value':
            self.phase()

    def close(self):
        for w in [self.F1p0, self.F1p1, self.F2p0, self.F2p1, self.scale, self.button, self.cancel]:
            w.close()

    def on_cancel(self, b):
        print('No action')
        self.ax.clear()
        self.data.display(figure=(self.ax), scale=(self.scale.value))
        self.ax.set_xlim(xmin=(self.data.axis2.itop(0)), xmax=(self.data.axis2.itop(self.data.size2)))
        self.ax.set_ylim(ymin=(self.data.axis1.itop(0)), ymax=(self.data.axis1.itop(self.data.size1)))
        self.close()

    def on_Apply(self, b):
        print("Applied: phase(%.1f,%.1f,axis='F1').phase(%.1f,%.1f,axis='F')" % (self.F1p0.value, self.F1p1.value, self.F2p0.value, self.F2p1.value))
        self.data.phase((self.F2p0.value), (self.F2p1.value), axis='F2').phase((self.F1p0.value), (self.F1p1.value), axis='F1')
        self.data.display(figure=(self.ax), scale=(self.scale.value))
        self.ax.set_xlim(xmin=(self.data.axis2.itop(0)), xmax=(self.data.axis2.itop(self.data.size2)))
        self.ax.set_ylim(ymin=(self.data.axis1.itop(0)), ymax=(self.data.axis1.itop(self.data.size1)))
        self.close()

    def display(self, todisplay=None):
        """display either the current data or the one provided - red and blue"""
        self.ax.clear()
        if not todisplay:
            todisplay = self.data
        todisplay.display(scale=(self.scale.value), new_fig=False, figure=(self.ax), color='blue')
        todisplay.display(scale=(-self.scale.value), new_fig=False, figure=(self.ax), color='red')
        self.ax.set_xlim(xmin=(self.data.axis2.itop(0)), xmax=(self.data.axis2.itop(self.data.size2)))
        self.ax.set_ylim(ymin=(self.data.axis1.itop(0)), ymax=(self.data.axis1.itop(self.data.size1)))

    def phase(self):
        """compute phase and display"""
        dp = self.data.copy().phase((self.F2p0.value), (self.F2p1.value), axis='F2').phase((self.F1p0.value), (self.F1p1.value), axis='F1')
        self.display(dp)


class AvProc1D:
    __doc__ = 'Detailed 1D NMR Processing'

    def __init__(self, filename=''):
        print('WARNING this tool is not functional/tested yet')
        self.wfile = widgets.Text(description='File to process', layout=Layout(width='80%'), value=filename)
        self.wapod = widgets.Dropdown(options=[
         'None', 'apod_sin (sine bell)', 'apod_em (Exponential)', 'apod_gm (Gaussian)', 'gaussenh (Gaussian Enhacement)', 'kaiser'],
          value='apod_sin (sine bell)',
          description='Apodisation')
        self.wpapod_Hz = widgets.FloatText(value=1.0,
          min=0,
          max=30,
          description='Width in Hz',
          layout=Layout(width='15%'),
          disabled=True)
        self.wpapod_enh = widgets.FloatText(value=2.0,
          min=0.0,
          max=5.0,
          description='strength',
          layout=Layout(width='15%'),
          step=1,
          disabled=True)
        self.wpapod_sin = widgets.FloatText(value=0.0,
          min=0,
          max=0.5,
          description='bell shape',
          layout=Layout(width='15%'),
          step=0.01,
          tooltip='value is the maximum of the bell, 0 is pure cosine, 0.5 is pure sine',
          disabled=False)
        self.wzf = widgets.Dropdown(options=[
         0, 1, 2, 4, 8],
          value=1,
          description='Zero-Filling')
        self.wphase0 = widgets.FloatText(value=0,
          description='Phase : P0',
          layout=Layout(width='20%'),
          disabled=True)
        self.wphase1 = widgets.FloatText(value=0,
          description='P1',
          layout=Layout(width='20%'),
          disabled=True)
        self.wapmin = widgets.Checkbox(value=True,
          description='AutoPhasing',
          tooltip='Perform AutoPhasing')
        self.wapmin.observe(self.apmin_select)
        self.wbcorr = widgets.Checkbox(value=False,
          description='Baseline Correction',
          tooltip='Perform AutoPhasing')
        self.wapod.observe(self.apod_select)
        self.bapod = widgets.Button(description='Show effect on FID')
        self.bapod.on_click(self.show_apod)
        self.bdoit = widgets.Button(description='Process')
        self.bdoit.on_click(self.process)
        self.show()
        fi, ax = plt.subplots()
        self.ax = ax
        if os.path.exists(filename):
            self.load()
            self.display()

    def apod_select(self, e):
        test = self.wapod.value.split()[0]
        self.wpapod_sin.disabled = True
        self.wpapod_Hz.disabled = True
        self.wpapod_enh.disabled = True
        if test == 'apod_sin':
            self.wpapod_sin.disabled = False
        if test in ('apod_em', 'apod_gm', 'gaussenh'):
            self.wpapod_Hz.disabled = False
        if test == 'gaussenh':
            self.wpapod_enh.disabled = False

    def apmin_select(self, e):
        for w in (self.wphase0, self.wphase1):
            w.disabled = self.wapmin.value

    def load(self):
        self.data = Import_1D(self.wfile.value)

    def apod(self):
        func = self.wapod.value.split()[0]
        todo = None
        if func == 'apod_sin':
            todo = 'self.data.apod_sin(%f)' % (self.wpapod_sin.value,)
        else:
            if func in ('apod_em', 'apod_gm'):
                todo = 'self.data.%s(%f)' % (func, self.wpapod_Hz.value)
            else:
                if func == 'gaussenh':
                    todo = 'self.data.gaussenh(%f,enhancement=%f)' % (self.wpapod_Hz.value, self.wpapod_enh.value)
        if todo is not None:
            eval(todo)
        return self.data

    def show_apod(self, e):
        self.load()
        self.apod()
        self.display()

    def process(self, e):
        self.load()
        self.apod().zf(self.wzf.value).ft_sim().bk_corr().set_unit('ppm')
        if self.wapmin.value:
            self.data.apmin()
            self.wphase0.value = round(self.data.axis1.P0, 1)
            self.wphase1.value = self.data.axis1.P1
        else:
            self.data.phaseself.wphase0.valueself.wphase1.value
        self.display()

    def display(self):
        self.ax.clear()
        self.data.display(figure=(self.ax))

    def show(self):
        display(VBox([self.wfile,
         HBox([self.wapod, self.wpapod_sin, self.wpapod_Hz, self.wpapod_enh, self.bapod]),
         self.wzf,
         HBox([self.wapmin, self.wphase0, self.wphase1]),
         self.bdoit]))


from spike.plugins import Peaks

class NMRPeaker1D(Show1D):
    __doc__ = '\n    a peak-picker for NMR experiments\n    '

    def __init__(self, data, figsize=None, reverse_scroll=False, show=True):
        super().__init__(data, figsize=figsize, reverse_scroll=reverse_scroll, show=False)
        self.data = data.real()
        try:
            self.peaks = self.data.peaks
        except AttributeError:
            self.peaks = Peaks.Peak1DList()

        self.temppk = Peaks.Peak1DList()
        self.thresh = widgets.FloatLogSlider(value=20.0, min=(-1),
          max=2.0,
          base=10,
          step=0.01,
          layout=Layout(width='30%'),
          continuous_update=False,
          readout=True,
          readout_format='.2f')
        try:
            self.thresh.value = 100 * self.data.peaks.threshold / self.data.absmax
        except:
            self.thresh.value = 20.0

        self.thresh.observe(self.pickpeak)
        self.peak_mode = widgets.Dropdown(options=['marker', 'bar'], value='marker', description='show as')
        self.peak_mode.observe(self.ob)
        self.out = Output(layout={'border': '1px solid red'})
        self.badd = widgets.Button(description='Add', button_style='success', layout=(self.blay))
        self.badd.on_click(self.on_add)
        self.brem = widgets.Button(description='Rem', button_style='warning', layout=(self.blay))
        self.brem.on_click(self.on_rem)
        self.cancel = widgets.Button(description='Cancel', button_style='warning', layout=(self.blay))
        self.cancel.on_click(self.on_cancel)
        self.selval = widgets.FloatText(value=0.0,
          description='selection',
          layout=Layout(width='20%'),
          step=0.001,
          disabled=True)
        self.newval = widgets.FloatText(value=0.0,
          description='calibration',
          layout=Layout(width='20%'),
          step=0.001,
          disabled=True)
        self.setcalib = widgets.Button(description='Set', layout=Layout(width='10%'), button_style='success',
          tooltip='Set spectrum calibration')
        self.setcalib.on_click(self.on_setcalib)

        def on_press(event):
            v = event.xdata
            iv = self.data.axis1.ptoi(v)
            distclose = np.inf
            pclose = 0.0
            for p in self.data.peaks:
                if abs(p.pos - iv) < distclose:
                    pclose = p.pos
                    distclose = abs(p.pos - iv)

            self.selval.value = self.data.axis1.itop(pclose)
            for w in (self.selval, self.newval):
                w.disabled = False

        cids = self.fig.canvas.mpl_connect'button_press_event'on_press
        self.tabs = Tab()
        self.tabs.children = [
         VBox([
          HBox([self.badd, self.brem, Label('threshold - % largest signal'), self.thresh, self.peak_mode]),
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])]),
         VBox([
          HBox([Label('Select a peak with mouse and set calibrated values'), self.selval, self.newval, self.setcalib]),
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])]),
         self.out]
        self.tabs.set_title0'Peak Picker'
        self.tabs.set_title1'calibration'
        self.tabs.set_title2'Peak Table'
        self.children = [
         VBox([HBox([self.done, self.cancel]), self.tabs])]
        if show:
            self.show()

    def show(self):
        self.data.display(figure=(self.ax))
        self.xb = self.ax.get_xbound()
        self.pp()
        self.data.display(figure=(self.ax))
        self.ax.set_xbound((self.data.axis1.itop(0), self.data.axis1.itop(self.data.size1)))
        self.disp()
        display(self)

    def on_add(self, b):
        self.peaks = Peaks.peak_aggreg((self.peaks + self.temppk), distance=1.0)
        self.temppk = Peaks.Peak1DList()
        self.disp()

    def on_rem(self, b):
        up, down = self.ax.get_xbound()
        iup = self.data.axis1.ptoi(up)
        idown = self.data.axis1.ptoi(down)
        iup, idown = max(iup, idown), min(iup, idown)
        to_rem = []
        for pk in self.peaks:
            if pk.pos < iup and pk.pos > idown:
                to_rem.append(pk)

        for pk in to_rem:
            self.peaks.remove(pk)

        self.disp()

    def on_cancel(self, b):
        self.close()
        del self.data.peaks
        print('no Peak-Picking done')

    def on_done(self, b):
        self.temppk = Peaks.Peak1DList()
        self.close()
        self.disp()
        tabs = Tab()
        tabs.children = [self.fig.canvas, self.out]
        tabs.set_title0'1D Display'
        tabs.set_title1'Peak Table'
        display(tabs)
        self.data.peaks = self.peaks

    def on_setcalib(self, e):
        off = self.selval.value - self.newval.value
        self.data.axis1.offset -= off * self.data.axis1.frequency
        self.selval.value = self.newval.value
        self.pp()

    def pkprint(self, event):
        self.out.clear_output(wait=True)
        with self.out:
            if len(self.temppk) > 0:
                self.data.peaks = self.temppk
                display(HTML('<p style=color:red> Transient peak list </p>'))
                display(HTML(self.data.pk2pandas().to_html()))
                display(HTML('<p style=color:blue> Defined peak list </p>'))
            self.data.peaks = self.peaks
            display(HTML(self.data.pk2pandas().to_html()))

    def _pkprint(self, event):
        self.out.clear_output(wait=True)
        with self.out:
            print(self.pklist())

    def pklist(self):
        """creates peaklist for printing or exporting"""
        text = ['ppm\tInt.(%)\twidth (Hz)']
        data = self.data
        intmax = max(data.peaks.intens) / 100
        for pk in data.peaks:
            ppm = data.axis1.itop(pk.pos)
            width = 2 * pk.width * data.axis1.specwidth / data.size1
            l = '%.3f\t%.1f\t%.2f' % (ppm, pk.intens / intmax, width)
            text.append(l)

        return '\n'.join(text)

    def ob(self, event):
        if event['name'] == 'value':
            self.disp()

    def disp(self):
        """interactive wrapper to peakpick"""
        self.xb = self.ax.get_xbound()
        self.ax.clear()
        self.data.display(scale=(self.scale.value), new_fig=False, figure=(self.ax), title=(self.title))
        x = [self.data.axis1.itoc(z) for z in (0, self.data.size1)]
        y = [self.data.absmax * self.thresh.value / 100] * 2
        self.ax.plot(x, y, ':r')
        try:
            self.temppk.display(peak_label=False, peak_mode=(self.peak_mode.value), f=(self.data.axis1.itoc), figure=(self.ax), color='red')
            self.peaks.display(peak_label=False, peak_mode=(self.peak_mode.value), f=(self.data.axis1.itoc), color='blue', figure=(self.ax))
        except:
            rrr('problem')

        self.temppk.display(peak_label=True, peak_mode=(self.peak_mode.value), color='red', figure=(self.ax))
        self.ax.set_xbound(self.xb)
        self.ax.set_ylim(ymax=(self.data.absmax / self.scale.value))
        self.pkprint({'name': 'value'})

    def pickpeak(self, event):
        """interactive wrapper to peakpick"""
        if event['name'] == 'value':
            self.pp()

    def pp(self):
        """do the peak-picking calling pp().centroid()"""
        th = self.data.absmax * self.thresh.value / 100
        zm = self.ax.get_xbound()
        self.data.set_unit('ppm').peakpick(threshold=th, verbose=False, zoom=zm).centroid()
        self.temppk = self.data.peaks
        self.disp()
        self.ax.annotate(('%d peaks detected' % len(self.data.peaks)), (0.05, 0.95), xycoords='figure fraction')


from spike.plugins.Integrate import Integrals, Integralitem

class NMRIntegrate(Show1D):
    __doc__ = 'an integrator for NMR experiments'

    def __init__(self, data, figsize=None, reverse_scroll=False, show=True):
        super().__init__(data, figsize=figsize, reverse_scroll=reverse_scroll, show=False)
        try:
            self.Integ = data.integrals
        except:
            self.Integ = Integrals(data, compute=False)

        self.thresh = widgets.FloatLogSlider(description='sensitivity', value=10.0, min=(-1),
          max=2.0,
          base=10,
          step=0.01,
          layout=Layout(width='30%'),
          continuous_update=HEAVY,
          readout=False,
          readout_format='.2f')
        self.bias = widgets.FloatSlider(description='bias',
          layout=Layout(width='20%'),
          value=0.0,
          min=(-10.0),
          max=10.0,
          step=0.1,
          continuous_update=HEAVY,
          readout=False,
          readout_format='.1f')
        self.sep = widgets.FloatSlider(description='separation',
          layout=Layout(width='30%'),
          value=3.0,
          min=0.0,
          max=20.0,
          step=0.1,
          continuous_update=HEAVY,
          readout=False,
          readout_format='.1f')
        self.wings = widgets.FloatSlider(description='extension',
          layout=Layout(width='30%'),
          value=5.0,
          min=0.5,
          max=20.0,
          step=0.1,
          continuous_update=HEAVY,
          readout=False,
          readout_format='.1f')
        for w in (self.bias, self.sep, self.wings):
            w.observe(self.integrate)

        self.thresh.observe(self.peak_and_integrate)
        self.cancel = widgets.Button(description='Cancel', button_style='warning', layout=(self.blay))
        self.cancel.on_click(self.on_cancel)
        self.bprint = widgets.Button(description='Print', layout=(self.blay), button_style='success',
          tooltip='Print to screen')
        self.bprint.on_click(self.print)
        self.badd = widgets.Button(description='Add', layout=(self.blay), button_style='success',
          tooltip='Add an entry from current zoom')
        self.badd.on_click(self.on_add)
        self.brem = widgets.Button(description='Rem', layout=(self.blay), button_style='warning',
          tooltip='Remove all entries in current zoom')
        self.brem.on_click(self.on_rem)
        self.bauto = widgets.Button(description='Compute', layout=(self.blay), button_style='success',
          tooltip='Automatic definition of integrals')
        self.bauto.on_click(self.peak_and_integrate)
        self.entry = widgets.IntText(value=0, description='Entry', min=0, layout=Layout(width='15%'))
        self.value = widgets.FloatText(value=100, description='Value', layout=Layout(width='15%'))
        self.set = widgets.Button(description='Set', button_style='success', layout=Layout(width='10%'))
        self.set.on_click(self.set_value)
        self.out = Output(layout={'border': '1px solid red'})
        self.tabs = Tab()
        self.tabs.children = [
         VBox([
          HBox([self.badd, self.brem,
           Label('Use buttons to add and remove integrals in the current zoom window')]),
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])]),
         VBox([HBox([self.bauto, Label('Define integral shapes using the sliders below')]),
          HBox([self.thresh, self.sep, self.wings]),
          HBox([VBox([self.blank, self.reset, self.scale]), self.fig.canvas])]),
         VBox([
          HBox([Label('Choose an integral for calibration'),
           self.entry, self.value, self.set, self.blank, self.bprint]),
          self.out])]
        self.tabs.set_title0'Manual integration'
        self.tabs.set_title1'Automatic'
        self.tabs.set_title2'Integral Table & Calibration'
        self.children = [VBox([HBox([self.done, self.cancel]), self.tabs])]
        if show:
            self.show()

    def show(self):
        self.data.display(figure=(self.ax))
        self.xb = self.ax.get_xbound()
        self.data.display(figure=(self.ax))
        self.ax.set_xbound((self.data.axis1.itop(0), self.data.axis1.itop(self.data.size1)))
        self.disp()
        display(self)

    def on_cancel(self, b):
        self.close()
        print('No integration')

    def on_done(self, b):
        self.close()
        self.disp(zoom=True)
        display(self.fig)
        display(self.out)
        self.data.integrals = self.Integ

    def on_add(self, b):
        start, end = self.ax.get_xbound()
        self.Integ.append(Integralitem(self.data.axis1.ptoi(start), self.data.axis1.ptoi(end), [], 0.0))
        self.Integ.zonestocurves()
        self.disp()
        self.print(None)

    def on_rem(self, b):
        start, end = self.ax.get_xbound()
        start, end = self.data.axis1.ptoi(start), self.data.axis1.ptoi(end)
        start, end = min(start, end), max(start, end)
        to_rem = []
        for ii in self.Integ:
            if ii.start > start and ii.end < end:
                to_rem.append(ii)

        for ii in to_rem:
            self.Integ.remove(ii)

        self.disp()
        self.print(None)

    def set_value(self, b):
        self.Integ.recalibrateself.entry.valueself.value.value
        self.disp()
        self.print(None)

    def print(self, event):
        self.out.clear_output()
        self.Integ.sort(key=(lambda x: x.start))
        with self.out:
            display(HTML(self.Integ.to_pandas().to_html()))

    def peak_and_integrate(self, event):
        self.data.pp(threshold=(self.data.absmax * self.thresh.value / 100), verbose=False,
          zoom=(self.ax.get_xbound())).centroid()
        if len(self.data.peaks) > 0:
            self.int()

    def integrate(self, event):
        self.int()

    def int(self):
        """do the automatic integration from peaks and parameters"""
        self.on_rem(None)
        try:
            calib = self.Integ.calibration
        except:
            calib = None

        self.data.set_unit('ppm')
        try:
            self.data.peaks
        except:
            self.data.pp(threshold=(self.data.absmax * self.thresh.value / 100), verbose=False,
              zoom=(self.ax.get_xbound())).centroid()

        self.Integ += Integrals((self.data), separation=(self.sep.value), wings=(self.wings.value), bias=(self.data.absmax * self.bias.value / 100))
        self.Integ.calibrate(calibration=calib)
        self.print(None)
        self.disp()

    def ob(self, event):
        if event['name'] == 'value':
            self.disp()

    def disp(self, zoom=False):
        """refresh display from event - if zoom is True, display only in xbound"""
        self.xb = self.ax.get_xbound()
        self.ax.clear()
        if zoom:
            zoom = self.xb
        else:
            zoom = None
        self.data.display(new_fig=False, figure=(self.ax), scale=(self.scale.value), zoom=zoom)
        try:
            self.Integ.display(label=True, figure=(self.ax), labelyposition=0.01, regions=False, zoom=zoom)
        except:
            pass

        self.ax.set_xbound(self.xb)