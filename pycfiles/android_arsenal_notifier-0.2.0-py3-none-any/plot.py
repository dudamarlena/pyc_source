# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/com/dtmilano/android/plot.py
# Compiled at: 2019-10-11 02:14:01
__doc__ = '\nCopyright (C) 2012-2018  Diego Torres Milano\nCreated on mar 11, 2017\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\n@author: Diego Torres Milano\n\n'
from __future__ import print_function
import sys, types
from math import ceil
import matplotlib.pyplot as plt, mpl_toolkits.axisartist as AA, numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
from com.dtmilano.android.adb.dumpsys import Dumpsys
__version__ = '15.8.1'
DEBUG = True
NumberTypes = (
 types.IntType, types.LongType, types.FloatType)

class Plot:

    def __init__(self):
        self.n = 0
        self.na = []
        self.va = []
        self.ava = {}
        self.aava = {}

    def append(self, value):
        if DEBUG:
            print(('append({})').format(value), file=sys.stderr)
        self.n += 1
        self.na.append(self.n)
        if isinstance(value, NumberTypes):
            self.va.append(value)
        elif isinstance(value, Dumpsys):
            if not self.ava:
                self.__initAva()
            if not self.aava:
                self.__initAava()
            dumpsys = value
            self.ava[Dumpsys.TOTAL].append(dumpsys.get(Dumpsys.TOTAL))
            self.ava[Dumpsys.ACTIVITIES].append(dumpsys.get(Dumpsys.ACTIVITIES))
            self.ava[Dumpsys.VIEWS].append(dumpsys.get(Dumpsys.VIEWS))
            self.aava[Dumpsys.FRAMESTATS].append(dumpsys.get(Dumpsys.FRAMESTATS))
        return self

    def __initAva(self):
        self.ava[Dumpsys.TOTAL] = []
        self.ava[Dumpsys.ACTIVITIES] = []
        self.ava[Dumpsys.VIEWS] = []

    def __initAava(self):
        self.aava[Dumpsys.FRAMESTATS] = []

    def plot(self, _type=Dumpsys.MEMINFO, filename=None):
        title = 'Dumpsys'
        if _type == Dumpsys.FRAMESTATS:
            subtitle = 'gfxinfo ' + Dumpsys.FRAMESTATS
        else:
            subtitle = _type
        if _type == Dumpsys.MEMINFO:
            if self.ava:
                if DEBUG:
                    print('plot:', file=sys.stderr)
                    for k in self.ava.keys():
                        print(('   {}: {}').format(k, self.ava[k]), file=sys.stderr)

                host = host_subplot(111, axes_class=AA.Axes)
                plt.subplots_adjust(right=0.75)
                par = {}
                for k in self.ava.keys():
                    if k != Dumpsys.TOTAL:
                        par[k] = host.twinx()

                axis = 1
                for k in self.ava.keys():
                    if k != Dumpsys.TOTAL and k != Dumpsys.ACTIVITIES:
                        offset = axis * 60
                        axis += 1
                        new_fixed_axis = par[k].get_grid_helper().new_fixed_axis
                        par[k].axis['right'] = new_fixed_axis(loc='right', axes=par[k], offset=(
                         offset, 0))
                        par[k].axis['right'].toggle(all=True)

                if DEBUG:
                    print(('setting host x lim {} {}').format(np.amin(self.na), np.amax(self.na)), file=sys.stderr)
                minx = np.amin(self.na)
                maxx = np.amax(self.na)
                divx = abs(maxx - minx) / (len(self.na) * 1.0)
                host.set_xlim(minx - divx, maxx + divx)
                miny = np.amin(self.ava[Dumpsys.TOTAL])
                maxy = np.amax(self.ava[Dumpsys.TOTAL])
                divy = ceil(abs(maxy - miny) / (len(self.ava[Dumpsys.TOTAL]) * 1.0))
                if DEBUG:
                    print(('setting host y lim {} {}').format(miny - divy, maxy + divy), file=sys.stderr)
                host.set_ylim(miny - divy, maxy + divy)
                host.set_xlabel('N')
                host.set_ylabel(Dumpsys.TOTAL)
                for k in self.ava.keys():
                    if k != Dumpsys.TOTAL:
                        par[k].set_ylabel(k)

                plots = {}
                if DEBUG:
                    print(('    host plot {} : {}').format(self.na, self.ava[Dumpsys.TOTAL]), file=sys.stderr)
                plots[Dumpsys.TOTAL], = host.plot(self.na, self.ava[Dumpsys.TOTAL], label=Dumpsys.TOTAL, linewidth=2)
                for k in self.ava.keys():
                    if k != Dumpsys.TOTAL:
                        if DEBUG:
                            print(('   {} plot {} : {}').format(k, self.na, self.ava[k]), file=sys.stderr)
                        plots[k], = par[k].plot(self.na, self.ava[k], label=k, linewidth=2)

                for k in self.ava.keys():
                    if k != Dumpsys.TOTAL:
                        miny = np.amin(self.ava[k])
                        maxy = np.amax(self.ava[k])
                        divy = ceil(abs(maxy - miny) / (len(self.ava[k]) * 1.0))
                        if DEBUG:
                            print(('setting {} y lim {}').format(k, (miny - divy, maxy + divy)), file=sys.stderr)
                        par[k].set_ylim(miny - divy, maxy + divy)

                host.legend()
            elif self.va:
                plt.xlabel('N')
                plt.ylabel('V')
                plt.plot(self.na, self.va, label='A')
            else:
                raise RuntimeError('No values to plot')
        elif _type == Dumpsys.FRAMESTATS:
            if DEBUG:
                print(('    plot: histogram {}').format(self.aava[Dumpsys.FRAMESTATS]), file=sys.stderr)
            n, bins, patches = plt.hist(self.aava[Dumpsys.FRAMESTATS])
            ymax = np.amax(n)
            x = []
            y = []
            for v in range(int(ceil(ymax)) + 1):
                x.append(1 / 60.0 * 1000)
                y.append(v)

            plt.plot(x, y, linewidth=2, color='c')
            x = []
            y = []
            for v in range(int(ceil(ymax)) + 1):
                x.append(1 / 30.0 * 1000)
                y.append(v)

            plt.plot(x, y, linewidth=2, color='r')
            plt.xlabel('ms')
            plt.ylabel('Frames')
        plt.title(title + ' ' + subtitle)
        plt.grid(True)
        plt.draw()
        if filename:
            plt.savefig(filename)
        else:
            plt.show()