# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sli/f5-admin/src/util.py
# Compiled at: 2020-03-10 21:17:36
# Size of source mod 2**32: 3270 bytes
import re, socket, os

def is_directory(dir_name):
    return os.path.exists(dir_name) and os.path.isdir(dir_name)


def is_file(file_name):
    return os.path.isfile(file_name)


def file_to_list(file):
    comment_pattern = re.compile('^#|^\\s+#')
    my_list = []
    with open(file, 'r') as (f1):
        line = f1.readline().strip()
        while line:
            if comment_pattern.match(line):
                next
            else:
                my_list.append(line)
            line = f1.readline().strip()

    f1.close()
    return my_list


def list_to_file(list, file):
    try:
        with open(file, 'w') as (f1):
            for x in list:
                f1.write(x + '\n')

        f1.close()
        return True
    except Exception as e:
        try:
            print('Error: ', e)
            return False
        finally:
            e = None
            del e


def traverse(obj, prev_path='obj', path_repr='{}[{!r}]'.format):
    if isinstance(obj, dict):
        it = list(obj.items())
    else:
        if isinstance(obj, list):
            it = enumerate(obj)
        else:
            yield (
             prev_path, obj)
            return
    for k, v in it:
        for data in traverse(v, path_repr(prev_path, k), path_repr):
            yield data


def host_to_ips(hostname):
    ip_list = []
    try:
        ais = socket.getaddrinfo(hostname, None)
        for result in ais:
            ip_list.append(result[(-1)][0])

        return ip_list
    except Exception as e:
        try:
            print('Error: ', e, 'Unable to resolve hostname: ', hostname)
            return
        finally:
            e = None
            del e


def is_valid_hostname(hostname):
    ips = host_to_ips(hostname)
    if ips == None:
        return False
    if len(ips) > 0:
        return True
    return False


def set_credential_1(id, *args):
    if args:
        if id:
            credential = {'user_name':str(id).strip(),  'user_pass':' '.join(args)}
        else:
            credential = {'user_name':'root',  'user_pass':' '.join(args)}
    return credential


def set_credential_2(id):
    if id:
        credential = {'user_name':str(id).strip(),  'user_pass':None}
    else:
        credential = None
    return credential