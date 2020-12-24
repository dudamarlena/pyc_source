# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fdfs_client/fdfs_test.py
# Compiled at: 2018-11-05 04:52:27
# Size of source mod 2**32: 13799 bytes
import os, sys, time
try:
    from fdfs_client.client import *
    from fdfs_client.exceptions import *
except ImportError:
    import_path = os.path.abspath('../')
    sys.path.append(import_path)
    from fdfs_client.client import *
    from fdfs_client.exceptions import *

def usage():
    s = 'Usage: python fdfs_test.py {options} [{local_filename} [{remote_file_id}]]\n'
    s += 'options: upfile, upbuffer, downfile, downbuffer, delete, listgroup, listserv\n'
    s += '         upslavefile, upslavebuffer, upappendfile, upappendbuffer\n'
    s += '\tupfile {local_filename}\n'
    s += '\tupbuffer {local_filename}\n'
    s += '\tdownfile {local_filename} {remote_file_id}\n'
    s += '\tdownbuffer {remote_file_id}\n'
    s += '\tdelete {remote_file_id}\n'
    s += '\tlistgroup {group_name}\n'
    s += '\tlistall \n'
    s += '\tlistsrv {group_name} [storage_ip]\n'
    s += '\tsetmeta {remote_file_id}\n'
    s += '\tgetmeta {remote_file_id}\n'
    s += '\tupslavefile {local_filename} {remote_fileid} {prefix_name}\n'
    s += '\tupappendfile {local_filename}\n'
    s += '\ttruncate {truncate_filesize} {remote_fileid}\n'
    s += '\tmodifyfile {local_filename} {remote_fileid} {file_offset}\n'
    s += '\tmodifybuffer {local_filename} {remote_fileid} {file_offset}\n'
    s += 'e.g.: python fdfs_test.py upfile test'
    print(s)
    sys.exit(0)


if len(sys.argv) < 2:
    usage()
client = Fdfs_client('client.conf')

