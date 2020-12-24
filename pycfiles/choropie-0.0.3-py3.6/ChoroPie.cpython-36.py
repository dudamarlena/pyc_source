# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/choropie/ChoroPie.py
# Compiled at: 2017-11-22 17:03:13
# Size of source mod 2**32: 26496 bytes
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
import matplotlib.path as mplPath
from choropie import poly_functs as sc

def get_shp_attributes(shp_file):
    """
    Convenience function for retrieving shp attributes.

    Parameters:
        shp_file (string): path to shp file without extension.
    """
    m = Basemap()
    m.readshapefile(shp_file, name='area')
    return m.area_info


def find_shp_key(area_index, shp_lst):
    """
    Iterate through shp file attributes to find the key which matches the input index which will be used in Choropie.

    Parameters:
        area_index (list of strings): area_names as indices. same index to be passed into choropie parameters like size_data.
        shp_lst (list of dicts): same object as returned by get_shp_attributes or Basemap."area"_info.
    """
    for item in area_index:
        for dct in shp_lst:
            for key, val in dct.items():
                if item == val:
                    return key


def coords_in_area(locations, coords, shp_file, shp_key):
    """
    Given a list of locations and corresponding coordinates, can determine in which shp file area polygon to plot each location.

    Parameters:
        locations (list of strings): Location names.
        coords (list of tuples): location coordinates: (lat, lon).
        shp_file (string): path to shp file without extension.
        shp_key (string): the attribute in the shape file which contains the area polygons

    Returns:
        Parallel lists of: locations, area which each location belongs to
    """
    m = Basemap()
    m.readshapefile(shp_file, name='area')
    area_names = [area[shp_key] for area in m.area_info]
    area_shapes = list(zip(area_names, m.area))
    return_lst = []
    for location, (lat, lon) in zip(locations, coords):
        x, y = m(lon, lat)
        coord = (x, y)
        for area_name, shape in area_shapes:
            poly = mplPath.Path(shape)
            if poly.contains_point(coord) is True:
                return_lst.append((location, area_name))

    return list(zip(*return_lst))


