# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/base_engine.py
# Compiled at: 2019-06-25 06:05:00
# Size of source mod 2**32: 462 bytes


class Engines:
    __doc__ = "\n    Engines base class containing core information that all other engines (PSI4, Gaussian etc) will have.\n    Provides atoms' coordinates with name tags for each atom and entire molecule.\n    Also gives all configs from the appropriate config file.\n    "

    def __init__(self, molecule):
        self.molecule = molecule

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__!r})"