# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/kde.py
# Compiled at: 2019-10-30 06:53:24
# Size of source mod 2**32: 450 bytes
from sklearn.neighbors.kde import KernelDensity
__all__ = [
 'KernelDensity']
kde_docs = KernelDensity.__doc__
old_str = 'Read more in the :ref:`User Guide <kernel_density>`.'
new_str = 'Read more in the `scikit-learn User Guide <https://scikit-learn.org/stable/modules/density.html#kernel-density>`_.'
kde_docs_new = kde_docs.replace(old_str, new_str, 1)
KernelDensity.__doc__ = kde_docs_new