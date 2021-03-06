# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/nist_sre/speech_augmentation.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 5385 bytes
from __future__ import print_function, division, absolute_import
import matplotlib
matplotlib.use('Agg')
import os, numpy as np
from odin import preprocessing as pp
from odin import fuel as F, visual as V
from odin.utils import ctext, get_logpath, get_module_from_path, get_script_path, Progbar, mpi, catch_warnings_ignore
from helpers import ALL_FILES, ALL_NOISE, ALL_DATASET, IS_DEBUGGING, PATH_ACOUSTIC_FEATURES, FEATURE_RECIPE, AUGMENTATION_NAME, Config, EXP_DIR, NCPU, validate_features_dataset
if AUGMENTATION_NAME == 'None':
    raise ValueError("`-aug` option was not provided, choose: 'rirs' or 'musan'")
else:
    np.random.seed(Config.SUPER_SEED)
    PERCENTAGE_AUGMENTATION = 0.8
    AUGMENTATION_DATASET = [
     'swb', 'sre04', 'sre05', 'sre06', 'sre08', 'sre10']
    AUGMENTATION_DATASET = [i for i in AUGMENTATION_DATASET if i in ALL_DATASET]
    print('Augmenting following dataset: %s' % ctext(', '.join(AUGMENTATION_DATASET), 'yellow'))
    path = os.path.join(PATH_ACOUSTIC_FEATURES, FEATURE_RECIPE)
    assert os.path.exists(path), 'Acoustic feature must be extracted first, and stored at path: %s' % path
    ds = F.Dataset(path, read_only=True)
    all_duration = dict(ds['duration'].items())
    ds.close()
    AUG_FILES = []
    missing_duration = []
    for row in ALL_FILES:
        if row[4] not in AUGMENTATION_DATASET:
            continue
        if row[2] not in all_duration:
            missing_duration.append(row)
            continue
        dur = all_duration[row[2]]
        AUG_FILES.append([i for i in row] + [dur])

    print('#Files missing duration:', ctext(len(missing_duration), 'cyan'))
    assert len(AUG_FILES), 'Cannot find any files for augmentation'
    AUG_FILES = np.array(AUG_FILES)
    org_shape = AUG_FILES.shape
    np.random.shuffle(AUG_FILES)
    np.random.shuffle(AUG_FILES)
    AUG_FILES = AUG_FILES[:int(len(AUG_FILES) * PERCENTAGE_AUGMENTATION)]
    sel_shape = AUG_FILES.shape
    print('#Augmentation Files:')
    print('  Found    :', ctext(org_shape, 'cyan'))
    print('  Selected :', ctext(sel_shape, 'cyan'))
    recipe = get_module_from_path(identifier=FEATURE_RECIPE, path=(get_script_path()),
      prefix='feature_recipes')
    assert len(recipe) > 0, 'Cannot find recipe with name: %s' % recipe
recipe = recipe[0](augmentation=AUGMENTATION_NAME)
if IS_DEBUGGING:
    with catch_warnings_ignore(Warning):
        n_samples = 120
        prog = Progbar(target=n_samples, print_summary=True, name='Debugging Augmentation')
        for feat in mpi.MPI(jobs=(AUG_FILES[:n_samples]), func=(recipe.transform),
          ncpu=NCPU,
          batch=1):
            if np.random.rand() > 0.8:
                feat = {i:j[:1200] if isinstance(j, np.ndarray) else j for i, j in feat.items()}
                V.plot_multiple_features(feat, fig_width=20, title=(feat['name']))
            prog['name'] = feat['name'][:48]
            prog['dsname'] = feat['dsname']
            prog['dsnoise'] = feat['dsnoise']
            prog.add(1)

        V.plot_save(os.path.join(EXP_DIR, 'debug_%s_%s.pdf' % (
         FEATURE_RECIPE, AUGMENTATION_NAME)))
        pp.set_extractor_debug(recipe, debug=True)
        recipe.transform(AUG_FILES[0])
        with open(os.path.join(EXP_DIR, 'debug_%s_%s.log' % (
         FEATURE_RECIPE, AUGMENTATION_NAME)), 'w') as (f):
            for name, step in recipe.steps:
                f.write(step.last_debugging_text)

    exit()
output_dataset_path = os.path.join(PATH_ACOUSTIC_FEATURES, '%s_%s' % (FEATURE_RECIPE, AUGMENTATION_NAME))
processor_log_path = os.path.join(EXP_DIR, 'processor_%s_%s.log' % (FEATURE_RECIPE, AUGMENTATION_NAME))
ds_validation_path = os.path.join(EXP_DIR, 'validate_%s_%s.pdf' % (FEATURE_RECIPE, AUGMENTATION_NAME))
with catch_warnings_ignore(Warning):
    processor = pp.FeatureProcessor(jobs=AUG_FILES,
      path=output_dataset_path,
      extractor=recipe,
      n_cache=320,
      ncpu=NCPU,
      override=True,
      identifier='name',
      log_path=processor_log_path,
      stop_on_failure=False)
    processor.run()
validate_features_dataset(output_dataset_path, ds_validation_path)