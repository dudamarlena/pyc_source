# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lback/core.py
# Compiled at: 2014-10-30 13:58:06
"""
Backup tool for linux.
This performs the needed functionality
behind this specifcation.

Implementors must deciede which 
version to run and on what port. This
file acts as 'both' a client and server
and can be started from the command line
via -c or -s respectively.
"""
from dal import DAL, Field
import zipfile, shutil, socket, glob, time, json, uuid, sys, os, re, zipfile, os.path
LOCAL_BACKUP_DIR = './backups/'
LOCAL_RESTORE_DIR = './restores/'

class Backup(object):

    def __init__(self, record_id, folder='./', client=True):
        global LOCAL_BACKUP_DIR
        if not folder[(len(folder) - 1)] == '/':
            folder += '/'
        self.things = []
        self.record_id = record_id
        if client:
            self.zip = zipfile.ZipFile(LOCAL_BACKUP_DIR + record_id + '.zip', 'w', zipfile.ZIP_DEFLATED)
        self.status = 0
        self.folder = folder

    def raw(self, content):
        try:
            from cStringIO import StringIO
        except:
            from StringIO import StringIO

        f = open(self.get(), 'w+')
        f.write(content)
        f.close()
        self.status = 1

    def run(self):
        l = os.listdir(self.folder)
        self.zip.write(self.folder)
        folders = [ self._folder(i, self.folder) for i in l if os.path.isdir(self.folder + i) ]
        files = [ self._file(i, self.folder) for i in l if os.path.isfile(self.folder + i) ]
        self.pack()

    def get(self):
        return LOCAL_BACKUP_DIR + self.record_id + '.zip'

    def pack(self):
        print 'Files have been gathered. Forming archive..'
        for i in self.things:
            self.zip.write(i, os.path.relpath(i, self.folder))

        print 'Files found: '
        print self.things
        self.zip.close()
        self.status = 1

    def _folder(self, anchor, prefix=''):
        l = os.listdir(prefix + anchor)
        print 'added => ' + prefix + anchor
        folders = [ self._folder(i, prefix + anchor) for i in l if os.path.isdir(prefix + anchor + i) ]
        files = [ self._file(i, prefix + anchor + '/') for i in l if os.path.isfile(prefix + anchor + '/' + i) ]
        self.things.append(prefix + anchor)
        return prefix + anchor

    def _file(self, anchor, prefix=''):
        print 'added => ' + prefix + anchor
        self.things.append(prefix + anchor)
        return prefix + anchor


class Restore(object):

    def __init__(self, zip_file_loc, folder='./', clean=False):
        self.zip_file, self.status = zip_file_loc, 0
        self.clean = clean
        self.folder = folder

    def run(self, local=False, uid=''):
        if local:
            self.zip_file = LOCAL_BACKUP_DIR + uid + '.zip'
        if self.clean:
            shutil.rmtree(self.folder)
            Util().unzip(self.zip_file, self.folder)
        else:
            Util().unzip(self.zip_file, self.folder)
        self.status = 1


import time, socket

def recvall(the_socket, timeout=''):
    the_socket.setblocking(0)
    total_data = []
    data = ''
    begin = time.time()
    if not timeout:
        timeout = 1
    while 1:
        if total_data and time.time() - begin > timeout:
            break
        else:
            if time.time() - begin > timeout * 2:
                break
            wait = 0
            try:
                data = the_socket.recv(4096)
                if data:
                    total_data.append(data)
                    begin = time.time()
                    data = ''
                    wait = 0
                else:
                    time.sleep(0.1)
            except:
                pass

    result = ('').join(total_data)
    return result


