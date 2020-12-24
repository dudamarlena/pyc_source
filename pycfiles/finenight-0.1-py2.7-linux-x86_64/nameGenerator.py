# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/nameGenerator.py
# Compiled at: 2014-08-29 00:09:34


class IndexNameGenerator:
    """Renaming states with this class is not stable, that is,
    it's not sure that renaming the FSA will give allways the
    same result.
    """

    def __init__(self):
        self.index = 0

    def generate(self):
        name = 'q' + str(self.index)
        self.index += 1
        return name


class PlainIndexNameGenerator:
    """Renaming states with this class is not stable, that is,
    it's not sure that renaming the FSA will give allways the
    same result.
    """

    def __init__(self):
        self.index = 0

    def generate(self):
        name = str(self.index)
        self.index += 1
        return name