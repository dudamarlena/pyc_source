# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgsilva/Astrophysics/Packages/ACTIN/actin/actin.py
# Compiled at: 2019-07-08 17:09:37
# Size of source mod 2**32: 12264 bytes
from __future__ import print_function
from __future__ import division
import sys, os, glob, time, datetime, numpy as np
import astropy.io.fits as pyfits
import argparse, pkg_resources, appdirs
path = os.path.dirname(os.path.realpath(__file__))
actin_files_dir = os.path.join(path, 'actin_files')
sys.path.append(actin_files_dir)
import ac_settings as ac_set, ac_config, ac_read_data, ac_get_win, ac_calc_ind, ac_save, ac_plot_time as ac_plot, ac_tools
from matplotlib import pylab as plt
ac_set.init()
config_file = os.path.join(path, 'config_lines.txt')
version_file = os.path.join(path, 'VERSION')
version = ac_set.preamble(version_file)

def actin_file(file, calc_index=None, rv_in=None, config_file=config_file, save_output=False, ln_plts=False, obj_name=None, targ_list=None, del_out=False, frac=True):
    """
    Runs ACTIN for one fits file.
    Accepts files of types: 'S2D', 'S1D', 'e2ds', 's1d', 's1d_*_rv', 'ADP', and 'rdb'.
    Recognizes fits files from HARPS, HARPS-N and ESPRESSO instruments.
    """
    print()
    print('--------------------')
    print('EXECUTING ACTIN_FILE')
    print('--------------------')
    if type(file) is list:
        file = file[0]
    tel, instr = ac_tools.get_instr(file)
    if instr == False:
        pass
    else:
        if instr in ac_set.instr:
            pass
        else:
            msg = "*** ERROR:\nUnrecognized instrument. ACTIN only accepts HARPS, HARPS-N or ESPRESSO. To read from a different instrument convert data to rdb file with the headers: 'obj', 'obs_date', 'bjd', 'wave', 'flux', 'error_pixel' (optional)."
            sys.exit(msg)
        if targ_list:
            check = ac_tools.check_targ(file, targets=targ_list)
            if check is True:
                pass
            elif check is False:
                return
        if calc_index:
            sel_lines = ac_config.read_conf(config_file, calc_index)
        else:
            data = ac_read_data.read_data(file, rv_in=rv_in, obj_name=obj_name)
            if not data:
                return
            if save_output is not False:
                if data['file_type'] != 'rdb':
                    dupl = ac_save.check_duplicate(data['obj'], data['obs_date'], data['instr'], data['file_type'], save_output)
                    if dupl is True:
                        return
                else:
                    if calc_index:
                        test = ac_calc_ind.check_lines(data['wave'], sel_lines)
                        if not test:
                            print('*** ACTION: Ignoring measurement.')
                            return
                        sel_lines = ac_calc_ind.calc_flux_lines(data, sel_lines, ln_plts=ln_plts, frac=frac)
                        index = ac_calc_ind.calc_ind(sel_lines)
                    index = calc_index or None
                    sel_lines = None
                if save_output is not False:
                    rdb_file = ac_save.save_data(data, index, out_dir=save_output)
            else:
                rdb_file = None
        info = {}
        info['config_file'] = config_file
        info['file_type'] = data['file_type']
        info['version'] = version
        info['source_path'] = os.path.split(file)[0]
        info['tel'] = data['tel']
        info['instr'] = data['instr']
        info['obj'] = data['obj']
        options = {}
        options['frac'] = frac
        output = {}
        output['data'] = data
        output['index'] = index
        output['sel_lines'] = sel_lines
        output['info'] = info
        output['options'] = options
        output['rdb_file'] = rdb_file
        return output


