# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cili/util.py
# Compiled at: 2014-06-10 20:11:51
import os, sys
from multiprocessing import Pool, cpu_count
from time import sleep
import numpy as np
from models import *
ASC_SFIELDS_EYE = {'l': [
       (
        'onset', np.int64),
       (
        'x_l', np.float64),
       (
        'y_l', np.float64),
       (
        'pup_l', np.float64)], 
   'r': [
       (
        'onset', np.int64),
       (
        'x_r', np.float64),
       (
        'y_r', np.float64),
       (
        'pup_r', np.float64)], 
   'b': [
       (
        'onset', np.int64),
       (
        'x_l', np.float64),
       (
        'y_l', np.float64),
       (
        'pup_l', np.float64),
       (
        'x_r', np.float64),
       (
        'y_r', np.float64),
       (
        'pup_r', np.float64)]}
ASC_SFIELDS_VEL = {'l': [
       (
        'vel_x_l', np.float64),
       (
        'vel_y_l', np.float64)], 
   'r': [
       (
        'vel_x_r', np.float64),
       (
        'vel_y_r', np.float64)], 
   'b': [
       (
        'vel_x_l', np.float64),
       (
        'vel_y_l', np.float64),
       (
        'vel_x_r', np.float64),
       (
        'vel_y_r', np.float64)]}
ASC_SFIELDS_REZ = [
 (
  'res_x', np.float64),
 (
  'res_y', np.float64)]
ASC_SFIELDS_EXTRA = [('junk', object)]
ASC_SFIELDS_IGNORE = ['junk']
TXT_FIELDS = {'LEFT_ACCELLERATION_X': np.float64, 
   'LEFT_ACCELLERATION_Y': np.float64, 
   'LEFT_GAZE_X': np.float64, 
   'LEFT_GAZE_Y': np.float64, 
   'LEFT_IN_BLINK': np.int64, 
   'LEFT_IN_SACCADE': np.int64, 
   'LEFT_PUPIL_SIZE': np.float64, 
   'LEFT_VELOCITY_X': np.float64, 
   'LEFT_VELOCITY_Y': np.float64, 
   'RECORDING_SESSION_LABEL': object, 
   'RIGHT_ACCELLERATION_X': np.float64, 
   'RIGHT_ACCELLERATION_Y': np.float64, 
   'RIGHT_GAZE_X': np.float64, 
   'RIGHT_GAZE_Y': np.float64, 
   'RIGHT_IN_BLINK': np.int64, 
   'RIGHT_IN_SACCADE': np.int64, 
   'RIGHT_PUPIL_SIZE': np.float64, 
   'RIGHT_VELOCITY_X': np.float64, 
   'RIGHT_VELOCITY_Y': np.float64, 
   'TIMESTAMP': np.int64}
TXT_INT_TYPES = [np.int64]
TXT_NAME_MAP = [np.int64]
ASC_EV_LINE_STARTS = [
 'MSG',
 'START',
 'END',
 'EBLINK',
 'ESACC',
 'EFIX',
 'BUTTON',
 'SAMPLES']
ASC_EFIELDS_EVENT = {'MSG': [
         (
          'name', object),
         (
          'onset', np.int64),
         (
          'label', object),
         (
          'content', object)], 
   'START': [
           (
            'name', object),
           (
            'onset', np.int64),
           (
            'eye', object),
           (
            'types', object)], 
   'END': [
         (
          'name', object),
         (
          'onset', np.int64),
         (
          'types', object),
         (
          'x_res', np.float64),
         (
          'y_res', np.float64)], 
   'EBLINK': [
            (
             'name', object),
            (
             'eye', object),
            (
             'onset', np.int64),
            (
             'last_onset', np.int64),
            (
             'duration', np.int64)], 
   'ESACC': [
           (
            'name', object),
           (
            'eye', object),
           (
            'onset', np.int64),
           (
            'last_onset', np.int64),
           (
            'duration', np.int64),
           (
            'x_start', np.float64),
           (
            'y_start', np.float64),
           (
            'x_end', np.float64),
           (
            'y_end', np.float64),
           (
            'vis_angle', np.float64),
           (
            'peak_velocity', np.int64)], 
   'EFIX': [
          (
           'name', object),
          (
           'eye', object),
          (
           'onset', np.int64),
          (
           'last_onset', np.int64),
          (
           'duration', np.int64),
          (
           'x_pos', np.float64),
          (
           'y_pos', np.float64),
          (
           'p_size', np.int64)], 
   'BUTTON': [
            (
             'name', object),
            (
             'onset', np.int64),
            (
             'b_num', np.int64),
            (
             'state', np.int64)]}
