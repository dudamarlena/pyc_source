# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gruffy/area.py
# Compiled at: 2013-01-27 08:32:55
from gruffy import base
from pgmagick import Color, DrawableList, DrawableFillColor, DrawableStrokeColor, DrawableScaling, DrawableFillOpacity, DrawablePolyline, Coordinate, CoordinateList

class Area(base.Base):
    """Area Graph Object
    """

    def draw(self):
        """override to draw() method in Base Class."""
        Area.__base__.draw(self)
        if not self.has_gdata:
            return
        x_increment = self.graph_width / float(self.column_count - 1)
        dl = DrawableList()
        dl.append(DrawableStrokeColor(Color('transparent')))
        for data_row in self.norm_data:
            poly_points = CoordinateList()
            prev_x = prev_y = 0.0
            dl.append(DrawableFillColor(Color(data_row['color'])))
            if type(self.transparent) is float:
                dl.append(DrawableFillOpacity(self.transparent))
            else:
                if self.transparent is True:
                    dl.append(DrawableFillOpacity(base.DEFAULT_TRANSPARENCY))
                for index, data_point in enumerate(data_row['values']):
                    new_x = self.graph_left + x_increment * index
                    new_y = self.graph_top + (self.graph_height - data_point * self.graph_height)
                    if prev_x > 0 and prev_y > 0:
                        poly_points.append(Coordinate(new_x, new_y))
                    else:
                        poly_points.append(Coordinate(self.graph_left, self.graph_bottom - 1))
                        poly_points.append(Coordinate(new_x, new_y))
                    self.draw_label(new_x, index)
                    prev_x = new_x
                    prev_y = new_y

            poly_points.append(Coordinate(self.graph_right, self.graph_bottom - 1))
            poly_points.append(Coordinate(self.graph_left, self.graph_bottom - 1))
            dl.append(DrawablePolyline(poly_points))

        dl.append(DrawableScaling(self.scale, self.scale))
        self.base_image.draw(dl)