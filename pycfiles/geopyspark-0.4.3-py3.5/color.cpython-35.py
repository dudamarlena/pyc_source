# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/color.py
# Compiled at: 2018-12-10 10:02:50
# Size of source mod 2**32: 11899 bytes
"""This module contains functions needed to create color maps used in coloring tiles,
PNGs, and GeoTiffs.
"""
import struct, numpy as np
from geopyspark import get_spark_context
from geopyspark.geotrellis.histogram import Histogram
from geopyspark.geopyspark_utils import ensure_pyspark
ensure_pyspark()
from geopyspark.geotrellis.constants import ClassificationStrategy
__all__ = [
 'get_colors_from_colors', 'get_colors_from_matplotlib', 'ColorMap']

def get_colors_from_colors(colors):
    """Returns a list of integer colors from a list of Color objects from the
    colortools package.

    Args:
        colors ([colortools.Color]): A list of color stops using colortools.Color

    Returns:
        [int]
    """
    return [struct.unpack('>L', bytes(c.rgba))[0] for c in colors]


def get_colors_from_matplotlib(ramp_name, num_colors=256):
    """Returns a list of color breaks from the color ramps defined by Matplotlib.

    Args:
        ramp_name (str): The name of a matplotlib color ramp. See the matplotlib documentation for
            a list of names and details on each color ramp.
        num_colors (int, optional): The number of color breaks to derive from the named map.

    Returns:
        [int]
    """
    try:
        import colortools, matplotlib.cm as mpc
    except:
        raise Exception('matplotlib>=2.0.0 and colortools>=0.1.2 required')

    ramp = mpc.get_cmap(ramp_name)
    return [struct.unpack('>L', bytes(map(lambda x: int(x * 255), ramp(x / (num_colors - 1)))))[0] for x in range(0, num_colors)]


nlcd_color_map = {0: 0, 
 11: 1382061567, 
 12: 4294967295, 
 21: 3531698431, 
 22: 3992979199, 
 23: 2566916607, 
 31: 3216552447, 
 32: 2526517503, 
 33: 942234111, 
 41: 1469929471, 
 42: 711671295, 
 43: 2797566975, 
 51: 3131464959, 
 61: 1162944511, 
 71: 3503270655, 
 81: 3435671551, 
 82: 2640125439, 
 83: 3449243647, 
 84: 2813042687, 
 85: 3867814655, 
 91: 3067672063, 
 92: 3067672063}

