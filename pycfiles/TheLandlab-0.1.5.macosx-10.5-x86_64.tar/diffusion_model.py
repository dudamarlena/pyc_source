# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/diffusion/diffusion_model.py
# Compiled at: 2014-09-23 12:37:24
"""

Landlab model of 2D diffusion, using DiffusionComponent.

Created July 2013 GT
Last updated August 2013 GT

"""
import sys
from landlab import ModelParameterDictionary
from landlab import create_and_initialize_grid
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_node_grid
import diffusion

class DiffusionModel:

    def initialize(self, input_stream=None):
        if input_stream == None:
            input_stream = str(raw_input('Enter name of input file: '))
        inputs = ModelParameterDictionary(input_stream)
        self.grid = create_and_initialize_grid(inputs)
        self.diffusion_component = diffusion.DiffusionComponent(self.grid)
        self.diffusion_component.initialize(input_stream)
        self.run_duration = inputs.get('RUN_DURATION', ptype=float)
        self.opt_netcdf_output = inputs.get('OPT_FILE_OUTPUT', ptype='bool')
        self.opt_display_output = inputs.get('OPT_DISPLAY_OUTPUT', ptype='bool')
        self.setup_output_timing(inputs)
        return

    def setup_output_timing(self, inputs):
        if self.opt_netcdf_output:
            self.netcdf_output_interval = inputs.get('FILE_OUTPUT_INTERVAL', ptype=float)
            self.next_file_output = self.netcdf_output_interval
        else:
            self.next_file_output = self.run_duration + 1.0
        if self.opt_display_output:
            self.display_output_interval = inputs.get('DISPLAY_OUTPUT_INTERVAL', ptype=float)
            self.next_display_output = self.display_output_interval
        else:
            self.next_display_output = self.run_duration + 1.0
        self.find_next_stop_time()
        self.current_time = 0.0

    def handle_output(self):
        if self.current_time >= self.next_display_output:
            self.do_display_output()
            self.next_display_output += self.display_output_interval
        if self.current_time >= self.next_file_output:
            self.do_file_output()
            self.next_file_output += self.file_output_interval

    def find_next_stop_time(self):
        self.next_stop_time = min(self.run_duration, self.next_file_output, self.next_display_output)

    def do_display_output(self):
        if type(self.grid) is RasterModelGrid:
            print 'This is a raster grid'
        else:
            print 'non-raster grid'
        imshow_node_grid(self.grid, self.diffusion_component.z)

    def do_file_output(self):
        print 'File output goes here'

    def update(self):
        self.diffusion_component.run_one_step()

    def run(self):
        while self.current_time < self.run_duration:
            self.diffusion_component.run_until(self.next_stop_time)
            self.current_time = self.next_stop_time
            print self.current_time
            self.handle_output()
            self.find_next_stop_time()

    def finalize(self):
        pass


def main():
    difmod = DiffusionModel()
    if len(sys.argv) == 1:
        input_file_name = None
    else:
        input_file_name = sys.argv[1]
    difmod.initialize(input_file_name)
    difmod.run()
    difmod.finalize()
    return


if __name__ == '__main__':
    main()