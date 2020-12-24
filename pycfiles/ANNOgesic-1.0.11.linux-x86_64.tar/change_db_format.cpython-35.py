# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/change_db_format.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 549 bytes


def change_format(input_file, output_file):
    """change the format of sRNA database"""
    num = 1
    out = open(output_file, 'w')
    with open(input_file) as (f_h):
        for line in f_h:
            line = line.strip()
            if line.startswith('>'):
                datas = line.split('|')
                if datas[0][1:] == 'NA':
                    datas[0] = '>srn_' + str(num)
                    num += 1
                out.write('|'.join(datas[:3]) + '\n')
            else:
                out.write(line + '\n')

    out.close()