class ColorMap(object):
    __doc__ = 'A class that wraps a GeoTrellis ColorMap class.\n\n    Args:\n        cmap (py4j.java_gateway.JavaObject): The ``JavaObject`` that represents the GeoTrellis ColorMap.\n\n    Attributes:\n        cmap (py4j.java_gateway.JavaObject): The ``JavaObject`` that represents the GeoTrellis ColorMap.\n    '

    def __init__(self, cmap):
        self.cmap = cmap

    @classmethod
    def build(cls, breaks, colors=None, no_data_color=0, fallback=0, classification_strategy=ClassificationStrategy.LESS_THAN_OR_EQUAL_TO):
        """Given breaks and colors, build a ``ColorMap`` object.

        Args:
            breaks (dict or list or ``np.ndarray`` or :class:`~geopyspark.geotrellis.Histogram`): If a
                ``dict`` then a mapping from tile values to colors, the latter represented as integers
                e.g., 0xff000080 is red at half opacity. If a ``list`` then tile values that
                specify breaks in the color mapping. If a ``Histogram`` then a histogram from which
                breaks can be derived.
            colors (str or list, optional):  If a ``str`` then the name of a matplotlib color ramp.
                If a ``list`` then either a list of colortools ``Color`` objects or a list
                of integers containing packed RGBA values. If ``None``, then the ``ColorMap`` will
                be created from the ``breaks`` given.
            no_data_color(int, optional): A color to replace NODATA values with
            fallback (int, optional): A color to replace cells that have no
                value in the mapping
            classification_strategy (str or :class:`~geopyspark.geotrellis.constants.ClassificationStrategy`, optional):
                A string giving the strategy for converting tile values to colors. e.g., if
                ``ClassificationStrategy.LESS_THAN_OR_EQUAL_TO`` is specified, and the break map is
                {3: 0xff0000ff, 4: 0x00ff00ff}, then values up to 3 map to red, values from above 3
                and up to and including 4 become green, and values over 4 become the fallback color.

        Returns:
            :class:`~geopyspark.geotrellis.color.ColorMap`
        """
        pysc = get_spark_context()
        if isinstance(breaks, dict):
            return ColorMap.from_break_map(breaks, no_data_color, fallback, classification_strategy)
        if isinstance(colors, str):
            color_list = get_colors_from_matplotlib(colors)
        else:
            if isinstance(colors, list):
                if all(isinstance(c, int) for c in colors):
                    color_list = colors
                else:
                    color_list = get_colors_from_colors(colors)
            else:
                raise ValueError('Could not construct ColorMap from the given colors', colors)
        if isinstance(breaks, np.ndarray):
            breaks = list(breaks)
        if isinstance(breaks, list):
            return ColorMap.from_colors(breaks, color_list, no_data_color, fallback, classification_strategy)
        if isinstance(breaks, Histogram):
            return ColorMap.from_histogram(breaks, color_list, no_data_color, fallback, classification_strategy)
        raise ValueError('Could not construct ColorMap from the given breaks', breaks)

    @classmethod
    def from_break_map(cls, break_map, no_data_color=0, fallback=0, classification_strategy=ClassificationStrategy.LESS_THAN_OR_EQUAL_TO):
        """Converts a dictionary mapping from tile values to colors to a ColorMap.

        Args:
            break_map (dict): A mapping from tile values to colors, the latter
                represented as integers e.g., 0xff000080 is red at half opacity.
            no_data_color(int, optional): A color to replace NODATA values with
            fallback (int, optional): A color to replace cells that have no
                value in the mapping
            classification_strategy (str or :class:`~geopyspark.geotrellis.constants.ClassificationStrategy`, optional):
                A string giving the strategy for converting tile values to colors. e.g., if
                ``ClassificationStrategy.LESS_THAN_OR_EQUAL_TO`` is specified, and the break map is
                {3: 0xff0000ff, 4: 0x00ff00ff}, then values up to 3 map to red, values from above 3
                and up to and including 4 become green, and values over 4 become the fallback color.

        Returns:
            :class:`~geopyspark.geotrellis.color.ColorMap`
        """
        pysc = get_spark_context()
        if all(isinstance(x, int) for x in break_map.keys()):
            fn = pysc._gateway.jvm.geopyspark.geotrellis.ColorMapUtils.fromMap
            strat = ClassificationStrategy(classification_strategy).value
            return cls(fn(break_map, no_data_color, fallback, strat))
        if all(isinstance(x, float) for x in break_map.keys()):
            fn = pysc._gateway.jvm.geopyspark.geotrellis.ColorMapUtils.fromMapDouble
            strat = ClassificationStrategy(classification_strategy).value
            return cls(fn(break_map, no_data_color, fallback, strat))
        raise TypeError('Break map keys must be either int or float.')

    @classmethod
    def from_colors(cls, breaks, color_list, no_data_color=0, fallback=0, classification_strategy=ClassificationStrategy.LESS_THAN_OR_EQUAL_TO):
        """Converts lists of values and colors to a ``ColorMap``.

        Args:
            breaks (list): The tile values that specify breaks in the color
                mapping.
            color_list ([int]): The colors corresponding to the values in the
                breaks list, represented as integers---e.g., 0xff000080 is red
                at half opacity.
            no_data_color(int, optional): A color to replace NODATA values with
            fallback (int, optional): A color to replace cells that have no
                value in the mapping
            classification_strategy (str or :class:`~geopyspark.geotrellis.constants.ClassificationStrategy`, optional):
                A string giving the strategy for converting tile values to colors. e.g., if
                ``ClassificationStrategy.LESS_THAN_OR_EQUAL_TO`` is specified, and the break map is
                {3: 0xff0000ff, 4: 0x00ff00ff}, then values up to 3 map to red, values from above 3
                and up to and including 4 become green, and values over 4 become the fallback color.

        Returns:
            :class:`~geopyspark.geotrellis.color.ColorMap`
        """
        pysc = get_spark_context()
        if all(isinstance(x, int) for x in breaks):
            fn = pysc._gateway.jvm.geopyspark.geotrellis.ColorMapUtils.fromBreaks
            strat = ClassificationStrategy(classification_strategy).value
            return cls(fn(breaks, color_list, no_data_color, fallback, strat))
        else:
            fn = pysc._gateway.jvm.geopyspark.geotrellis.ColorMapUtils.fromBreaksDouble
            arr = [float(br) for br in breaks]
            strat = ClassificationStrategy(classification_strategy).value
            return cls(fn(arr, color_list, no_data_color, fallback, strat))

    @classmethod
    def from_histogram(cls, histogram, color_list, no_data_color=0, fallback=0, classification_strategy=ClassificationStrategy.LESS_THAN_OR_EQUAL_TO):
        """Converts a wrapped GeoTrellis histogram into a ``ColorMap``.

        Args:
            histogram (:class:`~geopyspark.geotrellis.Histogram`): A ``Histogram`` instance;
                specifies breaks
            color_list ([int]): The colors corresponding to the values in the
                breaks list, represented as integers e.g., 0xff000080 is red
                at half opacity.
            no_data_color(int, optional): A color to replace NODATA values with
            fallback (int, optional): A color to replace cells that have no
                value in the mapping
            classification_strategy (str or :class:`~geopyspark.geotrellis.constants.ClassificationStrategy`, optional):
                A string giving the strategy for converting tile values to colors. e.g., if
                ``ClassificationStrategy.LESS_THAN_OR_EQUAL_TO`` is specified, and the break map is
                {3: 0xff0000ff, 4: 0x00ff00ff}, then values up to 3 map to red, values from above 3
                and up to and including 4 become green, and values over 4 become the fallback color.

        Returns:
            :class:`~geopyspark.geotrellis.color.ColorMap`
        """
        pysc = get_spark_context()
        fn = pysc._gateway.jvm.geopyspark.geotrellis.ColorMapUtils.fromHistogram
        strat = ClassificationStrategy(classification_strategy).value
        return cls(fn(histogram.scala_histogram, color_list, no_data_color, fallback, strat))

    @staticmethod
    def nlcd_colormap():
        """Returns a color map for NLCD tiles.

        Returns:
            :class:`~geopyspark.geotrellis.color.ColorMap`
        """
        return ColorMap.from_break_map(nlcd_color_map)