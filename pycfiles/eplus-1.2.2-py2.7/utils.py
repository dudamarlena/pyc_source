# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eplus/utils.py
# Compiled at: 2019-09-05 08:48:18
import os

def which(program):

    def is_exe(fxpath):
        return os.path.isfile(fxpath) and os.access(fxpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return


def find_sdk():
    env_sdk = os.environ.get('GAE_SDK_ROOT')
    if env_sdk:
        return env_sdk
    gcloud_path = which('gcloud')
    if gcloud_path:
        gcloud_path = os.path.realpath(gcloud_path)
        check_path = os.path.join(os.path.dirname(gcloud_path), '..', 'platform', 'google_appengine')
        try:
            os.stat(check_path)
            return check_path
        except OSError:
            pass

    devappserver_path = which('dev_appserver.py')
    if devappserver_path:
        devappserver_path = os.path.realpath(devappserver_path)
        check_path = os.path.join(os.path.dirname(devappserver_path), '..', 'platform', 'google_appengine')
        try:
            os.stat(check_path)
            return check_path
        except OSError:
            pass

        check_path = os.path.join(os.path.dirname(devappserver_path), 'google', 'appengine')
        try:
            os.stat(check_path)
            return os.path.dirname(devappserver_path)
        except OSError:
            pass


def find_gcloud_lib():
    gcloud_path = which('gcloud')
    if gcloud_path:
        gcloud_path = os.path.realpath(gcloud_path)
        check_path = os.path.join(os.path.dirname(gcloud_path), '..', 'lib')
        try:
            os.stat(check_path)
            return check_path
        except OSError:
            pass