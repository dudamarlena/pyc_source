# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfred/develop/wxcloudsdk/wxcloudsdk/file_manager.py
# Compiled at: 2020-03-09 04:19:27
# Size of source mod 2**32: 2384 bytes
import requests, json, hashlib
UPLOAD_API = 'https://api.weixin.qq.com/tcb/uploadfile'
COLLECTION_DELETE_API = 'https://api.weixin.qq.com/tcb/databasecollectiondelete'
COLLECTION_ADD_API = 'https://api.weixin.qq.com/tcb/databasecollectionadd'
COLLECTION_MIGRATE_API = 'https://api.weixin.qq.com/tcb/databasemigrateimport'

def get_md5(title):
    """
    return md5 code for the given string
        :param title: content to encode
    """
    if isinstance(title, str):
        title = title.encode('utf-8')
        md = hashlib.md5()
        md.update(title)
        return md.hexdigest()


def upload_file(token, env_id, cloud_path, cloud_dir, local_path):
    """
    upload file to the cloud storage by just one call
    :param token: wx token
    :param env_id: cloud env ID
    :param cloud_path: cloud path e.g.:demo/file.json
        :param cloud_dir: cloud dir e.g.:demo/
        :param local_path: localpath  e.g.:~/demo/file.json
    """
    post_url = UPLOAD_API + '?access_token=' + token
    payload = json.dumps({'env':env_id,  'path':cloud_path})
    try:
        upload = requests.post(post_url, data=payload)
        res = upload.json()
        form = {}
        form['key'] = cloud_dir + res['url'].split('/')[(-1)]
        form['Signature'] = res['authorization']
        form['x-cos-security-token'] = res['token']
        form['x-cos-meta-fileid'] = res['cos_file_id']
        res = (form, res['url'])
        form = res[0]
        upload_url = res[1]
        with open(local_path, 'rb') as (f):
            form['file'] = f.read()
            try:
                success = requests.post(upload_url, files=form)
                print(success)
            except Exception as e:
                try:
                    print(e)
                finally:
                    e = None
                    del e

    except Exception as e:
        try:
            print(e)
        finally:
            e = None
            del e


def rebuild(file, env, token, collection_name):
    """
    rebuild cloud collection by remove and rebuilding
    :param file: file path e.g.: datas/demo.json
    :param token: wx token
        :param collection_name: collection name
    """
    data = {'env':env, 
     'collection_name':collection_name, 
     'file_path':file, 
     'file_type':1, 
     'stop_on_error':False, 
     'conflict_mode':2}
    payload = json.dumps({'env':env,  'collection_name':collection_name})
    requests.post((COLLECTION_DELETE_API + '?access_token=' + token), data=payload)
    requests.post((COLLECTION_ADD_API + '?access_token=' + token), data=payload)
    r = requests.post((COLLECTION_MIGRATE_API + '?access_token=' + token), data=(json.dumps(data)))
    return r