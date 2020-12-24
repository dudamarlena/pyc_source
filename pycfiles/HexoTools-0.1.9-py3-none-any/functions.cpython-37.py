# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\HexoTools\hexotools\functions.py
# Compiled at: 2019-10-06 05:35:08
# Size of source mod 2**32: 1758 bytes
import sys
print(sys.path)
import os, json
import postprocess.post as P
PKG_PATH = os.path.dirname(__file__)
config_path = os.path.join(PKG_PATH, 'config.json')
with open(config_path, 'r', encoding='utf-8') as (fo):
    config = json.load(fo)

def urlFormat(url, delete_url='', description='', path=''):
    s = (
     '###--Markdown--###\n', '![{0}]({1})'.format(description, url), '\n\n',
     '###-----URL----###\n', '%s' % url, '\n\n', '###----HTML----###\n',
     '<a href="%s" target="_blank"><img src="https://i.loli.net/2019/10/03/TBgyP2nEcFar8Vw.png" ></a>' % url, '\n\n')
    if delete_url:
        s += ('###---删除URL---###\n', '%s' % delete_url, '\n\n')
    if path:
        s += ('###---本地路径---###\n', '%s' % path)
    return ''.join(s)


def setPath(path):
    if os.path.isdir(path):
        config['blog_path'] = os.path.normpath(path)
        config['disk'] = config['blog_path'].split(os.path.sep)[0]
        config['posts_path'] = os.path.join(config['blog_path'], 'source{}_posts'.format(os.path.sep))
        with open(config_path, 'w') as (fo):
            json.dump(config, fo, sort_keys=True, indent=4)


def setCwd(path):
    if os.path.isdir(path):
        config['cwd'] = os.path.normpath(path)
        with open(config_path, 'w') as (fo):
            json.dump(config, fo, sort_keys=True, indent=4)


def editCate(folder=config['posts_path'], root=config['posts_path']):
    edit_cate = P.EditCate()
    for i in edit_cate.getMDFlie(folder):
        edit_cate.writeToFile(i, edit_cate.getWriteContent(i, root))


if __name__ == '__main__':
    r = urlFormat('http://www.baidu.com', delete_url='DD', description='tu')
    print(r)