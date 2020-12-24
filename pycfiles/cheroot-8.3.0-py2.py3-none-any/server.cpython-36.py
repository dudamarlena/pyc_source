# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/server.py
# Compiled at: 2018-05-12 01:23:06
# Size of source mod 2**32: 2571 bytes
import daemon, tarfile
from daemon import pidfile
import subprocess
from flask import Flask
from flask import request
from flask import send_from_directory
import os
from ChernMachine.kernel.VJob import VJob
from ChernMachine.kernel.VImage import VImage
from ChernMachine.kernel.VContainer import VContainer
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        tarname = request.form['tarname']
        storage_path = os.path.join(os.environ['HOME'], '.ChernMachine/Storage')
        request.files[tarname].save(os.path.join('/tmp', tarname))
        tar = tarfile.open(os.path.join('/tmp', tarname), 'r')
        for ti in tar:
            tar.extract(ti, os.path.join(storage_path, tarname[:-7]))

        tar.close()


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    directory = os.getcwd() + '/data'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/test', methods=['GET'])
def test():
    return 'Good'


@app.route('/status/<impression>', methods=['GET'])
def status(impression):
    path = os.path.join(os.environ['HOME'], '.ChernMachine/Storage', impression)
    job = VJob(path)
    if job.job_type() == 'image':
        return VImage(path).status()
    else:
        if job.job_type() == 'container':
            return VContainer(path).status()
        return 'impressed'


@app.route('/outputs/<impression>', methods=['GET'])
def outputs(impression):
    path = os.path.join(os.environ['HOME'], '.ChernMachine/Storage', impression)
    job = VJob(path)
    if job.job_type() == 'container':
        return ' '.join(VContainer(path).outputs())
    else:
        return ''


@app.route('/getfile/<impression>/<filename>', methods=['GET'])
def get_file(impression, filename):
    path = os.path.join(os.environ['HOME'], '.ChernMachine/Storage', impression)
    job = VJob(path)
    if job.job_type() == 'container':
        return VContainer(path).get_file(filename)


def start():
    daemon_path = os.path.join(os.environ['HOME'], '.ChernMachine/daemon')
    with daemon.DaemonContext(working_directory='/',
      pidfile=(pidfile.TimeoutPIDLockFile(daemon_path + '/server.pid')),
      stderr=(open(daemon_path + '/server.log', 'w+'))):
        app.run()


def stop():
    if status() == 'stop':
        return
    daemon_path = os.path.join(os.environ['HOME'], '.ChernMachine/daemon')
    subprocess.call(('kill {}'.format(open(daemon_path + '/server.pid').read())), shell=True)


def status():
    pass