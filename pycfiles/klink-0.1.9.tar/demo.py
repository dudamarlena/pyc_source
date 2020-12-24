# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/dev/python/klink/klink/demo.py
# Compiled at: 2015-06-15 09:41:19


class TestClass(object):
    """
    This is a test class. Used for demo purposes.

    Lorem ipsum dolor sit amet, cu vero viris mollis his. Ex est
    iusto constituam. Id eam graeci iuvaret facilis, erant dicunt in
    quo, te iudico periculis interpretaris sed. Audire tibique te pro,
    equidem repudiare an vim. Nostrum placerat liberavisse ne eam.
    Zril corpora expetenda ex mea, at wisi vitae vocibus vix.

    .. note::

        Does not actually do anything. Just for demo.

    Args:
        name (str): Name arg
        age (int): Age arg

   """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def method1(self, arg1, arg2):
        """
        Does stuff with args.

        Demo method1 - this method does stuff. Interesting right?

        Args:
            arg1 (type): The first arg needed to do stuff.
            arg2 (type): The second arg needed to do stuff.

        Returns:
            str - stuff string

        """
        pass