ASC_EFIELDS_RES = {'MSG': [], 'START': [], 'END': [], 'EBLINK': [], 'ESACC': [
           (
            'x_res', np.float64),
           (
            'y_res', np.float64)], 
   'EFIX': [
          (
           'x_res', np.float64),
          (
           'y_res', np.float64)], 
   'BUTTON': []}
ASC_EV_IGNORE_COLUMNS = {'MSG': [], 'START': [], 'END': [], 'EBLINK': [], 'ESACC': [], 'EFIX': [], 'BUTTON': []}
ASC_IRREG_EVENTS = [
 'MSG', 'START', 'END']
ASC_INT_TYPES = [np.int64]
PUP_FIELDS = ['pup_r', 'pup_l', 'RIGHT_PUPIL_SIZE', 'LEFT_PUPIL_SIZE']

def load_eyelink_dataset(file_name):
    """ Parses eyelink data to return samples and events.

    For now, we can only parse events from .asc files. If you hand us a .txt,
    we'll parse out the samples, but not the events.

    Parameters
    ----------
    file_name (string)
        The .asc or .txt file you'd like to parse.

    Returns
    -------
    (Samples object, Events object (or None))
    """
    root, ext = os.path.splitext(file_name)
    if ext == '.asc':
        s, e = pandas_dfs_from_asc(file_name)
    elif ext in ('.txt', ):
        s = load_tdf(file_name)
        e = None
    else:
        raise ValueError('only .asc and .txt files supported at the moment...')
    return (s, e)


def pandas_df_from_txt(file_path):
    """ Parses samples out of an EyeLink .txt file """
    import pandas as pd, io
    df = pd.read_csv(file_path, sep='\t', index_col='TIMESTAMP', low_memory=False, na_values=['.'])
    fields = [ str(x) for x in df.dtypes.keys() ]
    dtypes = dict([ (d, object) for d in fields if d not in TXT_FIELDS.keys() ])
    dtypes.update(dict([ (k, v) for k, v in TXT_FIELDS.iteritems() if k in fields ]))
    nums = [ k for k, v in dtypes.iteritems() if v not in [object] ]
    ints = [ k for k in nums if dtypes[k] in TXT_INT_TYPES ]
    df[nums] = df[nums].convert_objects(convert_numeric=True)
    df[ints] = df[ints].astype(np.int64)
    fields = [ f.lower() for f in fields ]
    df.columns = fields
    df.index.name = 'onset'
    return Samples.from_pd_obj(df)


