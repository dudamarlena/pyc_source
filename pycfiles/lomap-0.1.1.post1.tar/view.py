# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alphan/Documents/svn/academic/bu/research/implementation/lomap-ltl_optimal_multi-agent_planner/trunk/examples/ijrr2014_rec_hor/view.py
# Compiled at: 2015-04-14 16:52:50
import itertools as it, matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from matplotlib import animation

class View:

    def __init__(self, env, quad):
        """Creates a figure window and initializes view parameters 
                for the environment and the quadrotor.
                """
        self.fig = plt.figure(figsize=(12.52, 9.39))
        self.ax = self.fig.gca()
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])
        self.ax.xaxis.set_ticks(range(-100, 100))
        self.ax.yaxis.set_ticks(range(-100, 100))
        self.margin = quad.sensing_range / 2
        plt.axis('scaled')
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.env = env
        self.quad = quad
        self.define_quadrotor()
        self.define_local()
        self.draw_regions()
        self.path_line = None
        self.arrow = None
        self.draw_quad()
        return

    def define_quadrotor(self):
        cell_cmd = "plt.Rectangle((0, 0), 1, 1, edgecolor = 'black', fill=False, linewidth = 0.5)"
        self.quad_cells = [ [ dict() for y in range(0, self.quad.sensing_range) ] for x in range(0, self.quad.sensing_range) ]
        for x, y in it.product(range(0, self.quad.sensing_range), repeat=2):
            self.quad_cells[x][y] = {'cell': eval(cell_cmd), 'text': self.ax.text(0.5, 0.5, 'X', fontsize=10, ha='center', va='center', weight='bold')}
            self.ax.add_artist(self.quad_cells[x][y]['cell'])

        blade_cmd = 'plt.Circle((0,0),0.20,fill=False,linewidth=1)'
        self.quad_blades = [None] * 4
        for i in range(0, 4):
            self.quad_blades[i] = eval(blade_cmd)
            self.ax.add_artist(self.quad_blades[i])

        return

    def get_vertices_of_cell(self, cell):
        x, y = cell
        lower_left = (x - 0.5, y - 0.5)
        lower_right = (x + 0.5, y - 0.5)
        upper_left = (x - 0.5, y + 0.5)
        upper_right = (x + 0.5, y + 0.5)
        return (lower_left, upper_left, upper_right, lower_right, lower_left)

    def draw_regions(self):
        """Draws the regions
                """
        global_reqs = self.env.global_reqs
        min_x, max_x, min_y, max_y = (
         self.quad.x, self.quad.x, self.quad.y, self.quad.y)
        for cell in global_reqs.iterkeys():
            color = global_reqs[cell]['color']
            vertices = self.get_vertices_of_cell(cell)
            x, y = zip(*vertices)
            self.ax.fill(x, y, color, edgecolor=color)
            min_x = min(min_x, min(x))
            min_y = min(min_y, min(y))
            max_x = max(max_x, max(x))
            max_y = max(max_y, max(y))

        plt.axis((min_x - self.margin, max_x + self.margin, min_y - self.margin, max_y + self.margin))
        self.ax.tight = True

    def define_local(self):
        """Defines polygons for locally sensed requests
                """
        local = self.env.local_reqs
        self.local_polygons = dict()
        for cell in local.iterkeys():
            color = local[cell]['color']
            vertices = self.get_vertices_of_cell(cell)
            self.local_polygons[cell] = plt.Polygon(vertices, facecolor=color, edgecolor=color, zorder=0)

    def draw_local(self):
        """Draws locally sensed requests
                """
        for name in self.local_polygons:
            artist = self.local_polygons[name]
            if artist not in self.ax.get_children():
                if self.env.local_reqs[name]['on']:
                    self.ax.add_artist(artist)
            elif not self.env.local_reqs[name]['on']:
                self.local_polygons[name].remove()

    def draw_quad(self):
        self.draw_local()
        txty = (
         (-0.2, 0.2), (0.2, 0.2), (0.2, -0.2), (-0.2, -0.2))
        for blade, (tx, ty) in it.izip(self.quad_blades, txty):
            trans = Affine2D().translate(tx, ty).translate(self.quad.x, self.quad.y) + self.ax.transData
            blade.set_transform(trans)

        for x, y in it.product(range(0, self.quad.sensing_range), repeat=2):
            cell_x, cell_y = self.quad.get_sensing_cell_global_coords((x, y))
            cell_trans = Affine2D().translate(-0.5, -0.5).translate(cell_x, cell_y) + self.ax.transData
            self.quad_cells[x][y]['cell'].set_transform(cell_trans)
            self.quad_cells[x][y]['text'].set_transform(cell_trans)
            props = self.quad.sensed[x][y]['local_reqs'] | self.quad.sensed[x][y]['global_reqs']
            new_text = (',').join(props)
            self.quad_cells[x][y]['text'].set_text(new_text)

        if self.path_line in self.ax.get_children():
            self.path_line.remove()
            self.arrow.remove()

    def draw_path(self, vertices):
        xs, ys = zip(*vertices)
        dx = (xs[(-1)] - xs[(-2)]) / 1.5
        dy = (ys[(-1)] - ys[(-2)]) / 1.5
        self.path_line = self.ax.plot(xs, ys, 'r-', lw=2)[0]
        self.arrow = self.ax.arrow(xs[(-2)], ys[(-2)], dx, dy, head_width=0.5, head_length=0.5, fc='r', ec='w')