# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/interface/jupyter.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 478 bytes
from IPython.core.display import display, HTML
from ..isa import ISAMagic
from ..ml import MLMagic
from .generic import Generic

class Jupyter(Generic):

    def __init__(self, *args, **kargs):
        (super().__init__)(*args, **kargs)

    def show(self, dataframe, limit=100):
        display(HTML(dataframe.limit(limit).toPandas().to_html()))

    def command_aux(self, ISAContext):
        ISAMagic(ISAContext)

    def command_ml(self, MLContext):
        MLMagic(MLContext)