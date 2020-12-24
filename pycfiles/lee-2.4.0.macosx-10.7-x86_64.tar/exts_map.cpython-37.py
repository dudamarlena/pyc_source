# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zk/anaconda3/lib/python3.7/site-packages/lee/exts_map.py
# Compiled at: 2020-02-11 23:07:02
# Size of source mod 2**32: 770 bytes
language_exts = {'python':[
  '#', 'py'], 
 'python3':[
  '#', 'py'], 
 'cpp':[
  '//', 'cpp', 'cc'], 
 'java':[
  '//', 'java'], 
 'golang':[
  '//', 'go'], 
 'go':[
  '//', 'go'], 
 'php':[
  '//', 'php'], 
 'javascript':[
  '//', 'js', 'ts'], 
 'js':[
  '//', 'js', 'ts']}

def ext2language(ext):
    for key, value in language_exts.items():
        if ext.lower() in value:
            return key

    raise Exception(f"can`t find file extension {ext} for language")


def language2extAndComemnt(language):
    exts = language_exts.get(language.lower())
    if exts:
        if len(exts) > 0:
            return (
             exts[1], exts[0])
    raise Exception(f"can`t find language: {language}")


if __name__ == '__main__':
    print(ext2language('py'))
    print(language2ext('Go'))