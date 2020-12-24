# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/interface.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 10222 bytes
"""
Created on Fri Jan 15 22:48:50 2016

@author: steven
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np, bms, math, itertools, networkx as nx

class ModelDrawer:

    def __init__(self, model):
        """ Create a new drag handler and connect it to the figure's event system.
        If the figure handler is not given, the current figure is used instead
        """
        import matplotlib.pyplot as plt
        self.l = 0.05
        self.dragged = None
        self.model = model
        self.element_from_artist = {}
        self.artists_from_element = {}
        self.noeud_clic = None
        self.position = nx.spring_layout(self.model.graph)
        plt.ioff()
        self.fig, self.ax = plt.subplots(1, 1)
        for variable in self.model.signals:
            points = np.array((5, 2))
            xp, yp = self.position[variable]
            points = np.array([[xp - 1.5 * self.l, yp - 0.5 * self.l], [xp - 0.5 * self.l, yp - 0.5 * self.l],
             [
              xp, yp], [xp - 0.5 * self.l, yp + 0.5 * self.l], [xp - 1.5 * self.l, yp + 0.5 * self.l]])
            p = mpatches.Polygon(points, facecolor='white', edgecolor='black',
              picker=10)
            self.ax.add_patch(p)
            t = self.ax.text((xp - 1 * self.l), yp, (variable.short_name), color='black', ha='center',
              multialignment='center',
              verticalalignment='center')
            self.element_from_artist[p] = variable
            self.artists_from_element[variable] = [
             p, t, [], []]

        for variable in self.model.variables:
            pos = self.position[variable]
            t = self.ax.text((pos[0]), (pos[1]), (variable.short_name), color='black', ha='center', picker=10, multialignment='center',
              bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
            self.element_from_artist[t] = variable
            self.artists_from_element[variable] = [
             t, None, [], []]

        for block in self.model.blocks:
            hb = 0.5 * (1 + max(len(block.inputs), len(block.outputs))) * self.l
            pb = self.position[block][:]
            p = mpatches.Rectangle((pb[0] - 0.5 * self.l, pb[1] - hb / 2), height=hb, width=(self.l),
              edgecolor='black',
              facecolor='#CCCCCC',
              picker=10)
            self.ax.add_patch(p)
            t = self.ax.text((pb[0]), (pb[1]), (block.LabelBlock()), color='black',
              multialignment='center',
              verticalalignment='center')
            self.element_from_artist[p] = block
            self.artists_from_element[block] = [p, t]
            for iv, variable in enumerate(block.inputs):
                pv = self.position[variable]
                pcb = self.position[block][:]
                a = mpatches.FancyArrowPatch(pv,
                  (pb[0] - 0.5 * self.l, pb[1] + hb / 2 - 0.5 * (iv + 1) * self.l), arrowstyle='-|>')
                self.ax.add_patch(a)
                self.artists_from_element[block].append(a)
                self.artists_from_element[variable][3].append(a)

            for iv, variable in enumerate(block.outputs):
                pv = self.position[variable]
                pb = self.position[block]
                a = mpatches.FancyArrowPatch((
                 pb[0] + 0.5 * self.l, pb[1] + hb / 2 - 0.5 * (iv + 1) * self.l),
                  pv, arrowstyle='-|>')
                self.ax.add_patch(a)
                self.artists_from_element[block].append(a)
                self.artists_from_element[variable][2].append(a)

        plt.axis('equal')
        plt.margins(0.05)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick_event)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release_event)
        plt.show()

    def on_pick_event(self, event):
        self.selected_patch = event.artist

    def on_release_event(self, event):
        """ Update text position and redraw"""
        element = self.element_from_artist[self.selected_patch]
        self.position[element] = [event.xdata, event.ydata]
        if isinstance(element, bms.Signal):
            artists = self.artists_from_element[element]
            points = np.array((5, 2))
            xp, yp = self.position[element]
            points = np.array([[xp - 1.5 * self.l, yp - 0.5 * self.l], [xp - 0.5 * self.l, yp - 0.5 * self.l],
             [
              xp, yp], [xp - 0.5 * self.l, yp + 0.5 * self.l], [xp - 1.5 * self.l, yp + 0.5 * self.l]])
            artists[0].set_xy(xy=points)
            artists[1].set(x=(xp - 1 * self.l), y=yp)
            for artist in artists[3]:
                artist.set_positions((xp, yp), None)

        else:
            if isinstance(element, bms.Variable):
                artists = self.artists_from_element[element]
                pos = self.position[element]
                artists[0].set(x=(pos[0]), y=(pos[1]))
                for artist in artists[2]:
                    artist.set_positions(None, pos)

                for artist in artists[3]:
                    artist.set_positions(pos, None)

            else:
                if isinstance(element, bms.Block):
                    artists = self.artists_from_element[element]
                    pb = self.position[element][:]
                    hb = 0.5 * (1 + max(len(element.inputs), len(element.outputs))) * self.l
                    artists[0].set(xy=(pb[0] - 0.5 * self.l, pb[1] - hb / 2))
                    artists[1].set(x=(pb[0]), y=(pb[1]))
                    li = len(element.inputs)
                    for i in range(2, li + 2):
                        artists[i].set_positions(None, (pb[0] - 0.5 * self.l, pb[1] + hb / 2 - 0.5 * (i + 1 - 2) * self.l))

                    for i in range(2 + li, len(artists)):
                        artists[i].set_positions((
                         pb[0] + 0.5 * self.l, pb[1] + hb / 2 - 0.5 * (i + 1 - 2 - li) * self.l), None)

                plt.draw()
                return True