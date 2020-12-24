# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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