# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/extract_sites.py
# Compiled at: 2019-08-30 11:41:07
# Size of source mod 2**32: 1333 bytes
"""
This script generates a sites file compatible with the shapefile used in the project
"""
from argparse import ArgumentParser
from dbfread import DBF

def extract_data(**args):
    table = DBF(shapefile.split('.')[0] + '.dbf')


if __name__ == '__main__':
    parser = ArgumentParser(description="generate a csv file containing the model's sites from a shapefile", prog='extract_sites')
    parser.add_argument('-n', '--name', dest='name', help='Define which column to use for name')
    parser.add_argument('-g', '--geocode', dest='geocode',
      help='Column to use as geocode. Must be unique numeric id')
    parser.add_argument('-p', '--population', dest='population',
      help='Column to use for population size')
    parser.add_argument('-o', '--outfile', dest='outfile',
      default='sites.csv',
      help='name of the sites file (<something>.csv)')
    parser.add_argument('shapefile', metavar='shapefile', nargs=1, help='Shapefile for the model (.shp).')
    args = parser.parse_args()
    extract_data(**args)