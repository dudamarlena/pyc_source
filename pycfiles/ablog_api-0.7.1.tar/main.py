# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ablog_api/main.py
# Compiled at: 2016-09-01 13:30:00
"""
    Module ablog_api.main
"""
import os, sys, json, logging, glob, shutil, gc, re
from os.path import expanduser, join
from datetime import datetime
from optparse import OptionParser
from flask import Flask, abort, request, send_from_directory
from werkzeug.utils import secure_filename
import ablog, sphinx, ablog_api
from ablog_api.util import Trace, LEVEL, ConfigAblog
from ablog_api.login import Login, login_required
from ablog_api.doc import Doc
app = Flask(__name__)
app.doc = Doc(app, '/api').doc
app.trace = Trace(app).trace
app.login = Login(app, '/api')
app.config = ConfigAblog(app.config)
app.config['ABLOG_RELOAD'] = 'unknow'

def getEnv(reload=False):
    if reload or not app.config.get('ABLOG_PICKLE', None):
        if len(app.config.get('ABLOG_PICKLE', [])):
            del app.config['ABLOG_PICKLE']
        app.config['ABLOG_PICKLE'] = []
        for f in glob.glob(os.path.join(app.config['ABLOG_SRC_DIR'], '*%s' % app.config['ABLOG_CONF'].source_suffix)):
            docname = f.split(os.sep)[(-1)].split('.')[0]
            with open(f, 'r') as (d):
                data = ('').join(open(f, 'r').readlines())
                try:
                    tags = re.findall(':tags:.*\\n', data)[0][6:-1].strip().split(',')
                except:
                    tags = []

                try:
                    category = re.findall(':category:.*\\n', data)[0][10:-1].strip().split(',')
                except:
                    category = []

                try:
                    author = re.findall(':author:.*\\n', data)[0][8:-1].strip().split(',')
                except:
                    author = []

                try:
                    find = False
                    txt = data.split('\n')
                    title = 'unknown'
                    old = ''
                    while len(txt) and not find:
                        l = txt[0].strip()
                        if len(re.findall('[\\*=-]+', l)):
                            if len(re.findall('[\\*=-]+', l)[0]) == len(l):
                                title = old
                                find = True
                        del txt[0]
                        old = l

                except:
                    title = 'unknown'

                try:
                    date = re.findall('post::.*\\n', data)[0][6:-1].strip()
                except:
                    date = datetime.now().strftime(app.config['ABLOG_CONF'].post_date_format)

                try:
                    update = datetime.fromtimestamp(os.path.getmtime(f)).strftime(app.config['ABLOG_CONF'].post_date_format)
                except:
                    update = datetime.now().strftime(app.config['ABLOG_CONF'].post_date_format)

            app.config['ABLOG_PICKLE'].append({'docname': docname, 'tags': tags, 'category': category, 'author': author, 'title': title, 'date': date, 'update': update})

        app.logger.debug(app.config['ABLOG_PICKLE'])
        app.config['ABLOG_RELOAD'] = datetime.now().strftime('%Y%m%d%H%M%S')
    gc.collect()
    return app.config['ABLOG_PICKLE']


@app.route('/api/version', methods=['GET'])
@app.doc.doc()
@app.trace
def url_version():
    """ 
    list of version: ablog, ablog-api
    """
    return json.dumps([{'module': 'ablog', 'version': ablog.__version__}, {'module': 'ablog_api', 'version': ablog_api.__version__}, {'module': 'python', 'version': ('.').join([ str(a) for a in sys.version_info[0:3] ])}, {'module': 'pickle', 'version': app.config['ABLOG_RELOAD']}])