class Server(object):

    def __init__(self, port, ip, db, table):
        self.status = 0
        self.ip = ip
        self.db = db
        self.port = port
        self.db_table = table

    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        self.port = int(self.port)
        s.bind((self.ip, self.port))
        s.listen(1)
        while True:
            c, addr = s.accept()
            print 'Got connection from', addr
            message = recvall(c)
            if len(re.findall('RESTORE', message)) > 0:
                s.setblocking(True)
                print "Running 'RESTORE'"
                uid = False
                uid = re.findall('UID:\\s+"([\\w\\d\\-]+)",', message)[0]
                if not uid:
                    continue
                r = self.db(self.db[self.db_table].uid == uid).select().first()
                if not r:
                    print "SERVER couldn't find backup.."
                    continue
                fi = open(LOCAL_BACKUP_DIR + uid + '.zip', 'r')
                contents = fi.read()
                fi.close()
                c.sendall('SUCCESS\nCONTENTS: ' + contents)
                print 'Restore backup fetched.'
                print 'Sending to client..'
                print 'Transaction ID: ' + uid
                continue
            if len(re.findall('BACKUP', message)) > 0:
                print "Running 'BACKUP'"
                uid = 0
                contents = 0
                folder = 0
                name = 'N/A'
                size = 0
                c.sendall('SUCCESS')
                try:
                    uid = re.findall('UID:\\s+"([\\w\\d\\-]+)",', message)[0]
                except:
                    pass

                try:
                    name = re.findall('NAME:\\s+(.*)', message)[0]
                except:
                    pass

                try:
                    size = re.findall('SIZE:\\s+([\\d]+),', message)[0]
                except:
                    pass

                try:
                    folder = re.findall('FOLDER:\\s+"([^^]+)",', message)[0]
                except:
                    pass

                try:
                    contents = re.sub('.*CONTENTS:\\s+', '', message)
                    contents = re.sub('BACKUP.*\n', '', contents)
                except:
                    pass

                if not uid:
                    continue
                if not contents:
                    continue
                bkp = Backup(uid, folder, False)
                bkp.raw(contents)
                if bkp.status:
                    self.db[self.db_table].insert(uid=uid, time=time.time(), folder=folder, size=size, local=False, name=name)
                    self.db.commit()
                    c.sendall('SUCCESS')
                    print 'Backup complete.'
                    print 'Transaction ID: ' + uid


class Output(object):

    def __init__(self):
        pass

    def show(self, msg, times=0):
        if times == 0:
            print msg
        else:
            print msg + '\n' * times


class Client(object):

    def __init__(self, ip, port, server=dict()):
        self.status = 0
        self.server = server

    def run(self, cmd='BACKUP', folder=None, uid='', contents='', name='', size=0):
        s = socket.socket()
        size = str(size)
        s.connect((self.server['ip'], int(self.server['port'])))
        smessage = cmd + ', ' + 'UID: "' + uid + '", ' + 'FOLDER: "' + folder + '", ' + 'SIZE: ' + size + ', ' + 'NAME: ' + name + '\nCONTENTS: ' + contents
        s.sendall(smessage)
        if cmd == 'BACKUP':
            self.m = recvall(s)
        else:
            self.m = ''
            while True:
                m = recvall(s)
                if m == '':
                    break
                self.m += m

            try:
                if len(re.findall('CONTENTS:\\s+', self.m)) > 0:
                    self.m = re.sub('SUCCESS.*\n', '', self.m)
                    self.m = re.sub('.*CONTENTS:\\s+', '', self.m)
            except:
                pass

        s.close()
        self.status = 1

    def get(self):
        return self.m

    def send(self, data):
        pass

    def receive(self, data):
        pass


class Record(object):

    def __init__(self):
        pass

    def generate(self):
        return uuid.uuid4().__str__()


class Profiler(object):

    def __init__(self, profiles, server_ip, server_port, ip, port, db, db_table):
        self.profiles = profiles
        self.server_ip = server_ip
        self.server_port = server_port
        self.ip = ip
        self.port = port
        self.db = db
        self.db_table = db_table
        self.o = Output()

    def run(self):
        client = Client(self.port, self.ip, dict(ip=self.server_ip, port=self.server_port))
        while True:
            now = int(time.time())
            for i in self.profiles:
                if not os.path.isdir(i['folder']):
                    continue
                size = str(Util().getFolderSize(i['folder']))
                name = 'N/A'
                if 'name' in i.keys():
                    name = i['name']
                c = self.db((self.db[self.db_table].name == name) & (self.db[self.db_table].folder == i['folder'])).count()
                if c > 0:
                    continue
                if int(i['time']) >= now:
                    uid = Record().generate()
                    bkp = Backup(uid, i['folder'])
                    bkp.run()
                    if bkp.status == 1:
                        self.db[self.db_table].insert(uid=uid, time=time.time(), folder=i['folder'], local=i['local'], name=name, size=size)
                        self.db.commit()
                        if i['local']:
                            self.o.show('Backup Ok -- Now saving to disk')
                            self.o.show('Local Backup has been successfully stored')
                        else:
                            fc = open(bkp.get(), 'r+').read()
                            client.run('BACKUP', i['folder'], uid, fc, name, size)
                            if client.status:
                                self.o.show('Backup Ok -- Now transferring to server')
                                fp = client.get()
                                if len(re.findall('SUCCESS', fp)) > 0:
                                    self.o.show('Remote Backup has been successfully transferred')
                                else:
                                    self.o.show('Something went wrong on the server.. couldnt back that folder. Reverting changes')
                    else:
                        continue


