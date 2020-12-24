# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-aarch64/egg/deepstacks/fields.py
# Compiled at: 2017-07-18 07:11:16


def fields(a):
    res = ()
    count = 0
    for line in a:
        print count, line
        if type(line[(-1)]) == set or type(line[(-1)]) == dict:
            pass
        else:
            line = line + ({},)
        while len(line) < 7:
            line = line[:-1] + (0, line[(-1)])

        flags = {}
        for k in line[(-1)]:
            flags[k] = line[(-1)][k]

        if line[1]:
            if type(line[1]) == tuple:
                flags['reshape'] = line[1]
            elif type(line[1]) == slice:
                flags['slice'] = line[1]
            else:
                flags['num_filters'] = line[1]
        if line[2]:
            flags['filter_size'] = line[2]
        if line[3]:
            flags['stride'] = line[3]
        if line[4]:
            flags['push'] = line[4]
        if line[5]:
            flags['sharegroup'] = line[5]
        res += (
         (
          line[0], flags),)
        print count, res[(-1)]
        count += 1

    return res