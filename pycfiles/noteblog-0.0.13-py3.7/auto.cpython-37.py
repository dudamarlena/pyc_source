# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/spider/auto.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2264 bytes
import codecs
from requests import get
from ..time_utils import get_shanghai_time
import templates.config as config
__all__ = [
 'auto_generate_crawler_code']

def auto_generate_crawler_code():
    """
    爬虫代码自动生成器
    :return:
    """

    def get_template_str():
        template_url = 'http://pdfs3i7nf.bkt.clouddn.com/base_spider_template.txt'
        s = get(url=template_url).content.decode('utf-8')
        return s

    s = get_template_str()
    if not s:
        return False
    print('#--------------------------------')
    print('# 爬虫模板自动生成器 by super_fazai')
    print('#--------------------------------')
    print('@@ 下面是备选参数, 无输入则取默认值!!')
    author = input('请输入author:')
    connect = input('请输入email:')
    file_name = input('请输入创建的文件名(不含.py):')
    class_name = input('请输入class_name:')
    try:
        s = s.format(author=(config.get('author') if author == '' else author),
          file_name=(config.get('file_name') if file_name == '' else file_name),
          create_time=(str(get_shanghai_time())),
          connect=(config.get('connect') if connect == '' else connect),
          class_name=(config.get('class_name') if class_name == '' else class_name))
    except Exception as e:
        try:
            print('遇到错误:', e)
            return False
        finally:
            e = None
            del e

    file_name = config['file_name'] + '.py' if file_name == '' else file_name + '.py'
    with codecs.open(file_name, 'wb', 'utf-8') as (f):
        f.write(s)
        f.flush()
    print('\n创建爬虫文件{0}完毕!\nenjoy!🍺'.format(file_name))
    return True