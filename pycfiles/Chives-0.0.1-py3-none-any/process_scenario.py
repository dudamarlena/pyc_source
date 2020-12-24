# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chitwanabm\process_scenario.py
# Compiled at: 2013-01-28 16:44:26
__doc__ = '\nWrapper to run R scripts processing scenario results.\n'
import os, sys, argparse, subprocess
from pkg_resources import resource_filename

def main():
    parser = argparse.ArgumentParser(description='Run the chitwanabm agent-based model (ABM).')
    parser.add_argument(dest='directory', metavar='directory', type=str, default=None, help='Path to a folder of ChitwanABM run results.')
    parser.add_argument('--Rscript', dest='Rscript', metavar='Rscript_binary', type=str, default='/usr/bin/Rscript', help='Path to the Rscript binary.')
    args = parser.parse_args()
    if not os.path.exists(args.Rscript):
        sys.exit('Must provide a valid path to Rscript binary.')
    scenario_path = args.directory
    print 'Running calculations for %s' % scenario_path
    batch_calc_script = resource_filename(__name__, 'R/batch_calculations.R')
    try:
        output = subprocess.check_output([args.Rscript, batch_calc_script, scenario_path], cwd=sys.path[0], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print 'Problem running calculations %s: %s' % (scenario_path, e.output)
        sys.exit(1)

    print 'Running making plots for %s' % scenario_path
    batch_plot_script = resource_filename(__name__, 'R/batch_plots.R')
    try:
        output = subprocess.check_output([args.Rscript, batch_plot_script, scenario_path], cwd=sys.path[0], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print 'Problem making plots for %s: %s' % (scenario_path, e.output)
        sys.exit(1)

    finished_file = open(os.path.join(scenario_path, 'SCENARIO_PROCESSED_OK'), 'w')
    finished_file.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())