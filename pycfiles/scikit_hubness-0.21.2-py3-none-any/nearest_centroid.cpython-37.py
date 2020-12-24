# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/nearest_centroid.py
# Compiled at: 2019-10-30 06:53:24
# Size of source mod 2**32: 502 bytes
from sklearn.neighbors import NearestCentroid
__all__ = [
 'NearestCentroid']
nc_docs = NearestCentroid.__doc__
old_str = 'Read more in the :ref:`User Guide <nearest_centroid_classifier>`.'
new_str = 'Read more in the `scikit-learn User Guide <https://scikit-learn.org/stable/modules/neighbors.html#nearest-centroid-classifier>`_.'
nc_docs_new = nc_docs.replace(old_str, new_str, 1)
NearestCentroid.__doc__ = nc_docs_new