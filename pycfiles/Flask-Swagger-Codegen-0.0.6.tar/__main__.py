# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rejown/Development/Project/flask_restful_swagger_codegen/flask_swagger_codegen/__main__.py
# Compiled at: 2015-04-15 05:01:32
import yaml, click, writer

@click.command()
@click.argument('path', required=True)
@click.option('-s', '--swagger-doc', required=True, help='Swagger doc file.')
@click.option('-a', '--appname', help='Application name or package name.')
def codegen(path, swagger_doc, appname=None):
    if appname is None:
        appname = path.split('/')[(-1)].replace('-', '_')
    print path
    print appname
    with open(swagger_doc) as (f):
        content = yaml.load(f)
    if not content:
        print 'swagger-doc could not be read.'
        exit(-1)
    if not content['swagger'] == '2.0':
        print '"%s" is not a swagger 2.0 doc.' % swagger_doc
        exit(-1)
    writer.write(content, path, name)
    return


if __name__ == '__main__':
    codegen()