# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: modules/colour.py
# Compiled at: 2019-07-19 05:01:50
C_START_GREEN = '\x1b[92m'
C_START_RED = '\x1b[91m'
C_START_ORANGE = '\x1b[93m'
C_START_VIOLET = '\x1b[95m'
C_START_BLUE = '\x1b[94m'
C_START_GREY = '\x1b[90m'
C_END = '\x1b[0m'

def get_single_str(list_):
    list_of_strs = []
    for elem in list_:
        list_of_strs.append(str(elem))

    return (' ').join(list_of_strs)


def print_success(*strs):
    global C_END
    global C_START_GREEN
    print C_START_GREEN + get_single_str(strs) + C_END


def print_err(*strs):
    global C_START_RED
    print C_START_RED + get_single_str(strs) + C_END


def print_warning(*strs):
    global C_START_ORANGE
    print C_START_ORANGE + get_single_str(strs) + C_END


def print_primary(*strs):
    global C_START_BLUE
    print C_START_BLUE + get_single_str(strs) + C_END


def print_secondary(*strs):
    global C_START_VIOLET
    print C_START_VIOLET + get_single_str(strs) + C_END


def print_muted(*strs):
    global C_START_GREY
    print C_START_GREY + get_single_str(strs) + C_END