def pandas_dfs_from_asc(file_path):
    """ Parses samples and events out of an EyeLink .asc file """
    e_lines = dict([ (k, []) for k in ASC_EV_LINE_STARTS ])
    s_lines = []
    with open(file_path, 'r') as (f):
        for line in f:
            if len(line) == 0:
                continue
            if line[0].isdigit():
                s_lines.append(line)
                continue
            for k in ASC_EV_LINE_STARTS:
                if line.startswith(k):
                    e_lines[k].append(line)
                    break

    if not len(e_lines['SAMPLES']) > 0:
        raise ValueError('Could not find samples line in .asc file.')
    side, has_vel, has_res = info_from_asc_samples_line(e_lines['SAMPLES'][0])
    samp_dtypes = build_asc_samp_dtypes(side, has_vel, has_res)
    ev_names = [ k for k in ASC_EV_LINE_STARTS if k not in ('SAMPLES', ) ]
    ev_dtypes = dict([ (ev_name, build_asc_ev_dtypes(ev_name, side, has_vel, has_res)) for ev_name in ev_names ])
    samp_df = pandas_df_from_lines(s_lines, samp_dtypes, ASC_SFIELDS_IGNORE)
    for ev_name in ASC_IRREG_EVENTS:
        if ev_name not in e_lines:
            continue
        e_lines[ev_name] = prep_irreg_asc_event_lines(e_lines[ev_name], ev_name)

    ev_dfs = dict([ (ev_name, pandas_df_from_lines(e_lines[ev_name], ev_dtypes[ev_name], ASC_EV_IGNORE_COLUMNS[ev_name])) for ev_name in ev_names if len(e_lines[ev_name]) > 0
                  ])
    return (
     Samples.from_pd_obj(samp_df), Events.from_dict(ev_dfs))


def pandas_df_from_lines(csv_lines, dtypes, ignore):
    import pandas as pd, cStringIO
    c = cStringIO.StringIO(('').join(csv_lines))
    fields, dts = zip(*dtypes)
    df = pd.read_csv(c, delim_whitespace=True, index_col=[
     'onset'], low_memory=False, na_values=[
     '.'], names=fields, header=0, error_bad_lines=False, warn_bad_lines=False)
    nums = [ d[0] for d in dtypes if d[1] not in [object] and d[0] not in ('onset', ) ]
    ints = [ d[0] for d in dtypes if d[1] in ASC_INT_TYPES and d[0] not in ('onset', ) ]
    df[nums] = df[nums].convert_objects(convert_numeric=True)
    df[ints] = df[ints].astype(np.int64)
    for ig in ignore:
        del df[ig]

    return df


def prep_irreg_asc_event_lines(lines, ev_name):
    """ uses quotes to force annoying events into usable chunks
    use sparingly - not super fast right now
    """
    new_lines = []
    if ev_name == 'MSG':
        for line in lines:
            l = line.split()
            lab = l[2] if len(l) > 2 else '.'
            cont = (' ').join(l[3:]) if len(l) > 3 else '.'
            nl = '%s\t%s\t"%s"\t"%s"\n' % (l[0], l[1], lab, cont)
            new_lines.append(nl)

    elif ev_name == 'START':
        for line in lines:
            l = line.split()
            new_lines.append('%s\t%s\t%s\t"%s"\n' % (l[0], l[1], l[2], (', ').join(l[3:])))

    elif ev_name == 'END':
        for line in lines:
            l = line.split()
            types = (' ').join(l[2:-3]) if len(l) > 5 else '.'
            x_res = l[(-2)]
            y_res = l[(-1)]
            new_lines.append('%s\t%s\t"%s"\t%s\t%s\n' % (l[0], l[1], types, l[(-2)], l[(-1)]))

    else:
        new_lines = lines
    return new_lines


def build_asc_samp_dtypes(side, has_vel, has_res):
    dtypes = list(ASC_SFIELDS_EYE[side])
    if has_vel:
        dtypes.extend(ASC_SFIELDS_VEL[side])
    if has_res:
        dtypes.extend(ASC_SFIELDS_REZ)
    dtypes.extend(ASC_SFIELDS_EXTRA)
    return dtypes


def build_asc_ev_dtypes(ev_name, side, has_vel, has_res):
    dtypes = list(ASC_EFIELDS_EVENT.get(ev_name, []))
    if has_res:
        dtypes.extend(ASC_EFIELDS_RES.get(ev_name, []))
    if dtypes:
        return dtypes
    else:
        return


