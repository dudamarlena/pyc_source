# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/asterisk_dialplan/util.py
# Compiled at: 2015-03-13 22:04:52


def common_start(first_number, last_number):
    """ Get the common starting characters of the two strings first_number and last_number """
    str_first = str(first_number)
    str_last = str(last_number)
    common = ''
    for a, b in zip(list(str_first), list(str_last)):
        if a == b:
            common = common + a
        else:
            return common

    return


def test_block_for_coverage(patterns, first_number, last_number):
    """ Helper function to allow testing for contiguous coverage of a block of numbers with a given set of patterns """
    patternList = []
    for pattern in patterns:
        pattern = re.sub('X', '\\d', pattern)
        pattern = re.sub('Z', '[1-9]', pattern)
        pattern = re.sub('N', '[2-9]', pattern)
        pattern = re.sub('^_', '', pattern)
        patternList.append(pattern)

    pre = re.compile('^(' + ('|').join(patternList) + ')$')
    for x in range(int(first_number), int(last_number) + 1):
        result = pre.match(str(x))
        if result is None:
            return False

    return True