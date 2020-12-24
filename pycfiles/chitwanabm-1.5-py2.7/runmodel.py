# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chitwanabm\runmodel.py
# Compiled at: 2013-01-29 19:40:54
"""
Wrapper to run a set of Chitwan ABM model runs: Reads in input parameters, then 
calls routines to initialize and run the model, and output model statistics.

NOTE: Borrows code from matplotlib, particularly for rcsetup functions.
"""
import os, sys, getopt, time, pickle, tempfile, subprocess, socket, csv, numpy as np, argparse, logging, shutil
from pkg_resources import resource_filename
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
temp_log_file = tempfile.NamedTemporaryFile(delete=False)
temp_log = logging.FileHandler(temp_log_file.name)
temp_log.setLevel(logging.DEBUG)
log_file_formatter = logging.Formatter('%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
temp_log.setFormatter(log_file_formatter)
root_logger.addHandler(temp_log)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log_console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%I:%M:%S%p')
ch.setFormatter(log_console_formatter)
root_logger.addHandler(ch)

def main():
    global rcParams
    parser = argparse.ArgumentParser(description='Run the chitwanabm agent-based model (ABM).')
    parser.add_argument('--rc', dest='rc_file', metavar='RC_FILE', type=str, default=None, help='Path to a rc file to initialize a model run with custom parameters')
    parser.add_argument('--log', metavar='LEVEL', type=str, default='info', help='The logging threshold for logging to the console')
    parser.add_argument('--logf', metavar='LEVEL', type=str, default='debug', help='The logging threshold for logging to the log file')
    parser.add_argument('--tail', dest='tail', action='store_const', const=True, default=False, help='Tail the logfile with the default tail application specified in the rc parameters')
    parser.add_argument('--output-path', dest='output_path', default=None, help='Path in which to store the model output (overrides any value set in the rc-file)')
    parser.add_argument('--run-id', dest='run_ID_number', default=None, help='Run ID number (automatically generated if it is not specified)')
    args = parser.parse_args()
    ch_level = getattr(logging, args.log.upper(), None)
    if not isinstance(ch_level, int):
        logger.critical('Invalid log level: %s' % args.log)
    root_logger.handlers[1].setLevel(ch_level)
    fh_level = getattr(logging, args.logf.upper(), None)
    if not isinstance(fh_level, int):
        logger.critical('Invalid log level: %s' % args.logf)
    root_logger.handlers[0].setLevel(fh_level)
    from chitwanabm import rc_params
    root_logger.handlers[0].setLevel(fh_level)
    rc_params.load_default_params('chitwanabm')
    if not args.rc_file == None and not os.path.exists(args.rc_file):
        logger.critical('Custom rc file %s does not exist' % args.rc_file)
    rc_params.initialize('chitwanabm', args.rc_file)
    rcParams = rc_params.get_params()
    from chitwanabm.initialize import generate_world
    from chitwanabm.modelloop import main_loop
    from pyabm.file_io import write_single_band_raster
    from pyabm.utility import save_git_diff
    from pyabm import __version__ as pyabm_version
    from chitwanabm import __version__ as chitwanabm_version
    if args.output_path != None:
        scenario_path = os.path.join(args.output_path, rcParams['scenario.name'])
        if not os.path.exists(args.output_path):
            try:
                os.mkdir(args.output_path)
            except OSError:
                logger.critical('Could not create output folder %s' % scenario_path)
                return 1

    else:
        scenario_path = os.path.join(rcParams['model.resultspath'], rcParams['scenario.name'])
    if not os.path.exists(scenario_path):
        try:
            os.mkdir(scenario_path)
        except OSError:
            logger.critical('Could not create scenario directory %s' % scenario_path)
            return 1

    if args.run_ID_number == None:
        hostname = socket.gethostname()
        run_ID_number = time.strftime('%Y%m%d-%H%M%S') + '_' + hostname
        results_path = os.path.join(scenario_path, run_ID_number)
        try:
            os.mkdir(results_path)
        except OSError:
            logger.critical('Could not create results directory %s' % results_path)
            return 1

    else:
        run_ID_number = args.run_ID_number
        results_path = os.path.join(scenario_path, run_ID_number)
        try:
            os.mkdir(results_path)
        except OSError:
            logger.critical('Could not create results directory %s' % results_path)
            return 1

        person_event_log_file_path = os.path.join(results_path, 'person_events.log')
        person_event_log_file = open(person_event_log_file_path, mode='w')
        person_event_log_header = (',').join(['time', 'event',
         'pid', 'hid', 'nid', 'rid', 'gender', 'age',
         'ethnicity', 'mother_id', 'father_id',
         'spouseid', 'marrtime', 'schooling',
         'num_children', 'alive', 'is_away',
         'is_initial_agent', 'is_in_migrant',
         'mother_num_children',
         'mother_years_schooling',
         'mother_work',
         'father_years_schooling', 'father_work',
         'parents_contracep'])
        person_event_log_file.write(person_event_log_header + '\n')
        person_event_log_file.close()
        person_event_fh = logging.FileHandler(os.path.join(results_path, 'person_events.log'), mode='a')
        person_event_fh.setLevel(logging.INFO)
        person_event_fh.setFormatter(logging.Formatter('%(modeltime)s,%(message)s,%(personinfo)s'))

        class PassEventFilter(logging.Filter):

            def filter(self, record):
                logger_name = getattr(record, 'name', None)
                return 'person_events' in logger_name

        person_event_fh.addFilter(PassEventFilter())
        person_event_logger = logging.getLogger('person_events')
        person_event_logger.addHandler(person_event_fh)
        log_file_path = os.path.join(results_path, 'chitwanabm.log')
        shutil.copyfile(temp_log_file.name, log_file_path)
        temp_log_file.close()
        root_logger.handlers.remove(temp_log)
        temp_log.close()
        os.unlink(temp_log_file.name)
        new_fh = logging.FileHandler(log_file_path, mode='a')
        new_fh.setLevel(fh_level)
        new_fh.setFormatter(log_file_formatter)
        root_logger.addHandler(new_fh)

        class DontPassEventFilter(logging.Filter):

            def filter(self, record):
                logger_name = getattr(record, 'name', None)
                return 'person_events' not in logger_name

        for handler in root_logger.handlers:
            handler.addFilter(DontPassEventFilter())

    if args.tail:
        try:
            subprocess.Popen([rcParams['path.tail_binary'], log_file_path], cwd=results_path)
        except:
            logger.warning('Error tailing model log file: %s' % sys.exc_info()[1])

    world = generate_world()
    if world == 1:
        logger.critical('Error initializing model world')
        return 1
    else:
        start_time = time.localtime()
        logger.info('Beginning model run %s' % run_ID_number)
        run_results, time_strings = main_loop(world, results_path)
        end_time = time.localtime()
        logger.info('Finished model run number %s' % run_ID_number)
        if rcParams['save_pickled_end_results']:
            logger.info('Saving results')
            pop_data_file = os.path.join(results_path, 'run_results.P')
            output = open(pop_data_file, 'w')
            pickle.dump(run_results, output)
            output.close()
        run_results = reformat_run_results(run_results)
        run_results_csv_file = os.path.join(results_path, 'run_results.csv')
        write_results_csv(run_results, run_results_csv_file, 'neighid')
        world.write_NBHs_to_csv('END', results_path)
        DEM_data_file = os.path.join(results_path, 'chitwanabm_DEM.tif')
        array, gt, prj = world.get_DEM_data()
        write_single_band_raster(array, gt, prj, DEM_data_file)
        world_mask_data_file = os.path.join(results_path, 'chitwanabm_world_mask.tif')
        array, gt, prj = world.get_world_mask_data()
        write_single_band_raster(array, gt, prj, world_mask_data_file)
        git_diff_file = os.path.join(results_path, 'git_diff.patch')
        commit_hash = save_git_diff(sys.path[0], git_diff_file)
        time_csv_file = os.path.join(results_path, 'time.csv')
        write_time_csv(time_strings, time_csv_file)
        if rcParams['model.make_plots']:
            logger.info('Plotting population results')
            Rscript_binary = rcParams['path.Rscript_binary']
            plot_pop_script = resource_filename(__name__, 'R/plot_pop.R')
            try:
                output = subprocess.check_output([Rscript_binary, plot_pop_script,
                 results_path], cwd=sys.path[0], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                logger.exception('Problem running plot_pop.R. R output: %s' % e.output)

            if rcParams['save_NBH_data']:
                logger.info('Plotting LULC results')
                plot_LULC_script = resource_filename(__name__, 'R/plot_LULC.R')
                try:
                    output = subprocess.check_output([Rscript_binary, plot_LULC_script,
                     results_path], cwd=sys.path[0], stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    logger.exception('Problem running plot_LULC.R. R output: %s' % e.output)

            if rcParams['save_psn_data']:
                logger.info('Plotting persons results')
                plot_psns_script = resource_filename(__name__, 'R/plot_psns_data.R')
                try:
                    output = subprocess.check_output([Rscript_binary, plot_psns_script,
                     results_path], cwd=sys.path[0], stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    logger.exception('Problem running plot_psns_data.R. R output: %s' % e.output)

        speed = (time.mktime(end_time) - time.mktime(start_time)) / (len(time_strings['timestep']) / rcParams['model.timestep'])
        start_time_string = time.strftime('%m/%d/%Y %I:%M:%S %p', start_time)
        end_time_string = time.strftime('%m/%d/%Y %I:%M:%S %p', end_time)
        run_RC_file = os.path.join(results_path, 'chitwanabmrc')
        RC_file_header = '# This file contains the parameters used for a chitwanabm model run.\n# Model run ID:\t\t%s\n# Start time:\t\t%s\n# End time:\t\t\t%s\n# Run speed:\t\t%.4f\n# Code SHA:\t\t\t%s\n# Code version:\t\t%s\n# PyABM version:\t%s' % (run_ID_number, start_time_string, end_time_string,
         speed, commit_hash, chitwanabm_version, pyabm_version)
        rc_params.write_RC_file(run_RC_file, RC_file_header)
        finished_file = open(os.path.join(results_path, 'RUN_FINISHED_OK'), 'w')
        finished_file.close()
        logger.info('Finished saving results for model run %s' % run_ID_number)
        return 0


def reformat_run_results(run_results):
    """
    For convenience and speed while running the model, the population results 
    are stored in a dictionary keyed as [timestep][variable][neighborhoodid] = 
    value. The write_results_csv function (written to export them in a 
    conveient format for input into R) needs them to be keyed as 
    [timestep][neighborhoodid][variable] = value. This function will reformat 
    the run_results to make them compatible with the write_results_csv 
    function.
    """
    run_results_fixed = {}
    for timestep in run_results.keys():
        run_results_fixed[timestep] = {}
        for variable in run_results[timestep].keys():
            for ID in run_results[timestep][variable]:
                if ID not in run_results_fixed[timestep]:
                    run_results_fixed[timestep][ID] = {}
                run_results_fixed[timestep][ID][variable] = run_results[timestep][variable][ID]

    return run_results_fixed


def write_time_csv(time_strings, time_csv_file):
    """
    Write a CSV file for conversion of timestep number, float, etc. to actual 
    year and month (for plotting).
    """
    out_file = open(time_csv_file, 'wb')
    csv_writer = csv.writer(out_file)
    col_headers = sorted(time_strings.keys())
    csv_writer.writerow(col_headers)
    columns = []
    for col_header in col_headers:
        if columns == []:
            columns = np.array(time_strings[col_header])
        else:
            columns = np.vstack((columns, time_strings[col_header]))

    columns = np.transpose(columns)
    csv_writer.writerows(columns)
    out_file.close()


def write_results_csv(results, csv_file, ID_col_name):
    """Write to CSV the saved model run data."""
    timesteps = sorted(results.keys())
    IDs = []
    for timestep in timesteps:
        IDs.extend(results[timestep].keys())

    IDs = sorted(np.unique(IDs))
    categories = []
    for timestep in timesteps:
        for ID in results[timestep].keys():
            categories.extend(results[timestep][ID].keys())

    categories = sorted(np.unique(categories))
    out_file = open(csv_file, 'wb')
    csv_writer = csv.writer(out_file)
    var_names = [ID_col_name]
    for category in categories:
        for timestep in timesteps:
            var_name = category + '.' + str(timestep)
            var_names.append(var_name)

    csv_writer.writerow(var_names)
    for ID in IDs:
        row = [ID]
        for category in categories:
            for timestep in timesteps:
                if ID in results[timestep]:
                    if category in results[timestep][ID]:
                        row.append(results[timestep][ID][category])
                    else:
                        row.append(0)

        csv_writer.writerow(row)

    out_file.close()


if __name__ == '__main__':
    sys.exit(main())