def info_from_asc_samples_line(line_txt):
    """ gets sample info from asc SAMPLE lines

    Parameters
    ----------
    line_txt (string)
        A single line from an EyeLink asc file.

    Returns
    -------
    side (str)
        'l', 'r', or 'b'
    has_velocity (bool)
        True if velocity information is included in samples
    has_resolution (bool)
        True is resolution information is included in samples
    """
    words = line_txt.split()
    has_velocity = 'VEL' in words
    has_resolution = 'RES' in words
    sample_side = 'b'
    if 'LEFT' in words and 'RIGHT' not in words:
        sample_side = 'l'
    elif 'RIGHT' in words and 'LEFT' not in words:
        sample_side = 'r'
    return (sample_side, has_velocity, has_resolution)


def percentile_bucket(vals, bucket_size=10, scale=1.0, shift=0.0):
    """ returns percentile scores for each value
    Parameters
    ----------
    bucket_size (float)
        The size of each bucket, in percentile points 0-100. Actual bucket
        cutoffs are calculated with numpy.arange(), so if 100 isn't divisible
        by bucket_size, your top bucket will be small.
    scale (float)
        All values will be multiplied by this number after bucketing.
    shift (float)
        All values will have this added to them after scaling.
    """
    from scipy.stats import scoreatpercentile as sp
    import numpy as np
    from bisect import bisect_left
    percs = np.concatenate([np.arange(bucket_size, 100, bucket_size), [100]])
    cuts = [ sp(vals, p) for p in percs ]
    new_list = np.array([ bisect_left(cuts, val) + 1 for val in vals ]) * scale + shift
    return new_list


def ensure_dir(dir_path, overwrite=False):
    from shutil import rmtree
    from os.path import isdir, exists
    from os import makedirs
    if exists(dir_path):
        if not isdir(dir_path):
            raise ValueError('%s is a file...' % dir_path)
        if overwrite:
            rmtree(dir_path)
    if not exists(dir_path):
        makedirs(dir_path)


def get_0_percentage(asc_path):
    from cili.util import pandas_dfs_from_asc
    import pandas as pd
    ds, _ = pandas_dfs_from_asc(asc_path)
    p_fields = [ f for f in ds.columns if f in PUP_FIELDS ]
    if len(p_fields) == 0:
        return 1.0
    return float(len(ds[(ds[p_fields[0]] == 0)])) / float(len(ds))


def list_run_corruption(asc_dir):
    from glob import glob
    from multiprocessing import Pool
    from time import sleep
    import os
    from pprint import pprint
    files = glob(os.path.join(asc_dir, '*.asc'))
    f_count = float(len(files))
    pool = Pool()
    result = pool.map_async(get_0_percentage, files)
    while not result.ready():
        sleep(0.5)
        perc = '\r(%d chunks remaining)...' % result._number_left
        sys.stdout.write(perc)
        sys.stdout.flush()

    file_checks = result.get()
    vals = {}
    for i, fn in enumerate(files):
        vals[os.path.basename(fn)] = file_checks[i]

    print '\nDropout by File:'
    pprint(vals)


help_message = '\nNo help at this time. Check the code.\n'

class Usage(Exception):

    def __init__(self, msg=help_message):
        self.msg = msg


def main(argv=None):
    import os, getopt
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'd:', ['dir', 'dropout'])
        except getopt.error as msg:
            raise Usage(msg='\n' + str(msg))

        drop_check = False
        asc_dir = None
        for option, value in opts:
            if option in ('-h', '--help'):
                raise Usage()
            if option in ('-d', '--dir'):
                asc_dir = os.path.abspath(value)
                if not os.path.exists(asc_dir):
                    raise Usage('Could not find directory %s' % asc_dir)
            if option in '--dropout':
                drop_check = True

        if drop_check and asc_dir:
            list_run_corruption(asc_dir)
            return
    except Usage as err:
        f_str = sys.argv[0].split('/')[(-1)] + ':'
        lfs = len(f_str)
        f_str = '%s\n%s\n%s\n' % ('-' * lfs, f_str, '-' * lfs)
        print >> sys.stderr, f_str + str(err.msg)
        print >> sys.stderr, '-------------------\nfor help use --help\n-------------------'
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())