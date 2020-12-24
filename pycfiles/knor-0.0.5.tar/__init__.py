# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: knor/__init__.py
# Compiled at: 2019-05-30 02:56:55
import sys
PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 2:
    from knor import Kmeans
    from knor import KmeansPP
    from knor import SKmeans
    from knor import FuzzyCMeans
    from knor import Kmedoids
    from knor import Hmeans
    from knor import Xmeans
    from knor import Gmeans
    from knor import cluster_t
else:
    from .knor import Kmeans
    from .knor import KmeansPP
    from .knor import SKmeans
    from .knor import FuzzyCMeans
    from .knor import Kmedoids
    from .knor import Hmeans
    from .knor import Xmeans
    from .knor import Gmeans
    from .knor import cluster_t