# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/tidigits/tidigits_preprocessor.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 8359 bytes
from __future__ import print_function, division, absolute_import
import matplotlib
matplotlib.use('Agg')
import os
os.environ['ODIN'] = 'cpu=1,float32'
import shutil, numpy as np
from odin import fuel as F, nnet as N
from odin import preprocessing as pp
from odin.utils import get_all_files, get_all_ext, exec_commands, MPI, cpu_count, Progbar, ArgController, stdio, ctext, crypto
args = ArgController().add('path', 'path to TIDIGITS dataset').add('--wav', 're-run Converting sphere file to wave', False).add('--ds', 're-run Group wave files into a dataset', False).add('--compress', 're-run compression of the dataset', False).parse()
TOTAL_FILES = 25096
README = '\nOriginal sample rate: 20,000 Hz\nDownsampled sample rate: 8,000 Hz\n\nSaved WAV file format:\n    * [train|test]\n    * [m|w|b|g] (alias for man, women, boy, girl)\n    * [age]\n    * [dialectID]\n    * [speakerID]\n    * [production]\n    * [digit_sequence]\n    => "train_g_08_17_as_a_4291815"\n\n    train material, child "g"irl, age is "08", dialect group is "17",\n    speaker code "as", "a" is first production,\n    digit sequence "4-2-9-1-8-1-5".\n--------------------\nCategory       Symbol    Number    Age Range (years)\n  Man            M        111           21 - 70\n  Woman          W        114           17 - 59\n  Boy            B         50            6 - 14\n  Girl           G         51            8 - 15\n\nEleven digits were used:  "zero", "one", "two", ... , "nine", and "oh".\n\nDigits for each speaker:\n    22 isolated digits (two tokens of each of the eleven digits)\n    11 two-digit sequences\n    11 three-digit sequences\n    11 four-digit sequences\n    11 five-digit sequences\n    11 seven-digit sequences\n\nExample of original data:\n     => "/data/adults/train/man/fd/6z97za.wav"\n     training material, adult male, speaker code "fd",\n     digit sequence "six zero nine seven zero", "a" is first production.\n\n     => "/data/adults/test/woman/pf/1b.wav"\n     test material, adult female, speaker code "pf",\n     digit sequence "one", "b" is second production.\n------------------\n    City                      Dialect             M    W    B    G\n\n01 Boston, MA            Eastern New England      5    5    0    1\n02 Richmond, VA          Virginia Piedmont        5    5    2    4\n03 Lubbock, TX           Southwest                5    5    0    1\n04 Los Angeles, CA       Southern California      5    5    0    1\n05 Knoxville, TN         South Midland            5    5    0    0\n06 Rochester, NY         Central New York         6    6    0    0\n07 Denver, CO            Rocky Mountains          5    5    0    0\n08 Milwaukee, WS         North Central            5    5    2    0\n09 Philadelphia, PA      Delaware Valley          5    6    0    1\n10 Kansas City, KS       Midland                  5    5    4    1\n11 Chicago, IL           North Central            5    5    1    2\n12 Charleston, SC        South Carolina           5    5    1    0\n13 New Orleans, LA       Gulf South               5    5    2    0\n14 Dayton, OH            South Midland            5    5    0    0\n15 Atlanta, GA           Gulf South               5    5    0    1\n16 Miami, FL             Spanish American         5    5    1    0\n17 Dallas, TX            Southwest                5    5   34   36\n18 New York, NY          New York City            5    5    2    2\n19 Little Rock, AR       South Midland            5    6    0    0\n20 Portland, OR          Pacific Northwest        5    5    0    0\n21 Pittsburgh, PA        Upper Ohio Valley        5    5    0    0\n22                       Black                    5    6    1    1\n\n                         Total Speakers         111  114   50   51    326\n'
inpath = args.path
outpath = '/home/trung/data/TIDIGITS_wav'
compress_path = '/home/trung/data/TIDIGITS.zip'
wav_path = os.path.join(inpath, 'wave')
infopath = os.path.join(inpath, 'data/children/doc/spkrinfo.txt')
logpath = os.path.join(inpath, 'log.txt')
print('Input path:       ', ctext(inpath, 'cyan'))
print('Output path:      ', ctext(outpath, 'cyan'))
print('Convert to WAV at:', ctext(wav_path, 'cyan'))
print('Log path:         ', ctext(logpath, 'cyan'))
stdio(logpath)
exts = get_all_ext(inpath)
audio_files = get_all_files(inpath, filter_func=(lambda f: f[-4:] == '.wav' and f.split('/')[(-3)] in ('girl', 'boy', 'man', 'woman')))
info = np.genfromtxt(infopath, dtype=str, skip_header=12)
info = {ID.lower():(Gender.lower(), Age, Dialect, Usage) for ID, Gender, Age, Dialect, Usage in info}
gender_map = {'man':'m', 
 'woman':'w', 
 'boy':'b', 
 'girl':'g'}
