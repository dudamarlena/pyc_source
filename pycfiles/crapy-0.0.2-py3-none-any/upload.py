# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jake/CRAPtion/craption/upload.py
# Compiled at: 2018-05-18 03:38:48
from craption import settings
from sfs_upload import sfs_upload
import base64, dropbox as dropbox_lib, requests, subprocess
conf = settings.get_conf()

def upload(path, filename):
    if conf.get('upload').as_bool('upload'):
        to = conf['upload']['to'].lower()
        if to == 'imgur':
            return imgur(path, conf['upload']['imgur']['api-key'])
        if to == 'scp':
            return scp(path, filename, conf['upload']['scp'])
        if to == 'dropbox':
            return dropbox(path, filename, conf['upload']['dropbox'])
        if to == 'sfs':
            return sfs(path, filename, conf['upload'].get('sfs_host'))


def dropbox(local_path, filename, dropconf):
    print dropconf
    client = dropbox_lib.client.DropboxClient(dropconf['token'])
    uploaded = client.put_file('/' + filename, open(local_path))
    return client.share(uploaded['path'])['url']


def imgur(path, api_key):
    img_data = base64.b64encode(open(path, 'rb').read())
    data = {'image': img_data}
    url = 'https://api.imgur.com/3/upload'
    headers = {'Authorization': 'Client-ID ' + api_key}
    res = requests.post(url, data=data, headers=headers).json()
    return res['data']['link']


def scp(local_file, filename, scpconf):
    cmd = [
     'scp',
     local_file,
     '%s@%s:%s/%s' % (
      scpconf['user'],
      scpconf['host'],
      scpconf['path'],
      filename)]
    nullw = open('/dev/null', 'w')
    nullr = open('/dev/null')
    p = subprocess.Popen(cmd, stdout=nullw, stdin=nullr, stderr=nullw)
    p.wait()
    return scpconf['url'].replace('{f}', filename)


def sfs(path, filename, host):
    fh = open(path, 'rb')
    return sfs_upload.upload(host, fh, filename)