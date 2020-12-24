# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/voxceleb/speech_features_extraction.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 2642 bytes
from __future__ import print_function, division, absolute_import
import matplotlib
matplotlib.use('Agg')
import os
os.environ['ODIN'] = 'float32,gpu'
import numpy as np
from odin import backend as K, nnet as N, visual as V
from odin import preprocessing as pp
from odin.utils import args_parse, stdio, get_module_from_path, get_script_path
from odin.utils.mpi import cpu_count
from utils import WAV_FILES, SAMPLED_WAV_FILE, PATH_ACOUSTIC_FEAT, PATH_EXP
stdio(os.path.join(PATH_EXP, 'features_extraction.log'))
args = args_parse(descriptions=[
 ('recipe', 'the name of function defined in feature_recipes.py', None),
 ('--debug', 'enable debug or not', None, False)])
DEBUG = args.debug
extractor = get_module_from_path(identifier=(str(args.recipe)), prefix='feature_recipes',
  path=(get_script_path()))
assert len(extractor) > 0, "Cannot find any recipe with name: '%s' from path: '%s'" % (args.recipe, get_script_path())
recipe = extractor[0](DEBUG)
if DEBUG:
    with np.warnings.catch_warnings():
        np.warnings.filterwarnings('ignore')
        for path, name in SAMPLED_WAV_FILE:
            feat = recipe.transform(path)
            assert feat['bnf'].shape[0] == feat['mspec'].shape[0]
            V.plot_multiple_features(feat, title=(feat['name']))

        V.plot_save(os.path.join(PATH_EXP, 'features_%s.pdf' % args.recipe))
        exit()
with np.warnings.catch_warnings():
    np.warnings.filterwarnings('ignore')
    jobs = list(WAV_FILES.keys())
    processor = pp.FeatureProcessor(jobs=jobs, path=(os.path.join(PATH_ACOUSTIC_FEAT, args.recipe)),
      extractor=recipe,
      n_cache=1200,
      ncpu=(min(18, cpu_count() - 2)),
      override=True,
      identifier='name',
      log_path=(os.path.join(PATH_EXP, 'processor_%s.log' % args.recipe)),
      stop_on_failure=False)
    processor.run()
    pp.validate_features(processor, nb_samples=12,
      path=(os.path.join(PATH_EXP, args.recipe)),
      override=True)