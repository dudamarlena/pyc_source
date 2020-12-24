# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/model/BestConfigPlot.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 2084 bytes
from ..model.BestConfigTrace import BestConfigTrace

class BestConfigPlot:
    __doc__ = '\n    Class which prepares given data to plot in views\n    author: Julian Gebker\n    version: 1.0.0\n    '

    def __init__(self, plot_name: str, title: str, best_config_training: BestConfigTrace, best_config_validation: BestConfigTrace):
        """ Constructor
        :param plot_name: name of the plot is the name of the div element which shows the plot
        :param title: title of the plot
        :param best_config_training: BestConfigDynamic Object representing a list of metrics
        :param best_config_validation: BestConfigDynamic Object representing a list of metrics
        """
        self.plot_name = plot_name
        self.title = title
        self.best_config_training = best_config_training
        self.best_config_validation = best_config_validation

    def to_plot(self):
        """ Prints the containing data as javascript function
        :return: Returns the string containing a javascript to show the plot
        """
        result = str('var ' + self.best_config_training.trace_name + ' = { x: [' + self.best_config_training.values_x() + '], y: [' + self.best_config_training.values_y() + "], name: '" + self.best_config_training.trace_name + "', mode: '" + self.best_config_training.trace_mode + "', type: '" + self.best_config_training.trace_type + "'};")
        result += str('var ' + self.best_config_validation.trace_name + ' = { x: [' + self.best_config_validation.values_x() + '], y: [' + self.best_config_validation.values_y() + "], name: '" + self.best_config_validation.trace_name + "', mode: '" + self.best_config_validation.trace_mode + "', type: '" + self.best_config_validation.trace_type + "'};")
        result += str("var layout = { title: '" + str(self.title) + "'};")
        result += str('var data = [' + self.best_config_training.trace_name + ', ' + self.best_config_validation.trace_name + '];')
        result += str("Plotly.newPlot('" + str(self.plot_name) + "', data, layout);")
        return result