def actin(files, calc_index=None, rv_in=None, config_file=None, save_output=False, ln_plts=False, obj_name=None, targ_list=None, del_out=False, frac=True, test=False, save_plots=False):
    """
    Runs 'actin_file' function for one or multiple fits files, for one or multiple stars.
    Accepts fits files from HARPS, HARPS-N, and ESPRESSO instruments.
    Accepts files of types: 'S1D', 'S2D', 'e2ds', 's1d', 's1d_*_rv', 'ADP', and 'rdb'.
    """
    print()
    print('----------------')
    print(' STARTING ACTIN ')
    print('----------------')
    start_time = time.time()
    if config_file is None:
        cfg_file = get_config()
    else:
        cfg_file = config_file
    print()
    print('Using spectral lines from configuration file:')
    print(cfg_file)
    if test:
        calc_index, files = ac_tools.test_actin(test, path, calc_index)
    if not files:
        sys.exit()
    if isinstance(files, str):
        files = [
         files]
    if rv_in is None:
        rv_in = [
         rv_in] * len(files)
    else:
        if type(rv_in) is not list:
            rv_in = [
             float(rv_in)]
        else:
            ac_tools.check_files(files)
            if del_out:
                print()
                print('Executing ac_tools.remove_output:')
                print('Searching output files to delete...')
                if obj_name:
                    for f in files:
                        _, instr = ac_tools.get_instr(f)
                        file_type = ac_tools.get_file_type(f)
                        if isinstance(obj_name, str):
                            star_name = obj_name
                            ac_tools.remove_output2(star_name, instr, file_type, save_output)
                        else:
                            if isinstance(obj_name, (list, np.ndarray)):
                                for star_name in obj_name:
                                    ac_tools.remove_output2(star_name, instr, file_type, save_output)

                else:
                    if not obj_name:
                        for f in files:
                            star_name = ac_tools.get_target(f)
                            _, instr = ac_tools.get_instr(f)
                            file_type = ac_tools.get_file_type(f)
                            ac_tools.remove_output2(star_name, instr, file_type, save_output)

            if ln_plts == 'same':
                ln_plts = save_output
            total_files = len(files)
            files_list = ac_tools.files_by_star_and_ftype(files)
            n_files_t = 0
            for k in range(len(files_list)):
                for i in range(len(files_list[k])):
                    n_files = 0
                    for j in range(len(files_list[k][i])):
                        n_files += 1
                        n_files_t += 1
                        output = actin_file((files_list[k][i][j]), calc_index,
                          rv_in=(rv_in[j]),
                          config_file=cfg_file,
                          save_output=save_output,
                          ln_plts=ln_plts,
                          obj_name=obj_name,
                          targ_list=targ_list,
                          del_out=del_out,
                          frac=frac)

                    if output:
                        sel_lines = output['sel_lines']
                        info = output['info']
                        options = output['options']
                        rdb_file = output['rdb_file']
                        ac_save.save_log(info, options, n_files, out_dir=save_output)
                        ac_save.save_line_info(info, sel_lines, out_dir=save_output)
                        if save_plots:
                            ac_plot.plt_time(info, out_dir=save_output, rmv_flgs=False, save_plt=True)
                            ac_plot.plt_time_mlty(info, out_dir=save_output, rmv_flgs=False, save_plt=True, hdrs=calc_index)

            if n_files_t != total_files:
                print()
                print('*** ERROR: Number of ACTIN calls different than number of files.')
                print('n_files_t:', n_files_t)
                print('total_files:', total_files)
            elapsed_time = (time.time() - start_time) / 60
            print('\n---------------------------------')
            print('Fractional pixels:\t{}'.format(frac))
            print('Files analysed:\t\t{}'.format(total_files))
            print('Save output:\t\t{}'.format(save_output))
            print('Elapsed time:\t\t{:.4f} min'.format(elapsed_time))


def get_config():
    """
    Check for existence of ACTIN folder and config file and creates them if not present. Returns the path to the config file.
    """
    cfg_dir = appdirs.user_config_dir('ACTIN')
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)
    cfg_file = os.path.join(cfg_dir, 'config_lines.txt')
    if not os.path.isfile(cfg_file):
        create_user_config(cfg_file)
    return cfg_file


def create_user_config(cfg_file):
    """
    Create the user's config file
    """
    from shutil import copyfile
    src = pkg_resources.resource_stream(__name__, 'config_lines.txt')
    copyfile(src.name, cfg_file)


def main():
    """
    Main function, call actin function with arguments from terminal.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', '-f', help='Read file(s)', nargs='+')
    parser.add_argument('--calc_index', '-i', help="Index id to calculate as designated by 'ind_id' in config_index.txt.", nargs='+', default=None)
    parser.add_argument('--rv_in', '-rv', help='RV value to calibrate wavelength. If False (default) try to read RV from CCF file.', nargs='+', default=None, type=float)
    parser.add_argument('--config_file', '-cf', help='Path to config_file, or False (default) read config file from standard directory.', default=None)
    parser.add_argument('--save_output', '-s', help='Path to output directory of data table, or False (default).', default=False)
    parser.add_argument('--ln_plts', '-lp', help="Path to directory to save line plots. If 'same' saves line plots to same directory of data output. If 'show' only shows the plots. If 'False' (default) does not save or show line plots", default=False)
    parser.add_argument('--obj_name', '-obj', help='Give target a name that overides the one from the fits files.', default=None)
    parser.add_argument('--targ_list', '-tl', help='Give a list of stars to select from fits files.', nargs='+', default=None)
    parser.add_argument('--del_out', '-del', help='Delete output data file if True.', default=False, type=(lambda x: str(x).lower() == 'true'))
    parser.add_argument('--test', '-t', help='Tests actin using the provided fits files in the "test_files" directory. Options are "e2ds", "s1d", and "adp"', default=False)
    parser.add_argument('--frac', '-frc', help='Turns fractional pixel on (True, default) or off (False).', default=True, type=(lambda x: str(x).lower() == 'true'))
    parser.add_argument('--save_plots', '-sp', help="If True saves time-series and multi-plots to same directory as 'save_output'.", default=False, type=(lambda x: str(x).lower() == 'true'))
    args = parser.parse_args()
    actin(files=(args.files), calc_index=(args.calc_index),
      rv_in=(args.rv_in),
      config_file=(args.config_file),
      save_output=(args.save_output),
      ln_plts=(args.ln_plts),
      obj_name=(args.obj_name),
      targ_list=(args.targ_list),
      del_out=(args.del_out),
      test=(args.test),
      frac=(args.frac),
      save_plots=(args.save_plots))


if __name__ == '__main__':
    main()