def upfile_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        local_filename = sys.argv[2]
        file_size = os.stat(local_filename).st_size
        meta_dict = {'ext_name':'py', 
         'file_size':str(file_size) + 'B'}
        t1 = time.time()
        ret_dict = client.upload_by_filename(local_filename, meta_dict)
        t2 = time.time()
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

        print('[+] time consume: %fs' % (t2 - t1))
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upfileex_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        local_filename = sys.argv[2]
        t1 = time.time()
        ret_dict = client.upload_by_file(local_filename)
        t2 = time.time()
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

        print('[+] time consume: %fs' % (t2 - t1))
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upslavefile_func():
    if len(sys.argv) < 5:
        usage()
        return
    try:
        local_filename = sys.argv[2]
        remote_fileid = sys.argv[3]
        prefix_name = sys.argv[4]
        ret_dict = client.upload_slave_by_file(local_filename, remote_fileid, prefix_name)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upslavebuffer_func():
    if len(sys.argv) < 5:
        usage()
        return
    try:
        local_filename = sys.argv[2]
        remote_fileid = sys.argv[3]
        prefix_name = sys.argv[4]
        with open(local_filename, 'rb') as (f):
            filebuffer = f.read()
            ret_dict = client.upload_slave_by_buffer(local_filename, remote_fileid, prefix_name)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def del_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        remote_file_id = sys.argv[2]
        ret_tuple = client.delete_file(remote_file_id)
        print('[+] %s' % ret_tuple[0])
        print('[+] remote_fileid: %s' % ret_tuple[1])
        print('[+] Storage IP: %s' % ret_tuple[2])
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def downfile_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        local_filename = sys.argv[2]
        remote_fileid = sys.argv[3]
        ret_dict = client.download_to_file(local_filename, remote_fileid)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def list_group_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        group_name = sys.argv[2]
        ret = client.list_one_group(group_name)
        print(ret)
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def listall_func():
    if len(sys.argv) < 2:
        usage()
        return
    try:
        ret_dict = client.list_all_groups()
        print('=' * 80)
        print('Groups count:', ret_dict['Groups count'])
        for li in ret_dict['Groups']:
            print('-' * 80)
            print(li)
            print('-' * 80)

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def list_server_func():
    if len(sys.argv) < 3:
        usage()
        return
    try:
        group_name = sys.argv[2]
        if len(sys.argv) > 3:
            storage_ip = sys.argv[3]
        else:
            storage_ip = None
        ret_dict = client.list_servers(group_name, storage_ip)
        print('=' * 80)
        print('Group name: %s' % ret_dict['Group name'])
        print('=' * 80)
        i = 1
        for serv in ret_dict['Servers']:
            print('Storage server %d:' % i)
            print('=' * 80)
            print(serv)
            i += 1
            print('=' * 80)

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upbuffer_func():
    if len(sys.argv) < 3:
        usage()
        return
    else:
        local_filename = sys.argv[2]
        if len(sys.argv) > 3:
            ext_name = sys.argv[3]
        else:
            ext_name = None
    meta_buffer = {'ext_name':'gif',  'width':'150px', 
     'height':'80px'}
    try:
        with open(local_filename, 'rb') as (f):
            file_buffer = f.read()
            ret_dict = client.upload_by_buffer(file_buffer, ext_name, meta_buffer)
            for key in ret_dict:
                print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def downbuffer_func():
    if len(sys.argv) < 3:
        usage()
        return
    remote_fileid = sys.argv[2]
    try:
        ret_dict = client.download_to_buffer(remote_fileid)
        print('Downloaded content:')
        print(ret_dict['Content'])
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def get_meta_data_func():
    if len(sys.argv) < 3:
        usage()
        return
    remote_fileid = sys.argv[2]
    try:
        ret_dict = client.get_meta_data(remote_fileid)
        print(ret_dict)
    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def set_meta_data_func():
    if len(sys.argv) < 3:
        usage()
        return
    remote_fileid = sys.argv[2]
    meta_dict = {'ext_name':'jgp', 
     'width':'160px', 
     'hight':'80px'}
    try:
        ret_dict = client.set_meta_data(remote_fileid, meta_dict)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upappendfile_func():
    if len(sys.argv) < 3:
        usage()
        return
    local_filename = sys.argv[2]
    try:
        ret_dict = client.upload_appender_by_file(local_filename)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def upappendbuffer_func():
    if len(sys.argv) < 3:
        usage()
        return
    local_filename = sys.argv[2]
    try:
        with open(local_filename, 'rb') as (f):
            file_buffer = f.read()
            ret_dict = client.upload_appender_by_buffer(file_buffer)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def appendfile_func():
    if len(sys.argv) < 4:
        usage()
        return
    local_filename = sys.argv[2]
    remote_fileid = sys.argv[3]
    try:
        ret_dict = client.append_by_file(local_filename, remote_fileid)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def appendbuffer_func():
    if len(sys.argv) < 4:
        usage()
        return
    local_filename = sys.argv[2]
    remote_fileid = sys.argv[3]
    try:
        with open(local_filename, 'rb') as (f):
            filebuffer = f.read()
            ret_dict = client.append_by_buffer(filebuffer, remote_fileid)
            for key in ret_dict:
                print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def truncate_func():
    if len(sys.argv) < 4:
        usage()
        return
    truncate_filesize = sys.argv[2]
    remote_fileid = sys.argv[3]
    try:
        ret_dict = client.truncate_file(truncate_filesize, remote_fileid)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def modifyfile_func():
    if len(sys.argv) < 4:
        usage()
        return
    else:
        local_filename = sys.argv[2]
        remote_fileid = sys.argv[3]
        if len(sys.argv) > 4:
            file_offset = sys.argv[4]
        else:
            file_offset = 0
    try:
        ret_dict = client.modify_by_filename(local_filename, remote_fileid, file_offset)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


def modifybuffer_func():
    if len(sys.argv) < 4:
        usage()
        return
    else:
        local_filename = sys.argv[2]
        remote_fileid = sys.argv[3]
        if len(sys.argv) > 4:
            file_offset = sys.argv[4]
        else:
            file_offset = 0
    try:
        with open(local_filename, 'rb') as (f):
            filebuffer = f.read()
        ret_dict = client.modify_by_buffer(filebuffer, remote_fileid, file_offset)
        for key in ret_dict:
            print('[+] %s : %s' % (key, ret_dict[key]))

    except (ConnectionError, ResponseError, DataError) as e:
        print(e)


result = {'upfile':lambda : upfile_func(), 
 'upfileex':lambda : upfileex_func(), 
 'upbuffer':lambda : upbuffer_func(), 
 'delete':lambda : del_func(), 
 'downfile':lambda : downfile_func(), 
 'downbuffer':lambda : downbuffer_func(), 
 'listgroup':lambda : list_group_func(), 
 'listall':lambda : listall_func(), 
 'listsrv':lambda : list_server_func(), 
 'getmeta':lambda : get_meta_data_func(), 
 'setmeta':lambda : set_meta_data_func(), 
 'upslavefile':lambda : upslavefile_func(), 
 'upappendfile':lambda : upappendfile_func(), 
 'upappendbuffer':lambda : upappendbuffer_func(), 
 'appendfile':lambda : appendfile_func(), 
 'appendbuffer':lambda : appendbuffer_func(), 
 'truncate':lambda : truncate_func(), 
 'modifyfile':lambda : modifyfile_func(), 
 'modifybuffer':lambda : modifybuffer_func(), 
 '-h':lambda : usage()}[sys.argv[1].lower()]()