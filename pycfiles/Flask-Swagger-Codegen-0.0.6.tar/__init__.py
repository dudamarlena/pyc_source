# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rejown/Development/Project/flask_restful_swagger_codegen/flask_swagger_codegen/__init__.py
# Compiled at: 2015-04-16 04:05:52
import codecs, click
from parser import parse_yaml
import writer
__version__ = '0.0.5'

@click.command()
@click.argument('path', required=True)
@click.option('-s', '--swagger-doc', required=True, help='Swagger doc file.')
@click.option('-f', '--force', is_flag=True, help='Force overwrite.')
@click.option('-a', '--appname', help='Application name or package name.')
def codegen(path, swagger_doc, force=False, appname=None):
    if appname is None:
        appname = path.split('/')[(-1)].replace('-', '_')
    with codecs.open(swagger_doc, 'r', 'utf-8') as (f):
        m = parse_yaml(f)
    if not m:
        print 'swagger-doc could not be read.'
        exit(-1)
    writer.write(m, path, appname, force)
    return


if __name__ == '__main__':
    codegen()