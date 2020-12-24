# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marx/venv3/lib/python3.6/site-packages/tsr/modules/os_info.py
# Compiled at: 2018-07-08 03:20:43
# Size of source mod 2**32: 10478 bytes
import os, json, shutil, glob
from requests import get as requests_get
from pathlib import Path as pathlib_Path
from collections import namedtuple
from .colours import cl
if os.name != 'posix':
    try:
        from psutil import Process
        use_psutil = True
    except ImportError:
        use_psutil = False

def rm_ext(fp):
    return '.'.join(fp.split('.')[:-1])


def replace_ext(fp, new_ext):
    return '.'.join(fp.split('.')[:-1]) + '.' + new_ext


def parent_dir(fp):
    return '/'.join(fp.split('/')[:-1])


def lsfiles(root_dir, **kwargs):
    blacklist_ext = []
    whitelist_ext = []
    whitelist_all = True
    recursive = False
    ext_case_sensitive = False
    full_paths = True
    relative_paths = False
    if 'blacklist_ext' in kwargs:
        blacklist_ext = kwargs['blacklist_ext']
        if type(blacklist_ext) == type(''):
            blacklist_ext = blacklist_ext.split(' ')
    if 'whitelist_ext' in kwargs:
        whitelist_ext = kwargs['whitelist_ext']
        if type(whitelist_ext) == type(''):
            whitelist_ext = whitelist_ext.split(' ')
    if 'whitelist_all' in kwargs:
        whitelist_all = kwargs['whitelist_all']
    elif 'recursive' in kwargs:
        recursive = kwargs['recursive']
    else:
        if 'full_paths' in kwargs:
            full_paths = kwargs['full_paths']
        else:
            if 'relative_paths' in kwargs:
                relative_paths = kwargs['relative_paths']
            else:
                if 'paths' in kwargs:
                    if kwargs['paths'] == 'relative':
                        relative_paths = True
                    elif kwargs['paths'] == 'full':
                        full_paths = True
                if full_paths & relative_paths:
                    raise Exception('full_paths and relative_paths flags are mutually exclusive')
                fp_ls = []
                if 'glob' in kwargs:
                    fp_ls = glob.glob(os.path.join(root_dir, kwargs['glob']))
                else:
                    if recursive:
                        for path, dirs, files in os.walk(root_dir):
                            filepaths = []
                            for fname in files:
                                ext = fname.split('.')[(-1)].lower()
                                if (ext in whitelist_ext) | (ext not in blacklist_ext) & whitelist_all:
                                    if full_paths:
                                        filepaths.append(os.path.join(path, fname))
                                    else:
                                        if relative_paths:
                                            dummy = os.path.join(path, fname)
                                            filepaths.append(dummy.split(root_dir)[(-1)])
                                        else:
                                            filepaths.append(fname)

                            fp_ls = fp_ls + filepaths

                    else:
                        fp_ls = os.listdir(root_dir)
                        if full_paths:
                            fp_ls = [os.path.join(root_dir, fname) for fname in fp_ls]
            fp_ls = whitelist_all or [fp for fp in fp_ls if fp.split('.')[(-1)].lower() in whitelist_ext]
        fp_ls = [fp for fp in fp_ls if fp.split('.')[(-1)].lower() not in blacklist_ext]
    for i in range(len(fp_ls)):
        while '/./' in fp_ls[i]:
            fp_ls[i] = fp_ls[i].replace('/./', '/')

    if 'sort' in kwargs:
        if kwargs['sort'] in ('modified', 'mtime'):
            fp_ls.sort(key=(lambda x: os.path.getmtime(x)))
    return fp_ls


def lsdir(path, **kwargs):
    paths = os.listdir(path)
    if 'items' in kwargs:
        item_n = int(kwargs['items'][1:])
        if kwargs['items'][0] == '>':
            dirls = [pth for pth in paths if os.path.isdir(os.path.join(path, pth))]
            paths = [pth for pth in dirls if len(os.listdir(os.path.join(path, pth))) > item_n]
        else:
            if kwargs['items'][0] == '=':
                dirls = [pth for pth in paths if os.path.isdir(os.path.join(path, pth))]
                paths = [pth for pth in dirls if len(os.listdir(os.path.join(path, pth))) == item_n]
            elif kwargs['items'][0] == '<':
                dirls = [pth for pth in paths if os.path.isdir(os.path.join(path, pth))]
                paths = [pth for pth in dirls if len(os.listdir(os.path.join(path, pth))) < item_n]
    if 'type' in kwargs:
        if kwargs['type'] == 'd':
            paths = [pth for pth in paths if os.path.isdir(os.path.join(path, pth))]
        else:
            if kwargs['type'] == 'f':
                paths = [pth for pth in paths if os.path.isfile(os.path.join(path, pth))]
            elif kwargs['type'] == 'l':
                paths = [pth for pth in paths if os.path.islink(os.path.join(path, pth))]
    if 'ignoreSymlinks' in kwargs:
        if kwargs['ignoreSymlinks']:
            paths = [pth for pth in paths if not os.path.islink(os.path.join(path, pth))]
    if 'onlySymlinks' in kwargs:
        if kwargs['onlySymlinks']:
            paths = [pth for pth in paths if os.path.islink(os.path.join(path, pth))]
    return paths


