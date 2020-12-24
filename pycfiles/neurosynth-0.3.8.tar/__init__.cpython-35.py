# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/__init__.py
# Compiled at: 2015-12-24 08:33:07
# Size of source mod 2**32: 1551 bytes
"""NeuroSynth -- large-scale synthesis of functional neuroimaging data.

"""
__all__ = [
 'analysis', 'base', 'set_logging_level', '__version__']
from .base.dataset import Dataset
from .base.mask import Masker
from .analysis.cluster import Clusterable
from .analysis.meta import MetaAnalysis
from .analysis.decode import Decoder
from .base import dataset, imageutils, lexparser, mask, transformations
from .analysis import classify, cluster, decode, meta, network, reduce
import logging, sys, os
from .version import __version__
logger = logging.getLogger('neurosynth')

def set_logging_level(level=None):
    """Set neurosynth's logging level

    Args
      level : str
        Name of the logging level (warning, error, info, etc) known
        to logging module.  If no level provided, it would get that one
        from environment variable NEUROSYNTH_LOGLEVEL
    """
    if level is None:
        level = os.environ.get('NEUROSYNTH_LOGLEVEL', 'warn')
    if level is not None:
        logger.setLevel(getattr(logging, level.upper()))
    return logger.getEffectiveLevel()


def _setup_logger(logger):
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter('%(levelname)-6s %(module)-7s %(message)s'))
    logger.addHandler(console)
    set_logging_level()


_setup_logger(logger)