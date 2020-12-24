# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/plots/violin.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 21554 bytes
from seaborn.categorical import _ViolinPlotter
import matplotlib as mpl
from textwrap import dedent
import colorsys, numpy as np
from scipy import stats
import pandas as pd
from matplotlib.collections import PatchCollection
import matplotlib.patches as Patches, matplotlib.pyplot as plt, warnings
from seaborn import utils
from seaborn.utils import iqr, categorical_order, remove_na
from seaborn.algorithms import bootstrap
from seaborn.palettes import color_palette, husl_palette, light_palette, dark_palette
from seaborn.axisgrid import FacetGrid, _facet_docs

class ViolinPlotter(_ViolinPlotter):
    __doc__ = 'A class to extend the _ViolinPlotter class provided by Seaborn\n    '

    def __init__(self, x=None, y=None, hue=None, data=None, order=None, hue_order=None, bw='scott', cut=2, scale='area', scale_hue=True, gridsize=100, width=0.8, inner='box', split=False, dodge=True, orient=None, linewidth=None, color=None, palette=None, saturation=0.75, ax=None, outer=None, **kwargs):
        self.multi_color = False
        self.establish_variables(x, y, hue, data, orient, order, hue_order)
        self.establish_colors(color, palette, saturation)
        self.estimate_densities(bw, cut, scale, scale_hue, gridsize)
        self.gridsize = gridsize
        self.width = width
        self.dodge = dodge
        if inner is not None:
            if not any([inner.startswith('quart'),
             inner.startswith('box'),
             inner.startswith('stick'),
             inner.startswith('point'),
             inner.startswith('line')]):
                err = "Inner style '{}' not recognized".format(inner)
                raise ValueError(err)
        self.inner = inner
        if outer is not None:
            if isinstance(outer, dict):
                for i in outer.keys():
                    if not any([i.startswith('percent'),
                     i.startswith('inject')]):
                        err = "Outer style '{}' not recognized".format(outer)
                        raise ValueError(err)

            elif not any([outer.startswith('percent'),
             outer.startswith('injection')]):
                err = "Outer style '{}' not recognized".format(outer)
                raise ValueError(err)
        self.outer = outer
        if split:
            if self.hue_names is not None:
                if len(self.hue_names) != 2:
                    msg = "There must be exactly two hue levels to use `split`.'"
                    raise ValueError(msg)
        self.split = split
        if linewidth is None:
            linewidth = mpl.rcParams['lines.linewidth']
        self.linewidth = linewidth

    def establish_colors(self, color, palette, saturation):
        """Get a list of colors for the main component of the plots."""
        if self.hue_names is None:
            n_colors = len(self.plot_data)
        else:
            n_colors = len(self.hue_names)
        if color is None:
            if palette is None:
                current_palette = utils.get_color_cycle()
                if n_colors <= len(current_palette):
                    colors = color_palette(n_colors=n_colors)
                else:
                    colors = husl_palette(n_colors, l=0.7)
        else:
            if palette is None:
                if self.hue_names:
                    if self.default_palette == 'light':
                        colors = light_palette(color, n_colors)
                    else:
                        if self.default_palette == 'dark':
                            colors = dark_palette(color, n_colors)
                        else:
                            raise RuntimeError('No default palette specified')
                else:
                    colors = [
                     color] * n_colors
            else:
                colors = self.colors_from_palette(palette)
        rgb_colors = color_palette(colors)
        light_vals = [(colorsys.rgb_to_hls)(*c)[1] for c in rgb_colors]
        lum = min(light_vals) * 0.6
        gray = mpl.colors.rgb2hex((lum, lum, lum))
        self.colors = rgb_colors
        self.gray = gray

    def colors_from_palette(self, palette):
        """grab the colors from the chosen palette"""
        if self.hue_names is None:
            n_colors = len(self.plot_data)
        else:
            n_colors = len(self.hue_names)
        if isinstance(palette, dict):
            keys = list(palette.keys())
            n_colors = len(self.plot_data)
            if 'left' in keys and 'right' in keys or all(j in keys for j in self.hue_names):
                self.multi_color = True
                colors = [self._palette_or_color(palette[i], n_colors) for i in keys]
                colors = [[colors[0][i], colors[1][i]] for i in range(n_colors)]
                colors = [y for x in colors for y in x]
            return colors
        else:
            colors = self._palette_or_color(palette, n_colors)
            return colors

    def _palette_or_color(self, palette_entry, n_colors):
        """Determine if the palette is a block color or a palette
        """
        if isinstance(palette_entry, list):
            while len(palette_entry) < n_colors:
                palette_entry += palette_entry

            return palette_entry
        else:
            if 'color:' in palette_entry:
                color = palette_entry.split('color:')[1]
                color = self._flatten_string(color)
                return [
                 color] * n_colors
            return color_palette(palette_entry, n_colors)

    @staticmethod
    def _flatten_string(string):
        """Remove the trailing white space from a string"""
        return string.lstrip(' ')

    def draw_violins(self, ax):
        """Draw the violins onto `ax`."""
        fill_func = ax.fill_betweenx if self.orient == 'v' else ax.fill_between
        checkpoint = 0
        for i, group_data in enumerate(self.plot_data):
            kws = dict(edgecolor=(self.gray), linewidth=(self.linewidth))
            if self.plot_hues is None:
                support, density = self.support[i], self.density[i]
                if support.size == 0:
                    continue
                else:
                    if support.size == 1:
                        val = np.asscalar(support)
                        d = np.asscalar(density)
                        self.draw_single_observation(ax, i, val, d)
                        continue
                grid = np.ones(self.gridsize) * i
                fill_func(support,
 grid - density * self.dwidth,
 grid + density * self.dwidth, facecolor=self.colors[i], **kws)
                if self.inner is None:
                    pass
                else:
                    violin_data = remove_na(group_data)
                    if self.inner.startswith('box'):
                        self.draw_box_lines(ax, violin_data, support, density, i)
                    else:
                        if self.inner.startswith('quart'):
                            self.draw_quartiles(ax, violin_data, support, density, i)
                        else:
                            if self.inner.startswith('stick'):
                                self.draw_stick_lines(ax, violin_data, support, density, i)
                            else:
                                if self.inner.startswith('point'):
                                    self.draw_points(ax, violin_data, i)
                                else:
                                    if self.inner.startswith('line'):
                                        self.draw_single_line(ax, violin_data, i)
                        if self.outer is None:
                            continue
                        else:
                            self.draw_external_range(ax, violin_data, support, density, i)
            else:
                offsets = self.hue_offsets
                for j, hue_level in enumerate(self.hue_names):
                    support, density = self.support[i][j], self.density[i][j]
                    kws['facecolor'] = self.colors[j]
                    if self.multi_color:
                        kws['facecolor'] = self.colors[checkpoint]
                        checkpoint += 1
                    if not i:
                        if not self.multi_color:
                            self.add_legend_data(ax, self.colors[j], hue_level)
                        if support.size == 0:
                            continue
                        else:
                            if support.size == 1:
                                val = np.asscalar(support)
                                d = np.asscalar(density)
                                if self.split:
                                    d = d / 2
                                at_group = i + offsets[j]
                                self.draw_single_observation(ax, at_group, val, d)
                                continue
                        if self.split:
                            grid = np.ones(self.gridsize) * i
                            if j:
                                fill_func(support, 
                                 grid, 
                                 (grid + density * self.dwidth), **kws)
                            else:
                                fill_func(support, 
                                 (grid - density * self.dwidth), 
                                 grid, **kws)
                            if self.inner is None:
                                pass
                            else:
                                hue_mask = self.plot_hues[i] == hue_level
                                violin_data = remove_na(group_data[hue_mask])
                                if self.inner.startswith('quart'):
                                    self.draw_quartiles(ax, violin_data, support, density, i, [
                                     'left', 'right'][j])
                                else:
                                    if self.inner.startswith('stick'):
                                        self.draw_stick_lines(ax, violin_data, support, density, i, [
                                         'left', 'right'][j])
                                    if self.outer is None:
                                        continue
                                    else:
                                        self.draw_external_range(ax, violin_data, support, density, i, [
                                         'left', 'right'][j])
                                if not j:
                                    pass
                                else:
                                    violin_data = remove_na(group_data)
                                    if self.inner.startswith('box'):
                                        self.draw_box_lines(ax, violin_data, support, density, i)
                                    else:
                                        if self.inner.startswith('point'):
                                            self.draw_points(ax, violin_data, i)
                                        elif self.inner.startswith('line'):
                                            self.draw_single_line(ax, violin_data, i)
                        else:
                            grid = np.ones(self.gridsize) * (i + offsets[j])
                            fill_func(support, 
                             (grid - density * self.dwidth), 
                             (grid + density * self.dwidth), **kws)
                            if self.inner is None:
                                pass
                            else:
                                hue_mask = self.plot_hues[i] == hue_level
                                violin_data = remove_na(group_data[hue_mask])
                                if self.inner.startswith('box'):
                                    self.draw_box_lines(ax, violin_data, support, density, i + offsets[j])
                                else:
                                    if self.inner.startswith('quart'):
                                        self.draw_quartiles(ax, violin_data, support, density, i + offsets[j])
                                    else:
                                        if self.inner.startswith('stick'):
                                            self.draw_stick_lines(ax, violin_data, support, density, i + offsets[j])
                                        elif self.inner.startswith('point'):
                                            self.draw_points(ax, violin_data, i + offsets[j])

    def annotate_axes(self, ax):
        """Add descriptive labels to an Axes object."""
        if self.orient == 'v':
            xlabel, ylabel = self.group_label, self.value_label
        else:
            xlabel, ylabel = self.value_label, self.group_label
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        else:
            if ylabel is not None:
                ax.set_ylabel(ylabel)
            else:
                if self.orient == 'v':
                    ax.set_xticks(np.arange(len(self.plot_data)))
                    ax.set_xticklabels(self.group_names)
                else:
                    ax.set_yticks(np.arange(len(self.plot_data)))
                    ax.set_yticklabels(self.group_names)
            if self.orient == 'v':
                ax.xaxis.grid(False)
                ax.set_xlim((-0.5), (len(self.plot_data) - 0.5), auto=None)
            else:
                ax.yaxis.grid(False)
                ax.set_ylim((-0.5), (len(self.plot_data) - 0.5), auto=None)
        if self.hue_names is not None:
            if not self.multi_color:
                leg = ax.legend(loc='best')
                if self.hue_title is not None:
                    leg.set_title(self.hue_title)
                    try:
                        title_size = mpl.rcParams['axes.labelsize'] * 0.85
                    except TypeError:
                        title_size = mpl.rcParams['axes.labelsize']

                    prop = mpl.font_manager.FontProperties(size=title_size)
                    leg._legend_title_box._text.set_font_properties(prop)

    def draw_single_line(self, ax, data, center):
        """Draw a single line through the middle of the violin"""
        kws = dict(color=(self.gray), edgecolor=(self.gray))
        upper = np.max(data)
        lower = np.min(data)
        ax.plot([center, center], [lower, upper], linewidth=(self.linewidth),
          color=(self.gray))

    def _plot_single_line(self, ax, center, y, density, split=None, color=None):
        """Plot a single line on a violin plot"""
        width = self.dwidth * np.max(density) * 1.1
        color = self.gray if color is None else color
        if split == 'left':
            ax.plot([center - width, center], [y, y], linewidth=(self.linewidth),
              color=color)
        else:
            if split == 'right':
                ax.plot([center, center + width], [y, y], linewidth=(self.linewidth),
                  color=color)
            else:
                ax.plot([center - width, center + width], [y, y], linewidth=(self.linewidth),
                  color=color)

    def draw_external_range(self, ax, data, support, density, center, split=None):
        """Draw lines extending outside of the violin showing given range"""
        width = self.dwidth * np.max(density) * 1.1
        if isinstance(self.outer, dict):
            if 'percentage' in list(self.outer.keys()):
                percent = float(self.outer['percentage'])
                lower, upper = np.percentile(data, [100 - percent, percent])
                h1 = np.min(data[(data >= upper)])
                h2 = np.max(data[(data <= lower)])
                self._plot_single_line(ax, center, h1, density, split=split)
                self._plot_single_line(ax, center, h2, density, split=split)
            if any('inject' in i for i in list(self.outer.keys())):
                key = [i for i in list(self.outer.keys()) if 'inject' in i]
                if any('injection:' in i for i in list(self.outer.keys())):
                    split = key[0].split('injection:')[1]
                    split = self._flatten_string(split)
                injection = self.outer[key[0]]
                if isinstance(injection, list):
                    self._plot_single_line(ax,
                      center, (injection[center]), density, split=split, color='r')
                else:
                    self._plot_single_line(ax,
                      center, injection, density, split=split, color='r')
        elif isinstance(self.outer, str):
            if 'percent' in self.outer:
                percent = self.outer.split('percent:')[1]
                percent = float(self._flatten_string(percent))
                percent += (100 - percent) / 2.0
                lower, upper = np.percentile(data, [100 - percent, percent])
                h1 = np.min(data[(data >= upper)])
                h2 = np.max(data[(data <= lower)])
                self._plot_single_line(ax, center, h1, density, split=split)
                self._plot_single_line(ax, center, h2, density, split=split)
            if 'inject' in self.outer:
                if 'injection:' in self.outer:
                    split = self.outer.split('injection:')[1]
                    split = self._flatten_string(split)
                injection = self.outer.split('injection:')[1]
                self._plot_single_line(ax,
                  center, injection, density, split=split, color='r')

    def plot(self, ax):
        """Make the violin plot."""
        self.draw_violins(ax)
        self.annotate_axes(ax)
        if self.orient == 'h':
            ax.invert_yaxis()


def violinplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, bw='scott', cut=2, scale='area', scale_hue=True, gridsize=100, width=0.8, inner='box', split=False, dodge=True, orient=None, linewidth=None, color=None, palette=None, saturation=0.75, ax=None, outer=None, **kwargs):
    plotter = ViolinPlotter(x, y, hue, data, order, hue_order, bw,
      cut, scale, scale_hue, gridsize, width,
      inner, split, dodge, orient, linewidth, color,
      palette, saturation, outer=outer)
    if ax is None:
        ax = plt.gca()
    plotter.plot(ax)
    return ax