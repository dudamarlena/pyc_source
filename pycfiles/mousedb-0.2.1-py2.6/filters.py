# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/filters.py
# Compiled at: 2010-06-14 19:51:42
from mousedb.animal.models import Animal
from filter import *

class AnimalFilter(FilterSet):

    class Meta:
        model = Animal
        fields = ['Strain', 'Background', 'Genotype', 'Gender', 'Alive']