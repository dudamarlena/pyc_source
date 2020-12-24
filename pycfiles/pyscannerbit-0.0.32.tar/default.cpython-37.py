# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmartine/pyscannerbit/tests/default.py
# Compiled at: 2020-03-04 01:47:30
# Size of source mod 2**32: 732 bytes
import import_yaml
template = '\nParameters:\n  python_model: None\n\nPriors:\n\nPrinter:\n\n  printer: hdf5\n  options:\n    output_file: "results.hdf5"\n    group: "/python"\n    delete_file_on_restart: true\n\nScanner:\n\n  use_scanner: None\n\n  scanners:\n\n    de:\n      plugin: diver\n      like: LogLike\n      NP: 1000\n\n    multinest:\n      plugin: multinest\n      like:  LogLike\n      nlive: 1000\n      tol: 0.1\n\n    mcmc:\n      plugin: great\n      like: LogLike\n      nTrialLists: 5\n      nTrials: 10000\n\n    twalk:\n      plugin: twalk\n\nLogger:\n  redirection:\n    [Default]      : "default.log"\n    [Scanner]      : "Scanner.log"\n\nKeyValues:\n  likelihood:\n    model_invalid_for_lnlike_below: -1e6\n'
settings = import_yaml.load(template)