class ChoroPie(Basemap):
    __doc__ = "\n    A Basemap/Matplotlib toolkit which allows the simplified creation of choropleth maps with colorbars using shapefiles, and the combined plotting of pie charts within the centroid coordinates of the shapefile's polygons.\n\n\n    Attributes:\n        choropie:\n            area_names (list of tuples): area names extracted from shape files corresponding to each shape (may have duplicates).\n            indexer (dict): area_name as key, index position in shapes and corr_shapes as value. use to index shapes and corr_shapes.\n            shapes (list): area_names, area (list of vector coordinates) from shp file.\n            corr_shapes (list of tuples): corrected  vector coordinates (takes into account any translation/rescaling) with associated area names (may have duplicates).\n            centroids (list of tuples): original polygon centroids with associated area names.\n            corr_centroids: corrected centroids (takes into account any translation/rescaling) with associated area names.\n            area_info (list): shp attributes as read by Basemap.\n            annotations (dict): holds matplotlib.pyplot.annotate objects for each area that are created after calling set_pie_offset method.\n\n        matplotlib:\n            fig (figure): matplotlib figure instance.\n            ax (axes): matplotlib axes instance where the map projection is plotted.\n            mpl_paths (dict): area, list of path collection memory addresses.\n            mpl_polygons (dict): area, list of polygons memory addresses.\n            x_lims (tuple): initial x axis limits.\n            y_lims (tuple): initial y axis limits.\n    "

    def __set_shape(self, shape, origin, lat, lon, scale=1):
        """
        Used in loops when translating and scaling an area. Accepts individual shapes as arguments.
        Do not use! Use translate_shapes method instead.
        """
        distances = np.array([(np.array(coord) - np.array(origin)) * np.float(scale) for coord in shape])
        new_origin = np.array(self(lon, lat))
        shape = new_origin + distances
        return (
         shape, tuple(new_origin))

    def __set_centroids(self, shape):
        """
        Used in loops for determining centroids. Accepts individual shapes as arguments.
        """
        poly_areas = [(poly, sc.area_for_polygon(poly)) for poly in shape]
        max_area = max([area for poly, area in poly_areas])
        max_poly = [poly for poly, area in poly_areas if area == max_area][0]
        poly_centroid = sc.centroid_for_polygon(max_poly)
        return poly_centroid

    def __draw_pie(self, X, Y, colors, pie_data, size_ratios, size):
        """
        Used in loops to draw pie charts. Returns matplotlib PathCollection object.
        """
        mpl_paths_sin = []
        if len(pie_data) == 1:
            path = self.ax.scatter(X,
              Y, s=size, facecolor=(self.pie_dict[colors[0]]), edgecolor='black', zorder=3)
            mpl_paths_sin.append(path)
        else:
            xy = []
            start = 0.0
            for ratio in pie_data:
                x = [
                 0] + np.cos(np.linspace(2 * np.pi * start, 2 * np.pi * (start + ratio), 30)).tolist()
                y = [0] + np.sin(np.linspace(2 * np.pi * start, 2 * np.pi * (start + ratio), 30)).tolist()
                xy.append(list(zip(x, y)))
                start += ratio

            for colors, xyi in zip(colors, xy):
                if size_ratios is not None:
                    path = self.ax.scatter(X, Y, marker=(xyi, 0), s=(np.array(size) * (np.array(size_ratios.loc[colors] / size_ratios.sum()) * 2 + 0.5)),
                      alpha=1,
                      facecolor=(self.pie_dict[colors]),
                      edgecolor='black',
                      zorder=3)
                    mpl_paths_sin.append(path)
                else:
                    path = self.ax.scatter(X, Y, marker=(
                     xyi, 0),
                      s=size,
                      facecolor=(self.pie_dict[colors]),
                      edgecolor='black',
                      zorder=3)
                    mpl_paths_sin.append(path)

        return mpl_paths_sin

    def __init__(self, basemap_kwargs, shp_file, shp_key, figsize=(22, 12)):
        """
        Initialization:
        Preps for plotting. Does the heavy lifting of finding polygon areas and centroids.

        Parameters:
        Positional:
            basemap_kwargs (dict): kwargs to pass into Basemap.
            shp_file (string): path to a shp_file without the ".shp" extension in the string.
            shp_key (string): the attribute in the shape file which contains the indices used in the data.
        Optional:
            drawbounds (bool): passed into Basemap.readshapefile method. draws borders on map.
            figsize (tuple): matplotlib figure size.
        """
        (Basemap.__init__)(self, **basemap_kwargs)
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_axes([0.1, 0.1, 0.95, 0.95], frame_on=False)
        self.readshapefile(shp_file,
          'area', drawbounds=True, zorder=1)
        self.area_names = [areas[shp_key] for areas in self.area_info]
        self.indexer = {}
        self.shapes = list(zip(self.area_names, self.area))
        self.corr_shapes = []
        self.centroids = {}
        self.corr_centroids = {}
        for i, (name_glob, shape) in enumerate(self.shapes):
            self.corr_shapes.append((name_glob, shape))
            try:
                if self.area_names[i] != self.area_names[(i - 1)]:
                    start = i
                    self.indexer.update({name_glob: start})
                if self.area_names[i] != self.area_names[(i + 1)]:
                    end = i + 1
                    shapes = [shapes for name, shapes in self.corr_shapes[start:end]]
                    poly_centroid = self._ChoroPie__set_centroids(shapes)
                    self.centroids.update({name_glob: poly_centroid})
                    self.corr_centroids.update({name_glob: poly_centroid})
            except IndexError:
                pass

        self.x_lims = self.ax.get_xlim()
        self.y_lims = self.ax.get_ylim()
        self.annotations = {}

    def choro_plot(self, num_colors, cmap, color_data, alpha=1):
        """
        Plot the choropleths.

        Parameters:
        Positional:
            num_colors (numeric): determines number of colors to be used in the plot.
            cmap (matplotlib.cmap): string representation of matplotlib colormap ie. "hot_r"
            color_data (series): series with the area name as the single index and a column for the numerical variable to be plotted as values.
            alpha (numeric): opacity of fills.

        Attributes:
            __scheme (list): list of rgb values from matplotlib
            __bins (np.array): bins corresponding to colors and values in color_data
        """
        cm = plt.get_cmap(cmap)
        self._ChoroPie__scheme = [cm(i / num_colors) for i in range(1, num_colors + 1)]
        self._ChoroPie__bins = np.linspace(color_data.min(), color_data.max(), num_colors + 1)
        series_bins = pd.Series(index=(color_data.index), data=(np.digitize(color_data, np.append(self._ChoroPie__bins[:-1], self._ChoroPie__bins[(-1)] + 1e-07)) - 1))
        self.mpl_polygons = {}
        for name_glob, shape in self.corr_shapes:
            if name_glob in series_bins:
                color = self._ChoroPie__scheme[series_bins.loc[name_glob]]
                poly = Polygon(shape, facecolor=color, edgecolor='black',
                  zorder=2,
                  alpha=alpha)
                self.ax.add_patch(poly)
                if name_glob not in self.mpl_polygons:
                    self.mpl_polygons.update({name_glob: [poly]})
                else:
                    self.mpl_polygons[name_glob].append(poly)

        if 'Alaska' in self.area_names:
            self.translate_shapes('Alaska', 28, -114, 0.3)
        if 'Hawaii' in self.area_names:
            self.translate_shapes('Hawaii', 25, -107, 0.75)

    def insert_colorbar(self, colorbar_title=None, colorbar_loc_kwargs=dict(), colorbar_title_kwargs=dict(), colorbarbase_kwargs=dict()):
        """
        Insert a colorbar next to the parent axes.

        Parameters:
        Optional:
            colorbar_title (string): title for the colorbar.
            colorbar_loc_kwargs (dict): kwargs to pass into matplotlib.colorbar.make_axes -
                used to adjust positioning of colorbar. pass in a keyword argument location with the options "right, left, top, bottom" to change location. defaults overwritten.
            colorbarbase_kwargs (dict): kwargs to pass into colorbarbase instance. defaults overwritten.
            colorbar_title_kwargs (dict): kwargs to pass into axes.set_ylabel method. defaults overwritten.
        Attributes:
            ax_colorbar (axes): matplotlib axes instances for the colorbar.
        """
        try:
            self.ax_colorbar.remove()
        except Exception:
            pass

        default = dict(fraction=0.05,
          location='right',
          aspect=40,
          shrink=0.75,
          pad=0.01)
        default.update(colorbar_loc_kwargs)
        self.ax_colorbar, kw = (mpl.colorbar.make_axes)(
         (self.ax), **default)
        cmap = mpl.colors.ListedColormap(self._ChoroPie__scheme)
        orientation = 'vertical'
        if default['location'] == 'right' or default['location'] == 'left':
            orientation = 'vertical'
            default = dict(ax=(self.ax_colorbar), cmap=cmap, ticks=(self._ChoroPie__bins), boundaries=(self._ChoroPie__bins),
              orientation='vertical')
        else:
            orientation = 'horizontal'
            default = dict(ax=(self.ax_colorbar), cmap=cmap, ticks=(self._ChoroPie__bins), boundaries=(self._ChoroPie__bins),
              orientation='horizontal')
        default.update(colorbarbase_kwargs)
        cb = (mpl.colorbar.ColorbarBase)(**default)
        cb.ax.set_xticklabels(self._ChoroPie__bins)
        default = dict(labelpad=15, fontdict=dict(fontsize=14, fontweight='bold',
          verticalalignment='center',
          horizontalalignment='center'))
        default.update(colorbar_title_kwargs)
        if orientation == 'vertical':
            (cb.ax.set_ylabel)(colorbar_title, **default)
        else:
            (cb.ax.set_xlabel)(colorbar_title, **default)

    def pie_plot(self, pie_data, pie_dict, size_data=1000, scale_factor_size=1, scale_factor_ratios=0.5, size_ratios=None):
        """
        Plots pies at centroids.

        Parameters:
        Positional:
            pie_data (series): determines the pie slices (traditional). multiindex with area names followed by pie features and a column of data. The data within an area should add up to the whole (as all pie charts do).
            pie_dict (dict): dictionary with pie slices as keys and colors as values.
        Optional:
            size_data (series or numeric): size of each pie chart at the centroid. single index with area names. if an int, then all pies are plotted to same size. can compare feature for each entire area.
            scale_factor_size (numeric): smaller numbers shrink differences in size between largest and smallest pies.
            size_ratios (series): can be used to compare a feature across pie slices. determines size of the radius / length of each slice. multiindex with area names followed by pie features and a column of data.

        Notes:
            Make sure first level of all series indexes match shp area names.

        Attributes:
            pie_dict (dict): returns the dictionary for colors.
        """
        pie_data.index.rename(['key1', 'key2'], inplace=True)
        df_sums = pie_data.groupby(level=0).sum()
        df_sums.rename('sums', inplace=True)
        pie_data = pd.merge((pie_data.reset_index()), (df_sums.reset_index()), on=[
         'key1'],
          how='inner').set_index(['key1', 'key2'])
        pie_data = pie_data[[column for column in pie_data.columns if 'sums' not in str(column)][0]] / pie_data['sums']
        if isinstance(size_ratios, pd.Series):
            size_ratios = size_ratios ** scale_factor_ratios
        if isinstance(size_data, pd.Series):
            size_data = size_data ** scale_factor_size
            size_data = size_data / size_data.sum() * len(size_data) * 1500
        self.pie_dict = pie_dict
        self.mpl_paths = {}

        def loop():
            x, y = poly_centroid
            series_sorted = pie_data[name_glob].sort_values()
            if name_glob == 'District of Columbia':
                x *= 1.105
                self.ax.annotate(name_glob, xy=(x, y), xycoords='data', xytext=(
                 x, y * 0.85),
                  textcoords='data',
                  color='black',
                  ha='center',
                  arrowprops=dict(arrowstyle='fancy', color='red'))
            path = self._ChoroPie__draw_pie(X=x, Y=y, colors=(series_sorted.index),
              size_ratios=size_ratios_args,
              pie_data=series_sorted,
              size=size_data_args)
            self.mpl_paths.update({name_glob: path})

        for name_glob, poly_centroid in self.corr_centroids.items():
            if name_glob in pie_data:
                if isinstance(size_ratios, pd.Series):
                    size_ratios_args = size_ratios.loc[name_glob]
                else:
                    size_ratios_args = size_ratios
                if isinstance(size_data, pd.Series):
                    if name_glob in size_data:
                        size_data_args = size_data.loc[name_glob]
                        loop()
                else:
                    size_data_args = size_data
                    loop()

        if 'Alaska' in self.area_names:
            self.set_pie_loc('Alaska', 28, -114)
        if 'Hawaii' in self.area_names:
            self.set_pie_loc('Hawaii', 25, -107)

    def insert_pie_legend(self, legend_loc='upper left', pie_legend_kwargs=dict()):
        """
        Inserts legend for pie plots.

        Parameters:
        Optional:
            legend_loc (string): 'upper left', 'upper right', 'lower left', 'lower right.' can be overwritten by pie_legend_kwards if bbox_to_anchor is passed.
            pie_legend_kwargs (dict): kwargs to pass into legend axes creation. defaults overwritten.
        """
        try:
            patches = []
        except AttributeError:
            print('call method "pie_plot" first')

        for label, color in self.pie_dict.items():
            patches.append(Patch(label=label,
              facecolor=color,
              edgecolor='black'))

        bbox_anchor = (0.03, 0.97)
        if legend_loc == 'upper right':
            bbox_anchor = (
             bbox_anchor[1], bbox_anchor[1])
        else:
            if legend_loc == 'lower right':
                bbox_anchor = (
                 bbox_anchor[1], bbox_anchor[0])
            else:
                if legend_loc == 'lower left':
                    bbox_anchor = (
                     bbox_anchor[0], bbox_anchor[0])
        legend_default = dict(handles=patches,
          title=None,
          loc=legend_loc,
          bbox_to_anchor=bbox_anchor,
          edgecolor='black')
        legend_default.update(pie_legend_kwargs)
        (self.ax.legend)(**legend_default)

    def translate_shapes(self, area_name, lat, lon, scale=1):
        """
        Manually translate/scale an area. Fixes corr_shapes attribute inplace.

        Parameters:
            area_name (string): name of area to translate/scale.
            lat (numeric): new lat.
            lon (numeric): new lon.
            scale (numeric): scale factor. only affects area shape.
        """
        start = self.indexer[area_name]
        origin = self.centroids[area_name]
        for i, (name, shapes) in enumerate(self.shapes[start:]):
            if area_name == name:
                shape, new_origin = self._ChoroPie__set_shape(shapes, origin, lat, lon, scale)
                self.corr_shapes[start + i] = (
                 name, shape)
                self.mpl_polygons[area_name][i].set_xy(shape)
            else:
                break

    def set_pie_loc(self, area_name, lat, lon):
        """
        Translates a pie chart. Fixes corr_centroids attrbite in place.

        Parameters:
            area_name (string): name of area to translate/scale.
            lat (numeric): new lat.
            lon (numeric): new lon.
        """
        new_origin = self(lon, lat)
        self.corr_centroids[area_name] = new_origin
        for paths in self.mpl_paths[area_name]:
            paths.set_offset_position('data')
            paths.set_offsets(new_origin)

    def set_pie_offset(self, area_name, lat_offset=0, lon_offset=0, arrow=True, annotate_kwargs=dict()):
        """
        Offsets pies by lat and lon. If called with lat_offset as 0 and lon_offset as 0, resets pie position.

        Paraters:
        Positional:
            area_name (string): name of area to translate/scale.
        Optional:
            lat_offset (numeric): positive to send right, negative to send left.
            lon_offset (numeric): positive to send right, negative to send left.
            annotations_kwargs (dict): paramaters to pass into matplotlib.pyplot.annotate
        """
        old_origin = self.centroids[area_name]
        lon, lat = self(*old_origin, **{'inverse': True})
        lon_new = lon + lon_offset
        lat_new = lat + lat_offset
        new_origin = self(lon_new, lat_new)
        for paths in self.mpl_paths[area_name]:
            paths.set_offset_position('data')
            paths.set_offsets(new_origin)

        if area_name in self.annotations:
            try:
                self.annotations[area_name].remove()
            except Exception as e:
                del self.annotations['area_name']
                print('exception: ', e)

        default = dict(s='', xy=(new_origin[0], new_origin[1]), xycoords='data', xytext=(
         old_origin[0], old_origin[1]),
          textcoords='data',
          color='black',
          ha='center',
          arrowprops=dict(arrowstyle='fancy', color='red'))
        default.update(annotate_kwargs)
        self.annotations.update({area_name: (self.ax.annotate)(**default)})
        self.corr_centroids[area_name] = new_origin

    def translate_pies_shapes(self, area_name, lat, lon, scale=1):
        """
        Manually translate/scale an area and corresponding pie chart. Fixes corr_shapes and corr_centroids attributes inplace.
        """
        self.translate_shapes(area_name, lat, lon, scale)
        self.set_pie_loc(area_name, lat, lon)

    def clear_elements(self):
        """
        Delete all choropleth and pie elements on the plot.
        """
        for child in self.ax.get_children():
            if 'legend' and 'anno' in str(child).lower():
                child.remove()

        for axes in self.fig.axes[1:]:
            axes.remove()

        try:
            for mpl_objects in [pie for lst in self.mpl_paths.values() for pie in lst]:
                try:
                    mpl_objects.remove()
                except Exception:
                    continue

        except Exception as e:
            print('No Pies Plotted!')
            print('exception: ', e)

        try:
            for mpl_objects in [poly for lst in self.mpl_polygons.values() for poly in lst]:
                try:
                    mpl_objects.remove()
                except Exception:
                    continue

        except Exception as e:
            print('No Polygons Plotted!')
            print('exception: ', e)

    def zoom_to_area(self, area_names):
        """
        Reduces the main axes size to the size of a specific area. Return the original x_lims and y_lims as a tuple. Call back method ChoroPie.ax.set_xlim and set_ylim to return to original scale.

        Parameters:
            area_names (list of strings): names of areas to translate/scale.
        """
        coords = []
        for area_name in area_names:
            start = self.indexer[area_name]
            for name, shapes in self.corr_shapes[start:]:
                if area_name == name:
                    for shape in shapes:
                        coords.append(shape)

                else:
                    break

        x_coords, y_coords = list(zip(*coords))
        x0, x1 = min(x_coords), max(x_coords)
        y0, y1 = min(y_coords), max(y_coords)
        self.ax.set_xlim(x0, x1)
        self.ax.set_ylim(y0, y1)
        for name, polys in self.mpl_polygons.items():
            if name in area_names:
                for poly in polys:
                    poly.set_visible(True)

            else:
                for poly in polys:
                    poly.set_visible(False)

        for name, paths in self.mpl_paths.items():
            if name in area_names:
                for paths in paths:
                    paths.set_visible(True)

            else:
                for paths in paths:
                    paths.set_visible(False)

    def zoom_home(self):
        """
        If zoom_to_area method was called, this zooms the main axes to the initial position.
        """
        (self.ax.set_xlim)(*self.x_lims)
        (self.ax.set_ylim)(*self.y_lims)
        for name, polys in self.mpl_polygons.items():
            for poly in polys:
                poly.set_visible(True)

        for name, paths in self.mpl_paths.items():
            for path in paths:
                path.set_visible(True)