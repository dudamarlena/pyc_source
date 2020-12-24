# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\pyrolite\pyrolite\data\Aitchison\__init__.py
# Compiled at: 2020-01-10 04:16:12
# Size of source mod 2**32: 1431 bytes
"""
These data module provides small toy data sets are from [#ref_1]_. As some of these
compositions were not fully closed, each has been renormalised to 100% over the
parameters "A" to "E".

References
-----------
.. [#ref_1] Aitchison J. (1984) The statistical analysis of geochemical compositions.
       Journal of the International Association for Mathematical Geology 16, 531–564.
       doi: {aitchison1984}
"""
import pandas as pd, logging
from ...util.meta import pyrolite_datafolder, sphinx_doi_link
from ...util.text import titlecase
from ...comp.codata import renormalise
__doc__ = __doc__.format(aitchison1984=(sphinx_doi_link('10.1007/BF01029316')))
__doc__ = str(__doc__).replace('ref', __name__)
logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)
__folder__ = pyrolite_datafolder(subfolder='Aitchison')

def _load_frame(filename):
    path = __folder__ / filename
    df = pd.read_csv(path)
    df.loc[:, ['A', 'B', 'C', 'D', 'E']] = renormalise(df.loc[:, ['A', 'B', 'C', 'D', 'E']])
    df = df.set_index('Specimen')
    df.name = titlecase(path.stem)
    return df


def load_boxite():
    return _load_frame('boxite.csv')


def load_coxite():
    return _load_frame('coxite.csv')


def load_hongite():
    return _load_frame('hongite.csv')


def load_kongite():
    return _load_frame('kongite.csv')