# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\markdown2html.py
# Compiled at: 2019-04-01 23:35:22
import sys, os, markdown, codecs
css = '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<style type="text/css">\n<!-- 此处省略掉markdown的css样式，因为太长了 -->\n</style>\n'

def main(argv):
    name = argv[0]
    in_file = '%s.md' % name
    out_file = '%s.html' % name
    print os.path.abspath(in_file)
    print os.path.abspath(out_file)
    input_file = codecs.open(in_file, mode='r', encoding='utf-8')
    text = input_file.read()
    html = markdown.markdown(text)
    output_file = codecs.open(out_file, 'w', encoding='utf-8', errors='xmlcharrefreplace')
    output_file.write(css + html)


if __name__ == '__main__':
    main(sys.argv[1:])