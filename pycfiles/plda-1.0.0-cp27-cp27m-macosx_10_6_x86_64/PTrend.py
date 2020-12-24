# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\PTrend.py
# Compiled at: 2019-03-05 01:36:24
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt, random

class PAxes:

    def __init__(self):
        self.axes = []

    def __del__(self):
        self.axes = []

    def add(self, name, label, vmin, vmax, loc):
        dc = {}
        dc['name'] = name
        dc['label'] = label
        dc['min'] = min(vmin, vmax)
        dc['max'] = max(vmin, vmax)
        dc['loc'] = loc
        dc['idx'] = len(self.axes)
        self.axes.append(dc)

    def get_axes_range(self, name):
        for a in self.axes:
            if a['name'] == name:
                return (a['min'], a['max'])

        return (0, 100)

    def get_axes_id(self, name):
        for i in range(len(self.axes)):
            if self.axes[i]['name'] == name:
                return i

        return

    def get_axes_name(self, idx):
        if idx >= 0 and idx < len(self.axes):
            return self.axes[idx]['name']
        else:
            return
            return

    def build_axes(self, fig, xlabel):
        _left = 0.3
        _right = 0.1
        _width = 0.2
        _height = 0.8
        par = []
        for i in range(len(self.axes)):
            if i == 0:
                host = HostAxes(fig, [_left, _right, _width, _height])
            else:
                _p = ParasiteAxes(host, sharex=host)
                par.append(_p)

        for _p in par:
            host.parasites.append(_p)

        host.axis['right'].set_visible(False)
        host.axis['top'].set_visible(False)
        host.set_xlabel(xlabel)
        host.set_ylabel(self.axes[0]['label'])
        _leftoffset = 0
        _rightoffset = 0
        for i in range(len(par)):
            _p = par[i]
            if i == 0:
                _p.axis['right'].set_visible(True)
                _p.axis['right'].major_ticklabels.set_visible(True)
                _p.axis['right'].label.set_visible(True)
            else:
                _axisline = _p.get_grid_helper().new_fixed_axis
                _loc = self.axes[(i + 1)]['loc']
                if _loc == 'left':
                    _leftoffset -= 60
                    _offset = _leftoffset
                else:
                    _rightoffset += 60
                    _offset = _rightoffset
                _p.axis['right%d' % (i + 1)] = _axisline(loc=_loc, axes=_p, offset=(_offset, 0))
            _p.set_ylabel(self.axes[(i + 1)]['label'])

        fig.add_axes(host)
        axes = [
         host]
        axes.extend(par)
        return axes

    def get_axes_num(self):
        return len(self.axes)


class PLine:

    def __init__(self):
        self.lines = []

    def __del__(self):
        self.lines = []

    def add(self, name, axes, color):

        def tcolor(c):
            c = c.replace('(', '')
            c = c.replace(')', '')
            _rgba = c.split(',')
            _r = int(_rgba[0])
            _g = int(_rgba[1])
            _b = int(_rgba[2])
            if _r < 0:
                _r = 0
            if _g < 0:
                _g = 0
            if _b < 0:
                _b = 0
            if _r + _g + _b == 0:
                _r = random.randint(1, 255)
                _g = random.randint(1, 255)
                _b = random.randint(1, 255)
            val = _r * 65536 + _g * 256 + _b
            t = hex(val)
            t = t.replace('0x', '')
            t = t.zfill(6)
            return '#' + t

        dc = {}
        dc['name'] = name
        dc['axes'] = axes
        dc['color'] = tcolor(color)
        self.lines.append(dc)

    def get_curve_byidx(self, idx):
        idx = int(idx)
        if idx < 0 or idx >= len(self.lines):
            return
        return self.lines[idx]
        return

    def get_num(self):
        return len(self.lines)


class PTrend:

    def __init__(self, title, xlabel):
        self.title = title
        self.xlabel = xlabel
        self.objAxes = PAxes()
        self.objLine = PLine()

    def render_random(self, filename=''):
        if self.objLine.get_num() == 0 or self.objAxes.get_axes_num() == 0:
            return -1
        fig = plt.figure(1)
        ltaxes = self.objAxes.build_axes(fig, self.xlabel)
        xval = []
        for i in range(10):
            xval.append(i)

        for i in range(self.objLine.get_num()):
            _curve = self.objLine.get_curve_byidx(i)
            if _curve == None:
                return
            ax_id = self.objAxes.get_axes_id(_curve['axes'])
            ax_cp = ltaxes[ax_id]
            if ax_id == None:
                return
            _range = self.objAxes.get_axes_range(_curve['axes'])
            yval = []
            for i in range(10):
                yval.append(random.random() * (_range[1] - _range[0]) + _range[0])

            curve_cp, = ax_cp.plot(xval, yval, label=_curve['name'], color=_curve['color'])

        for i in range(len(ltaxes)):
            _aname = self.objAxes.get_axes_name(i)
            _range = self.objAxes.get_axes_range(_aname)
            ltaxes[i].set_ylim(_range[0], _range[1])

        ltaxes[0].legend()
        if filename == '':
            fig.show()
        else:
            fig.savefig(filename)
        fig.clear()
        del fig
        return

    def append_axes(self, name, label, vmin, vmax, loc):
        self.objAxes.add(name, label, vmin, vmax, loc)

    def append_curve(self, name, axes, color):
        self.objLine.add(name, axes, color)

    def __del__(self):
        del self.objAxes
        del self.objLine