@app.route('/api/ls', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_ls():
    """ 
    list of post with information

    * categorys
    * tags
    * docname
    * author
    * title
    * date (epoch)
    """
    data = getEnv()
    lst = []
    for post in data:
        lst.append(post)
        lst[(-1)]['encoding'] = app.config['ABLOG_CONF'].source_encoding
        lst[(-1)]['post_date_format'] = app.config['ABLOG_CONF'].post_date_format

    return json.dumps(lst)


@app.route('/api/rm', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_rm():
    """ 
    delete post

    **param**:

    - docname post
    """
    if not request.data:
        request.data = str(json.dumps({})).encode()
    docname = json.loads(request.data.decode()).get('docname', '')
    if not len(docname):
        abort(418)
    os.remove(os.path.join(app.config['ABLOG_SRC_DIR'], '%s%s' % (docname, app.config['ABLOG_CONF'].source_suffix)))
    getEnv(reload=True)
    return json.dumps({'rm': True})


@app.route('/api/upload/<path:path>', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_upload(path):
    """ 
    upload file in directory

    **param**:

    - file
    """
    bfile = request.data
    if not len(bfile) or not len(path):
        abort(418)
    if app.config.allowed_file(path):
        with open(os.path.join(app.config['ABLOG_SRC_DIR'], *path.split('/')), 'wb') as (file_):
            file_.write(bfile)
        return json.dumps({'upload': True})
    return abort(418)


@app.route('/api/download', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_download():
    """ 
    download file

    **param**:

    - path
    """
    if not request.data:
        request.data = str(json.dumps({})).encode()
    path = json.loads(request.data.decode()).get('path', '')
    if not len(path) or path.endswith('conf.py'):
        abort(418)
    return send_from_directory(app.config['ABLOG_SRC_DIR'], path)


@app.route('/api/edit/<docname>', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_edit(docname):
    """ 
    edit post

    **param**:

    - docname
    """
    try:
        bfile = request.data
        if not len(bfile) or not len(docname):
            abort(418)
        with open(os.path.join(app.config['ABLOG_SRC_DIR'], '%s%s' % (docname, app.config['ABLOG_CONF'].source_suffix)), 'wb') as (file_):
            file_.write(bfile)
        getEnv(reload=True)
        return json.dumps({'save': True})
    except Exception as e:
        app.logger.debug(e)
        return json.dumps({'save': False})


@app.route('/api/build', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_build():
    """ 
    build ablog

    **param**:

    - all (default: false)
    """
    try:
        if not request.data:
            request.data = str(json.dumps({})).encode()
        allfiles = json.loads(request.data.decode()).get('all', False)
        argv = sys.argv[:1]
        argv.extend(['-b', app.config['ABLOG_BUILDER']])
        argv.extend(['-d', app.config['ABLOG_DOCTREES']])
        if allfiles:
            argv.extend(['-a'])
        argv.extend([app.config['ABLOG_SRC_DIR'], app.config['ABLOG_WEBSITE']])
        sphinx.build_main(argv)
        getEnv(reload=True)
        return json.dumps({'build': True})
    except Exception as e:
        app.logger.debug(e)
        return json.dumps({'build': False})


@app.route('/api/clean', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_clean():
    """ 
    clean ablog

    **param**:

    - deep (default: false)

    """
    if not request.data:
        request.data = str(json.dumps({})).encode()
    deep = json.loads(request.data.decode()).get('deep', False)
    nothing = True
    if glob.glob(os.path.join(app.config['ABLOG_WEBSITE'], '*')):
        shutil.rmtree(app.config['ABLOG_WEBSITE'])
        app.logger.debug(('Removed {}.').format(os.path.relpath(app.config['ABLOG_WEBSITE'])))
        nothing = False
    if deep and glob.glob(os.path.join(app.config['ABLOG_DOCTREES'], '*')):
        shutil.rmtree(app.config['ABLOG_DOCTREES'])
        app.logger.debug(('Removed {}.').format(os.path.relpath(app.config['ABLOG_DOCTREES'])))
        nothing = False
    if nothing:
        app.logger.debug('Nothing to clean.')
    return json.dumps({'clean': True})


@app.route('/api/get', methods=['POST'])
@app.doc.doc()
@app.trace
def url_get():
    """ 
    return post

    **param**:

    - docname
    """
    if not request.data:
        request.data = str(json.dumps({})).encode()
    encoding = app.config['ABLOG_CONF'].source_encoding
    docname = json.loads(request.data.decode()).get('docname', '')
    data = getEnv()
    if docname not in [ post['docname'] for post in data ] or not len(docname):
        abort(418)
    return send_from_directory(app.config['ABLOG_SRC_DIR'], '%s%s' % (docname, app.config['ABLOG_CONF'].source_suffix))


@app.route('/api/conf', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_conf():
    """ 
    return value of conf

    **param**:

    - key
    """
    if not request.data:
        request.data = str(json.dumps({})).encode()
    key = json.loads(request.data.decode()).get('key', '')
    if not len(key):
        abort(418)
    if key.isupper():
        return json.dumps({key: app.config[key]})
    else:
        return json.dumps({key: getattr(app.config['ABLOG_CONF'], key, None)})


@app.route('/api/reload', methods=['POST'])
@login_required
@app.doc.doc()
@app.trace
def url_reload():
    """ 
    reload environnement
    """
    try:
        getEnv(reload=True)
        return json.dumps({'reload': 'ok'})
    except Exception as e:
        app.logger.debug(e)
        return json.dumps({'reload': 'ko'})


def main():
    parser = OptionParser(version='ablog-api %s' % ablog_api.__version__, usage='usage: %prog [options] args')
    parser.description = 'run a api server for ablog'
    parser.epilog = 'by Frederic Aoustin'
    parser.add_option('-H', '--host', dest='host', help='the hostname to listen on', type='string', default='')
    parser.add_option('-p', '--port', dest='port', help='the port of the webserver', type='int')
    parser.add_option('-c', '--conf', dest='conf', help='file configuration', type='string', default='')
    parser.add_option('-d', '--dir', dest='dir_ablog', help='dir of conf ablog', type='string', default='')
    parser.add_option('-l', '--log', dest='level', help='level of log: %s' % (',').join(LEVEL), type='string', default='')
    options, args = parser.parse_args()
    try:
        app.config['ABLOG_HOST'] = '0.0.0.0'
        app.config['ABLOG_PORT'] = 5000
        app.config['ABLOG_LEVEL_LOG'] = logging.DEBUG
        app.config['ABLOG_CONF_DIR'] = os.path.abspath('.')
        app.config.from_pyfile(join(expanduser('~'), '.ablog', 'conf.py'), silent=True)
        app.config.from_env('ABLOG_')
        if app.config['ABLOG_LEVEL_LOG'] in LEVEL.keys():
            app.config['ABLOG_LEVEL_LOG'] = LEVEL[app.config['ABLOG_LEVEL_LOG']]
        if options.host:
            app.config['ABLOG_HOST'] = options.host
        if options.port:
            app.config['ABLOG_PORT'] = options.port
        if options.dir_ablog:
            app.config['ABLOG_CONF_DIR'] = os.path.abspath(options.dir_ablog)
        if options.conf:
            app.config.from_pyfile(os.path.abspath(options.conf), silent=False)
        if options.level:
            app.config['ABLOG_LEVEL_LOG'] = LEVEL[options.level]
        app.config.complete()
        app.logger.setLevel(app.config['ABLOG_LEVEL_LOG'])
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(app.config['ABLOG_LEVEL_LOG'])
        app.logger.addHandler(stream_handler)
        app.run(host=app.config['ABLOG_HOST'], port=app.config['ABLOG_PORT'], threaded=True)
    except Exception as e:
        print parser.error(e)
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()