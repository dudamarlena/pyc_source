# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jeju/executor/editor.py
# Compiled at: 2016-11-09 20:33:52
import string, ConfigParser, io, logging

def replaceable(code, kv):
    keys = kv.keys()
    for key in keys:
        nkey = '${%s}' % key
        code = string.replace(code, nkey, kv[key])

    logging.debug('####################' + '\n%s' % code)
    logging.debug('####################')
    return code


def find_file_path(lookahead):
    if lookahead == None:
        return
    else:
        ctx = lookahead['text']
        items = ctx.split()
        if items[0] == 'edit':
            return items[1]
        return


def editor_text(**kwargs):
    lookahead = kwargs['lookahead']
    code = kwargs['code']
    kv = kwargs['kv']
    file_path = find_file_path(kwargs['lookahead'])
    if file_path == None:
        msg = 'Cannot find content:%s' % lookahead['text']
        logging.error(msg)
        return msg
    else:
        fp = open(file_path, 'w')
        rcode = replaceable(code, kv)
        fp.write(rcode)
        fp.close()
        return {'output': rcode}


def editor_ini(**kwargs):
    lookahead = kwargs['lookahead']
    code = kwargs['code']
    kv = kwargs['kv']
    added = ConfigParser.RawConfigParser(allow_no_value=True)
    rcode = replaceable(code, kv)
    added.readfp(io.BytesIO(rcode))
    file_path = find_file_path(kwargs['lookahead'])
    if file_path == None:
        msg = 'Cannot find content path: %s' % lookahead['text']
        logging.error(msg)
        return msg
    else:
        orig = ConfigParser.ConfigParser()
        orig.readfp(open(file_path))
        for section in added.sections():
            if orig.has_section(section) == False:
                msg = 'Add new section'
                logging.debug(msg)
                orig.add_section(section)
            for item, value in added.items(section):
                if item == '...':
                    msg = 'abbreviation'
                else:
                    orig.set(section, item, value)

        fp = open(file_path, 'w')
        orig.write(fp)
        new_content = orig.readfp(open(file_path))
        fp.close()
        return {'output': new_content}