usage_map = {'TST':'test', 
 'TRN':'train'}

def get_name(path):
    usage, gender, ID, digits = path.split('/')[-4:]
    production = digits[(-5)]
    digits = digits[:-5]
    gender = gender_map[gender]
    gender_, age_, dialect_, usage_ = info[ID]
    usage_ = usage_map[usage_]
    assert usage == usage_ and gender == gender_, path
    name = '%s_%s_%s_%s_%s_%s_%s.wav' % (
     usage, gender, age_, dialect_, ID, production, digits)
    return name


if os.path.exists(wav_path):
    if args.wav:
        print("Override wave files at '%s'" % wav_path)
        shutil.rmtree(wav_path)
    elif len(os.listdir(wav_path)) != TOTAL_FILES:
        print("Found only %d files at '%s', delete old wave files" % (
         len(os.listdir(wav_path)), wav_path))
        shutil.rmtree(wav_path)
else:
    if not os.path.exists(wav_path):
        os.mkdir(wav_path)
        cmds = ['sph2pipe %s %s -f rif' % (path, os.path.join(wav_path, get_name(path))) for path in audio_files]

        def mpi_fn(cmd):
            exec_commands(cmd, print_progress=False)
            yield len(cmd)


        prog = Progbar(target=(len(cmds)), print_report=True,
          print_summary=True,
          name='Converting .sph to .wav')
        mpi = MPI(jobs=cmds, func=mpi_fn, ncpu=(cpu_count() - 1),
          batch=12)
        for i in mpi:
            prog.add(i)

    jobs = get_all_files(wav_path, filter_func=(lambda x: '.wav' == x[-4:]))
    assert len(jobs) == TOTAL_FILES
if not os.path.exists(outpath) or args.ds:
    extractors = pp.make_pipeline(steps=[
     pp.speech.AudioReader(sr=None, sr_new=8000, best_resample=True, remove_dc=True),
     pp.base.Converter(converter=(lambda x: os.path.basename(x).split('.')[0]), input_name='path',
       output_name='name'),
     pp.base.AsType(dtype='float16', input_name='raw')],
      debug=False)
    processor = pp.FeatureProcessor(jobs=jobs, path=outpath, extractor=extractors, n_cache=0.08,
      ncpu=None,
      override=True)
    processor.run()
    pp.validate_features(processor, path='/tmp/tidigits', nb_samples=12, override=True)
    with open(os.path.join(outpath, 'README'), 'w') as (f):
        f.write(README)
ds = F.Dataset(outpath, read_only=True)
print(ds)
print(ctext(ds.md5, 'yellow'))
ds.close()
if not os.path.exists(compress_path) or args.compress:
    if os.path.exists(compress_path):
        os.remove(compress_path)
    crypto.zip_aes(in_path=outpath, out_path=compress_path, verbose=True)
print('Log at path:', ctext(logpath, 'cyan'))