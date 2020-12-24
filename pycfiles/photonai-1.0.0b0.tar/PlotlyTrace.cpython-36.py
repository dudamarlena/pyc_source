# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/model/PlotlyTrace.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 3988 bytes
import numpy as np

class PlotlyTrace:
    __doc__ = ' Class represents a trace made with Plotly\n    author: Julian Gebker\n    version: 1.0.0\n    '

    def __init__(self, variable_name: str, mode: str='markers', trace_type: str='scatter', trace_size: int=0, trace_color: str='', with_error: bool=False, colorscale: list=None, marker_line_width: int=None, marker_line_color: str=None):
        """ Constructor
        :param variable_name: Variable name in javascript
        :param mode: Trace's mode (default: 'markers')
        :param trace_type: Trace's type (default: 'scatter')
        """
        self.variable_name = variable_name
        self.mode = mode
        self.trace_type = trace_type
        self.x = []
        self.y = []
        self.z = []
        self.error_y = []
        self.trace_size = trace_size
        self.with_error = with_error
        self.trace_color = trace_color
        self.colorscale = colorscale
        self.marker_line_width = marker_line_width
        self.marker_line_color = marker_line_color

    def add_x(self, x):
        """ function to add new value for x axis
        :param x: value for x axis
        """
        self.x.append(x)

    def add_y(self, y):
        """ function to add new value for y axis
        :param y: value for y axis
        """
        self.y.append(y)

    def add_z(self, z):
        """ function to add new value for z axis
                :param z: value for z axis
                """
        self.z.append(z)

    def add_error_y(self, y):
        """ function to add new value for y axis
        :param y: add y error value
        """
        self.error_y.append(y)

    def get_x_to_string(self) -> str:
        """ function to print all x values comma separated
        :return: comma separated string of x values
        """
        result = ''
        for item in self.x:
            if isinstance(item, list):
                result += '['
                for iitem in item:
                    result += "'" + str(iitem) + "',"

                result.rstrip(',')
                result += '],'
            else:
                result += "'" + str(item) + "',"

        return result.rstrip(',')

    def get_y_to_string(self) -> str:
        """ function to print all y values comma separated
        :return: comma separated string of y values
        """
        result = ''
        for item in self.y:
            if isinstance(item, list):
                result += '['
                for iitem in item:
                    result += "'" + str(iitem) + "',"

                result.rstrip(',')
                result += '],'
            else:
                result += "'" + str(item) + "',"

        return result.rstrip(',')

    def get_err_y_to_string(self) -> str:
        """ function to print all err_y values comma separated
        :return: comma separated string of y error values
        """
        result = ''
        for item in self.error_y:
            if isinstance(item, list):
                result += '['
                for iitem in item:
                    result += "'" + str(iitem) + "',"

                result.rstrip(',')
                result += '],'
            else:
                result += "'" + str(item) + "',"

        return result.rstrip(',')

    def get_z_to_string(self, as_numbers: bool=False) -> str:
        result = ''
        for item in self.z:
            if isinstance(item, (list, np.ndarray)):
                result += '['
                for iitem in item:
                    if as_numbers:
                        result += str(iitem) + ','
                    else:
                        result += "'" + str(iitem) + "',"

                result = result.rstrip(',')
                result += '],'
            else:
                if as_numbers:
                    result += "'" + str(item) + "',"
                else:
                    result += str(item) + ','

        return result.rstrip(',')