# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/toutf8/__init__.py
# Compiled at: 2016-07-20 11:58:40
# Size of source mod 2**32: 1535 bytes
import os, re, sys, shutil, chardet
des_enc = 'utf-8'

def trans_file(file_name):
    bk_file = file_name + '.bk'
    shutil.copy(file_name, bk_file)
    fin = open(bk_file, 'rb')
    succeed = True
    try:
        try:
            data = fin.read()
            guess = chardet.detect(data)
            if guess is None or guess['confidence'] < 0.618:
                raise Exception
            src_enc = guess['encoding']
            if src_enc == des_enc:
                raise Exception
            src_enc = 'GB18030' if src_enc in ('GB2312', 'GBK', 'ISO-8859-2', 'windows-1252') else src_enc
            padding = ' ' * max(60 - len(file_name), 0)
            print('%s:%s%s ==> %s' % (file_name, padding, src_enc, des_enc))
            data = data.decode(encoding=src_enc).encode(des_enc)
            fout = open(file_name, 'wb')
            fout.write(data)
            fout.close()
        except Exception as e:
            succeed = False

    finally:
        fin.close()
        os.remove(bk_file)
        return succeed


def main():
    nums = len(sys.argv)
    if nums not in (2, 3):
        print('Usage: toutf8 path [filename_pattern(in regular expression)]')
        exit()
    path = os.path.abspath(sys.argv[1])
    if os.path.isfile(path):
        trans_file(path)
    else:
        pattern = '.*' if nums == 2 else sys.argv[2]
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if re.search(pattern, filename) and filename != __file__:
                trans_file(os.path.join(dirpath, filename))