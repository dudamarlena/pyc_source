# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/lib/fs/dropbox_fs.py
# Compiled at: 2011-07-12 22:16:02
import httplib, tempfile, base64, os, json
from dropbox import client, rest, auth

class FileSystem:

    def __init__(self, username, password, root, config_path):
        config = auth.Authenticator.load_config(config_path)
        dba = auth.Authenticator(config)
        access_token = dba.obtain_trusted_access_token(username, password)
        self.db_client = client.DropboxClient(config['server'], config['content_server'], config['port'], dba, access_token)
        self.db_root = config['root']
        self.root = root

    def listdir(self):
        """Return a list of file paths"""
        file_list = []
        r = self.db_client.metadata(self.db_root, self.root)
        data = json.loads(r.body)
        for f in data['contents']:
            file_list.append(f['path'].replace(self.root, ''))

        return file_list

    def get(self, path):
        """Returns a temp file path"""
        r = self.db_client.get_file(self.db_root, os.path.join(self.root, path))
        temppath = tempfile.mkstemp(suffix='.org')[1]
        fd = open(temppath, 'w')
        fd.write(r.read())
        fd.close()
        return temppath

    def put(self, path, temppath):
        fd = open(temppath, 'r')
        r = self.db_client.put_file(self.db_root, os.path.join(self.root, path), fd)
        print r
        fd.close()

    def rm(self, path):
        os.remove(path)