class Util(object):

    def unzip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as (zf):
            for member in zf.infolist():
                words = member.filename.split('/')
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''):
                        continue
                    path = os.path.join(path, word)

                zf.extract(member, os.path.relpath(path))

    def zip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as (zf):
            for member in zf.infolist():
                words = member.filename.split('/')
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''):
                        continue
                    path = os.path.join(path, word)

                zf.write(member, path)

    def getFolderSize(self, p):
        from functools import partial
        prepend = partial(os.path.join, p)
        return sum([ os.path.getsize(f) if os.path.isfile(f) else self.getFolderSize(f) for f in map(prepend, os.listdir(p)) ])


class Runtime(object):

    def __init__(self, a):
        self.db_name = ''
        self.db_pass = ''
        self.db_host = ''
        self.db_table = ''
        self.db_user = ''
        self._settings()
        self._profiles()
        self.propagate()
        self.uid = Record().generate()
        self.o = Output()
        self.type = 'CLIENT'
        self.help = 0
        self.clean = 0
        self.name = 'N/A'
        for _i in range(0, len(a)):
            i = a[_i]
            try:
                j = a[(_i + 1)]
            except:
                j = a[_i]

            if i in ('-c', '--client'):
                self.type = 'CLIENT'
            if i in ('-s', '--server'):
                self.type = 'SERVER'
            if i in ('-h', '--help'):
                self.help = True
            if i in ('-b', '--backup'):
                self.backup = True
            if i in ('-r', '--restore'):
                self.restore = True
            if i in ('-i', '--ip'):
                self.ip = j
            if i in ('-p', '--port'):
                self.port = j
            if i in ('-x', '--compress'):
                self.compress = True
            if i in ('-e', '--encrypt'):
                self.encrypt = True
            if i in ('-l', '--local'):
                self.local = True
            if i in ('-f', '--folder'):
                self.folder = j
            if i in ('-l', '--list'):
                self.list = True
            if i in ('-p', '--profiler'):
                self.profiler = True
            if i in ('-rm', '--remove'):
                self.remove = True
            if i in ('-n', '--name'):
                self.name = j
            if i in ('-cl', '--clean'):
                self.clean = True
            if i in ('-id', '--id'):
                self.id = j

        if self.help:
            self._help()
            return
        self.o.show(('Running in {0} mode').format(self.type))
        self.perform()

    def propagate(self):
        if self.db_family == 'mysql':
            self.db = DAL(self.db_family + '://' + self.db_user + ':' + self.db_pass + '@' + self.db_host + '/' + self.db_name, pool_size=1, migrate_enabled=False)
            self.db.executesql(('\n\t\t\tCREATE DATABASE IF NOT EXISTS {0};\n\t\t\t').format(self.db_name))
            self.db.executesql(('\n\t\t\tCREATE TABLE IF NOT EXISTS {0} (\n\t\t\t\t`id` int,\n\t\t\t\t`uid` varchar(255),\n\t\t\t\t`name` varchar(255),\n\t\t\t\t`time` varchar(255),\n\t\t\t\t`folder` varchar(255),\n\t\t\t\t`size` int,\n\t\t\t\t`local` varchar(255)\n\t\t\t); ').format(self.db_table))
        else:
            self.db = DAL('sqlite://storage.db')
        self.db.define_table(self.db_table, Field('id'), Field('uid'), Field('name'), Field('time'), Field('folder'), Field('size'), Field('local'), migrate=False)

    def perform(self):
        is_success = False
        if 'folder' in dir(self):
            self.size = Util().getFolderSize(self.folder)
        if 'profiler' in dir(self):
            profiler = Profiler(self.profiles, self.server_ip, self.server_port, self.ip, self.port, self.db, self.db_table).run()
        if 'local' not in dir(self):
            self.isLocal = False
            if self.type == 'CLIENT':
                client = Client(self.port, self.ip, dict(ip=self.server_ip, port=self.server_port))
                self.o.show(('Running on port: {0}, ip: {1}').format(self.server_port, self.server_ip))
            else:
                server = Server(self.server_port, self.server_ip, self.db, self.db_table)
                self.o.show(('Running on port: {0}, ip: {1}').format(self.server_port, self.server_ip))
                server.run()
        else:
            self.isLocal = True
        if 'backup' in dir(self):
            if 'folder' not in dir(self):
                pass
            else:
                self.o.show('Gathering files.. this can take awhile')
                bkp = Backup(self.uid, self.folder)
                bkp.run()
                if bkp.status == 1:
                    self.db[self.db_table].insert(uid=self.uid, time=time.time(), folder=self.folder, size=self.size, local=self.isLocal, name=self.name)
                    self.db.commit()
                    is_success = True
                    if self.isLocal:
                        self.o.show('Backup Ok -- Now saving to disk')
                        self.o.show('Local Backup has been successfully stored')
                        self.o.show('Transaction ID: ' + self.uid)
                    else:
                        fc = open(bkp.get(), 'r').read().decode('utf-8')
                        client.run('BACKUP', self.folder, self.uid, fc, self.name, self.size)
                        if client.status:
                            self.o.show('Backup Ok -- Now transferring to server')
                            fp = client.get()
                            if len(re.findall('SUCCESS', fp)) > 0:
                                self.o.show('Remote Backup has been successfully transferred')
                                self.o.show('Transaction ID: ' + self.uid)
                            else:
                                self.o.show('Something went wrong on the server.. couldnt back that folder. Reverting changes')
        if 'restore' in dir(self):
            if 'id' in dir(self):
                r = self.db(self.db[self.db_table].uid == self.id).select().first()
                if not r:
                    self.o.show('ERROR: Backup not found.')
                    return
                self.folder = r['folder']
                self.local = r['local']
                self.ruid = r['uid']
                if self.clean:
                    self.o.show('Cleaning directory..')
                if self.isLocal:
                    self.o.show('Restore Ok -- Now restoring compartment')
                    rst = Restore(False, self.folder, self.clean)
                    rst.run(True, self.ruid)
                    if rst.status:
                        self.o.show('Restore has been successfully performed')
                else:
                    self.o.show('Pinging server for restore..')
                    client.run('RESTORE', self.folder, self.ruid, '')
                    if client.status:
                        self.o.show('Restore Retrieval Ok -- now attempting to restore')
                        fp = open(LOCAL_BACKUP_DIR + self.ruid + '.zip', 'w+')
                        fp.write(client.get())
                        fp.close()
                        rst = Restore(LOCAL_BACKUP_DIR + self.ruid + '.zip', self.folder, self.clean)
                        rst.run(True, self.ruid)
                        if rst.status:
                            self.o.show('Restore Successful')
        if 'remove' in dir(self) and is_success:
            if 'folder' in dir(self):
                shutil.rmtree(self.folder)
                self.o.show('Directory successfully deleted..')
        if 'list' in dir(self):
            rows = self.db(self.db[self.db_table].time > 0).select().as_list()
            self.o.show('Full list of stored backups')
            for i in rows:
                print i

    def _help(self):
        print '\nusage: lback [options] required_input required_input2\noptions:\n-c, --client     Run a command as a client (required)\n-s, --server     Initiate a server (required)\n-b, --backup     Run a backup\n-r, --restore    Run a restore\n-f, --folder     Specify a folder (required *) for backups\n-i, --id         Specify an id (required *) for restores\n-n, --name       Name for backup (optional)\n-rm, --remove    Remove a directory on backup\n-x, --compress   Compress an archive (default)\n-l, --list       Generate a full list of your backups\n-i, --ip         Specify an ip (overridden by settings.json if found)\n-p, --port       Specify a port (overridden by settings.json if found)\n-h, --help       Print this text\n\t\t'

    def try_hard_to_find(self):
        pass

    def _settings(self):
        if os.path.isfile('./settings.json'):
            settings = json.loads(open('./settings.json').read())
        else:
            if os.path.isfile('../settings.json'):
                settings = json.loads(open('../settings.json').read())
            for i in settings.keys():
                setattr(self, i, settings[i])

        self.ip = settings['client_ip']
        self.port = settings['client_port']
        self.server_ip = settings['server_ip']
        self.server_port = settings['server_port']
        if 'db_family' not in settings.keys():
            self.db_family = 'mysql'
        else:
            self.db_family = settings['db_family']

    def _profiles(self):
        if os.path.isfile('./profiles.json'):
            self.profiles = json.loads(open('./profiles.json').read())
        elif os.path.isfile('../profiles.json'):
            self.profiles = json.loads(open('../profiles.json').read())


if __name__ == '__main__':
    r = Runtime(sys.argv)