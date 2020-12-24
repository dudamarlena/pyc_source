# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/tests/run_raster_model_grid_builtin_unit_test.py
# Compiled at: 2014-09-23 12:37:24
"""
Runs RasterModelGrid's unit_test() method
"""
import landlab as ll

def main():
    mg = ll.RasterModelGrid()
    mg._unit_test()


if __name__ == '__main__':
    main()