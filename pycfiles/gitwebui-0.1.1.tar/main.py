# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/gitwebui/gitwebui/main.py
# Compiled at: 2017-10-31 15:05:53
import os, os.path, sys, subprocess, platform, codecs, shlex, socket
from flask import Flask, send_from_directory, request, abort, Response

def process(cmd, stdin, add_footers, repo_root, env=None):
    git = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repo_root, env=env)
    stdout, stderr = git.communicate(stdin)
    if add_footers:
        stdout = stdout + stderr
        stdout = stdout + '\r\n'
        stdout = stdout + codecs.encode('\r\nGit-Stderr-Length: ' + str(len(stderr)), 'utf-8')
        stdout = stdout + codecs.encode('\r\nGit-Return-Code: ' + str(git.returncode), 'utf-8')
    elif git.returncode != 0:
        print stderr
    return stdout


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return static_web('index.html')


@app.route('/<path:path>', methods=['GET'])
def static_web(path):
    return send_from_directory(app.config['WEB_ROOT'], path)


@app.route('/git/cat-file/<path:path>', methods=['GET'])
def catfile(path):
    r = Response(response=process(['git', '-c', 'color.ui=false', 'cat-file', '-p', path], '', False, app.config['REPO_ROOT']), status=200, mimetype='text')
    r.headers['Content-Type'] = ''
    return r


@app.route('/hostname', methods=['GET'])
def hostname():
    return codecs.encode(socket.gethostname(), 'utf-8')


@app.route('/dirname', methods=['GET'])
def dirname():
    wc = os.path.split(app.config['REPO_ROOT'])[1]
    return codecs.encode(wc, 'utf-8')


@app.route('/viewonly', methods=['GET'])
def viewonly():
    return '0'


@app.route('/git', methods=['POST'])
def get_git():
    content = ''
    for key in request.form.to_dict():
        if len(content):
            content = content + '&'
        if len(request.form.to_dict()[key]):
            content = key + '=' + request.form.to_dict()[key]
        else:
            content = key

    i = content.find('\n')
    if i != -1:
        args = content[:i]
        stdin = content[i + 1:]
    else:
        args = content
        stdin = ''
    cmd = shlex.split('git -c color.ui=true ' + args)
    action = cmd[3]
    if args in ('branch', 'branch --remotes', 'tag') or action in ('show', 'status',
                                                                   'log', 'ls-tree'):
        return process(cmd, stdin, True, app.config['REPO_ROOT'])


if __name__ == '__main__':
    app.config['REPO_ROOT'] = os.path.abspath(os.getcwd())
    if sys.version > '3':
        localpath = os.path.dirname(os.path.abspath(__file__))
    else:
        localpath = os.path.dirname(os.path.abspath(__file__)).decode('utf-8')
    app.config['WEB_ROOT'] = os.path.join(localpath, 'static')
    app.run(host='0.0.0.0', port=5000)