# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jeju/executor/yaml.py
# Compiled at: 2016-11-09 20:33:52
import string, uuid, logging, jeju.do
exist_ruamel = True
try:
    import ruamel.yaml
    from ruamel.yaml.util import load_yaml_guess_indent
except ImportError:
    err_msg = '\n    ##################################################################\n    # ! Warning                                                      #\n    # rumal.yaml library does not exist                              #\n    # jeju *can not* execute yaml plugin!                            #\n    #                                                                #\n    # To install ruamel.yaml                                         #\n    # (RedHat, CentOS)                                               #\n    # yum install python-devel gcc                                   #\n    # pip install ruamel.yaml                                        #\n    #                                                                #\n    # (Debian, Ubuntu)                                               #\n    # apt-get install python-dev gcc                                 #\n    # pip install ruamel.yaml                                        #\n    ##################################################################\n    '
    print err_msg
    import time
    time.sleep(5)
    exist_ruamel = False

def replaceable(code, kv):
    keys = kv.keys()
    for key in keys:
        nkey = '${%s}' % key
        code = string.replace(code, nkey, kv[key])

    logging.debug('####################' + '\n%s' % code)
    logging.debug('####################')
    return code


def find_file_path(lookahead):
    print lookahead
    if lookahead == None:
        return
    else:
        ctx = lookahead['text']
        items = ctx.split()
        if items[0] == 'edit':
            return items[1]
        return


def execute_yaml(**kwargs):
    code = kwargs['code']
    kv = kwargs['kv']
    import os
    rcode = replaceable(code, kv)
    file_path = find_file_path(kwargs['lookahead'])
    if file_path == None:
        msg = "[DEBUG] I don't know how to edit!"
        print msg
        return msg
    else:
        if exist_ruamel == False:
            logging.error(err_msg)
            distro = jeju.do.detect_dist()
            os_ = distro['distname'].split(' ')[0].lower()
            if os_ == 'ubuntu' or os_ == 'debian':
                cmd = 'apt-get update;apt-get install -y gcc python-dev;pip install ruamel.yaml'
            elif os_ == 'centos' or os_ == 'redhat':
                cmd = 'yum install -y python-devel gcc;pip install ruamel.yaml'
            else:
                return {'input': rcode, 'output': '[ERROR] Install ruamel.yaml'}
            import os
            os.system(cmd)
        import ruamel.yaml
        from ruamel.yaml.util import load_yaml_guess_indent
        config, ind, bsi = load_yaml_guess_indent(open(file_path))
        config2, ind2, bsi2 = load_yaml_guess_indent(rcode)
        config.update(config2)
        ruamel.yaml.round_trip_dump(config, open(file_path, 'w'), indent=ind, block_seq_indent=bsi)
        return {'input': rcode, 'output': open(file_path, 'r').read()}