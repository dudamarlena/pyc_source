# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Exceptions.py
# Compiled at: 2015-06-30 06:52:38
"""
The System of Exceptions

@author: Assem Chelli
@contact: assem.ch [at] gmail.com
@license: AGPL

"""

class Ta7rif(Exception):
    """ raise when an error in Holy Quran text

    example:
    ========
        >>> raise Ta7rif(type="new",value=u"ابراهام",original="ابراهيم",aya_gid=0,msg="word changed")

    @param type:type of ta7rif
    @type type:string
    @param value:value of ta7rif
    @type value:unicode
    @param original:the original value
    @type original:unicode
    @param aya_gid:the general id of aya
    @type aya_gid:int
    @param msg:the message of error
    @type msg:unicode

    """

    def __init__(self, type='new', value='undefined', original=None, aya_gid=None, msg=''):
        self.type = type
        self.aya_gid = aya_gid
        self.value = value
        self.original = original
        self.msg = msg

    def __str__(self):
        return '\nTa7rif in Holy Quran :\n\tType:' + str(self.type) + '\n\tvalue:' + str(self.value) + '\n\toriginalvalue:' + str(self.original) + '\n\taya_gid:' + str(self.aya_gid) + '\n\n' + str(self.msg)


class NotImplementedYet(Exception):
    """raise when a methode is not implemented

    example:
    ========
        >>> raise NotImplementedYet(message="waiting a good stemmer",methode="derivation",developper="assem.ch@gmail.com",date="01/02/10")

    @param message:the message of error
    @type message:unicode

    """

    def __init__(self, message='', methode='undefined', developper='', date=''):
        self.methode = methode
        self.developper = developper
        self.message = message
        self.date = date

    def __str__(self):
        return '\nthis  :\n\tType:' + str(self.type) + '\n\tvalue:' + str(self.value) + '\n\toriginalvalue:' + str(self.original) + '\n\taya_gid:' + str(self.aya_gid) + '\n\n' + str(self.msg)


class FeedBack(Exception):
    """ declare an empty case in an index

    example:
    ========
        >>>

    """

    def __init__(self, table, value):
        self.table = table
        self.value = value

    def __str__(self):
        return '\n\ttable:' + self.table + '\n\tvalue:' + self.value