def lsdir_if(path, **kwargs):
    return lsdir(path, **kwargs)


def jdump(d, fp):
    json.dump(d, open(fp, 'w'))


class BadRequest(Exception):
    pass


def download_file(url, destination_dir=os.getcwd(), destination_filename=None, **kwargs):
    attempt_https = 1
    if 'attempt_https' in kwargs:
        attempt_https = kwargs['attempt_https']
    else:
        to_print = ''
        if url[:7] == 'http://':
            to_print += cl.yellow + 'W: Not using HTTPS  ' + cl.end
            if attempt_https:
                url = 'https://' + url[7:]
        if not destination_filename:
            destination_filename = url.split('/')[(-1)]
        request = requests_get(url, stream=True)
        if request.ok:
            mkdir(destination_dir)
            if 'chunkSize' in kwargs:
                with open(os.path.join(destination_dir, destination_filename), 'wb') as (f):
                    for chunk in request.iter_content(chunk_size=(kwargs['chunkSize'])):
                        f.write(chunk)

            else:
                with open(os.path.join(destination_dir, destination_filename), 'wb') as (f):
                    shutil.copyfileobj(request.raw, f)
            request.close()
            to_print += '{}{}{} {}/{}'.format(cl.cyan, url, cl.end, destination_dir, destination_filename)
            print(to_print)
        else:
            print(cl.red, 'Bad request', cl.end)
            raise BadRequest('Bad request')


def writeif(path, content, readonly=False, **kwargs):
    if readonly:
        return
    else:
        append = False
        if 'append' in kwargs:
            append = True
        if append:
            with open(path, 'a') as (f):
                f.write(content)
        else:
            with open(path, 'w') as (f):
                f.write(content)


def mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        return
    except Exception as e:
        print(cl.red, e, cl.end)


def touch(path):
    if not os.path.isfile(path):
        pathlib_Path(path).touch()


def bytes_to_human_readable(n_bytes):
    if n_bytes < 0:
        return '-' + positive_bytes_to_human_readable(n_bytes)
    else:
        return positive_bytes_to_human_readable(n_bytes)


def positive_bytes_to_human_readable(n_bytes):
    n_bytes = float(n_bytes)
    units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while n_bytes > 1024:
        i += 1
        n_bytes /= 1024.0

    unit = units[i]
    n_bytes = round(n_bytes, 3)
    return str(n_bytes) + ' ' + unit


def memory_usage_raw():
    status = None
    result = {'peak':0,  'rss':0}
    try:
        status = open('/proc/self/status')
        for line in status:
            parts = line.split()
            key = parts[0][2:-1].lower()
            if key in result:
                result[key] = int(parts[1])

    finally:
        if status is not None:
            status.close()

    return result


def memory_usage():
    if os.name == 'posix':
        d = memory_usage_raw()
        peak = bytes_to_human_readable(d['peak'] * 1024)
        rss = bytes_to_human_readable(d['rss'] * 1024)
        return {'peak':peak, 
         'rss':rss}
    else:
        if use_psutil:
            process = Process(os.getpid())
            return process.memory_info()
        return 'psutil not installed'


def cp(src, dst):
    try:
        shutil.copytree(src, dst)
    except:
        shutil.copy(src, dst)


def free_space(path):
    statvfs = os.statvfs(path)
    return statvfs.f_frsize * statvfs.f_bavail


file_location = os.path.join(os.path.expanduser('~'), '.config', 'tsr', 'paths.json')
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
default_path_settings = os.path.join(root_dir, 'settings')
if os.path.isfile(file_location):
    paths = json.load(open(file_location, 'r'))
else:
    paths = {'main':root_dir, 
     'posts':os.path.join(root_dir, 'posts'), 
     'threads':os.path.join(root_dir, 'threads'), 
     'threads_json':os.path.join(root_dir, 'threads.json'), 
     'forums':os.path.join(root_dir, 'forums'), 
     'users':os.path.join(root_dir, 'users'), 
     'users_json':os.path.join(root_dir, 'users.json'), 
     'avatars':os.path.join(root_dir, 'avatars'), 
     'settings':os.path.join(os.path.expanduser('~'), '.config', 'tsr'), 
     'images':os.path.join(os.path.expanduser('~'), 'Pictures', 'tsr'), 
     'log':os.path.join(root_dir, 'log.txt')}
    cp(default_path_settings, paths['settings'])
    with open(file_location, 'w') as (f):
        json.dump(paths, f)
path_variables_str = ' '.join([path for path in paths])
PathObject = namedtuple('path', path_variables_str)
path = PathObject(**paths)
del path_variables_str
if not os.path.isdir(path.settings):
    cp(default_path_settings, path.settings)
for key in paths:
    object_path = paths[key]
    if object_path.split('.')[(-1)] == 'json':
        if not os.path.isfile(object_path):
            open(object_path, 'w').write('{}')
    else:
        if object_path.split('.')[(-1)] not in ('txt', ):
            mkdir(object_path)
        else:
            touch(object_path)