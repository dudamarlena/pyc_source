# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\getweather.py
# Compiled at: 2020-01-15 16:12:19
# Size of source mod 2**32: 3704 bytes
"""
getweather - get specified weather information from forecast.io
==============================================================================

"""
import argparse, textwrap
from running.running import version

def main():
    description = 'Get specified weather information from forecast.io'
    epilog = textwrap.dedent('        paramsfile contains the following\n        \n            [getweather]\n            starttime = <starttime>\n            wxpoints = {"dist":[deltat,deltat,...],\n                "dist":[deltat,deltat,...],\n                ...\n                }\n        \n        where:\n            <starttime>\tstarting time for collection, in \'yyyy-mm-dd HH:MM\' format (no quotes, local timezone)\n            <dist>\tdistance in miles from the first gpx point\n            <deltat>\ttime in seconds from <starttime> for weather collection\n            \n        outfile is a csv file, with a header row, containing the following fields - see https://developer.forecast.io/docs/v2 Data Points for details\n        \n            exectime\ttime script was executed (Unix time format)\n            time\ttime forecast is predicting for (Unix time format)\n            lat\n            lon\n            temperature\n            humidity\n            dewpoint\tcalculated from temperature, humidity\n            windchill\tcalculated from temperature, windSpeed\n            heatindex\tcalculated from temperature, humidity\n            precipType\n            precipProbability\n            precipIntensity\n            windSpeed\n            windBearing\n            cloudCover\n            summary\n            pressure\n            visibility\n        ')
    parser = argparse.ArgumentParser(prog='getweather.py',
      formatter_class=(argparse.RawDescriptionHelpFormatter),
      description=description,
      epilog=epilog,
      version=('{0} {1}'.format('running', version.__version__)))
    parser.add_argument('gpxfile', help='gpx file containing course')
    parser.add_argument('paramsfile', help='file containing parameters')
    parser.add_argument('outfile', help='csv file containing output from queries')
    parser.add_argument('-a', '--apikey', help='API key to access forecast.io')
    args = parser.parse_args()


if __name__ == '__main__':
    main()