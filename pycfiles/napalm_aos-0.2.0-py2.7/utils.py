# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/napalm_aos/utils/utils.py
# Compiled at: 2019-06-13 23:53:04
import re, ntpath, difflib, socket, struct, logging, inspect, os

def to_seconds(time_format):
    seconds = minutes = hours = days = weeks = 0
    days_match = re.match('(\\d+)( days|d)', time_format)
    hours_match = re.match('(\\d+)( hours|h)', time_format)
    minutes_match = re.match('(\\d+)( minutes|m)', time_format)
    seconds_match = re.match('(\\d+)( seconds|s)', time_format)
    if days_match:
        days = int(days_match.groups()[0])
    if hours_match:
        hours = int(hours_match.groups()[0])
    if minutes_match:
        minutes = int(minutes_match.groups()[0])
    if seconds_match:
        seconds = int(seconds_match.groups()[0])
    if minutes + hours + seconds + days + weeks == 0:
        hms_match = re.match('.*(\\d+):(\\d+):(\\d+)', time_format)
        if hms_match:
            hours = int(hms_match.groups()[0])
            minutes = int(hms_match.groups()[1])
            seconds = int(hms_match.groups()[2])
    seconds += minutes * 60
    seconds += hours * 3600
    seconds += days * 86400
    return seconds


def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', 4294967296 - (1 << host_bits)))
    return (network, netmask)


def format_white_space(string):
    temp = re.sub(' +', ' ', string)
    temp = re.sub('\n ', '\n', temp)
    temp = re.sub(' \n', '\n', temp)
    return temp.strip()


def format_white_space_for_file(filename):
    new_config = ''
    if filename and os.path.exists(filename) is True:
        with open(filename) as (f):
            new_config = f.read()
        with open(filename, 'w') as (f):
            f.write(format_white_space(new_config))


class AOSTable:

    def __init__(self, stdin):
        self.table = self.__table2dict(stdin)

    def isEmpty(self):
        if len(self.table) == 0:
            return True
        return False

    def __table2dict(self, stdin):
        result = {}
        try:
            start, end = (0, -1)
            arr_tbl = stdin.splitlines()
            for idx, value in enumerate(arr_tbl):
                if '-+-' in value:
                    start = idx
                if value == '' and idx > start and start != 0:
                    end = idx
                    break

            if end != -1:
                arr_tbl = arr_tbl[:end]
            col_str = arr_tbl[start]
            colunms = col_str.split('+')
            col_header = arr_tbl[(start - 1)]
            for line, value in enumerate(arr_tbl):
                idx = 0
                for col_num, colunm in enumerate(colunms):
                    col_name = col_header[idx:idx + len(colunm)].strip()
                    if line < start:
                        result[(col_name, col_num)] = []
                    elif line > start:
                        col_val = value[idx:idx + len(colunm)].strip()
                        result[(col_name, col_num)].append(col_val)
                    idx = idx + len(colunm) + 1

        except Exception as e:
            logging.debug('Got exception on parse output table.', exc_info=True)

        return result

    def get_column_by_name(self, column_name):
        for key in self.table.keys():
            if key[0] == column_name:
                return self.table[key]

        return []

    def get_column_by_index(self, index):
        for key in self.table.keys():
            if key[1] == index:
                return self.table[key]

        return []

    def get_id_by_value(self, index, value):
        column = self.get_column_by_index(index)
        for cid, val in enumerate(column):
            if value in val:
                return cid

        return -1


def ttree_to_json(ttree, level=0):
    result = {}
    for i in range(0, len(ttree)):
        cn = ttree[i]
        try:
            nn = ttree[(i + 1)]
        except Exception:
            nn = {'level': -1}

        if cn['level'] > level:
            continue
        if cn['level'] < level:
            return result
        if nn['level'] == level:
            dict_insert_or_append(result, cn['name'], cn['value'])
        elif nn['level'] > level:
            rr = ttree_to_json(ttree[i + 1:], level=nn['level'])
            dict_insert_or_append(result, cn['name'], rr)
        else:
            dict_insert_or_append(result, cn['name'], cn['value'])
            return result

    return result


def dict_insert_or_append(adict, key, val):
    """Insert a value in dict at key if one does not exist
    Otherwise, convert value to list and append
    """
    if key in adict:
        if type(adict[key]) != list:
            adict[key] = [
             adict[key]]
        adict[key].append(val)
    else:
        adict[key] = val


def parse_block(string, indent=' ', delimiter=':', reverse_delimiter=False):
    """
    Parse
        person:
        address:
            street1: 12 Bar St
            street2:
            city: Madison
            state: WI
            zip: 55555
        web:
            email: foo@bar.com
    to dict
        {'person': {'web':
            {'email': ' foo@bar.com'},
            'address': {'street1': ' 12 Bar St', 'street2': ' ', 'state': ' WI', 'zip': ' 55555', 'city': ' Madison'}}}
    """
    fout = []
    string = string.strip()
    arr_str = string.splitlines()
    for line in arr_str:
        try:
            key, value = (reverse_delimiter or line.split)(delimiter, 1) if 1 else line.rsplit(delimiter, 1)
            level = len(key) - len(key.lstrip(indent))
            prop = {'name': key.strip(), 'value': value, 'level': level}
            fout.append(prop)
        except Exception as e:
            logging.debug('Got exception on parse output block.', exc_info=True)

    return ttree_to_json(fout)


def jprint(stdin):
    import json
    print json.dumps(stdin, indent=4)


def compare_configure(conf1, conf2, mod='+-'):
    result = []
    diff = difflib.ndiff(conf1.splitlines(), conf2.splitlines())
    diff_lst = list(diff)
    mode = '[\\+-]'
    if mod == '+':
        mode = '[\\+]'
    if mod == '-':
        mode = '[\\-]'
    for line in diff_lst:
        if re.match(mode + '?\\s+?(!.+:.*)', line):
            line = re.sub(mode, '', line, 1)
            if not result or re.match(mode + '\\s[^!]+', result[(-1)]):
                result.append(line)
            else:
                result[-1] = line
        if re.match(mode + '\\s[^!]+', line):
            result.append(line)

    if result != [] and re.match(mode + '?\\s+?(!.+:.*)', result[(-1)]):
        result = result[:-1]
    return result


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def str_filter(astr):
    return re.sub('[,\\s]', '', astr)


def get_dec_num(astr, ttype):
    try:
        f_list = re.findall('.*?([-+]?[0-9]+\\.?[0-9]*)', astr)
        if f_list:
            return ttype(f_list[0])
        return astr
    except ValueError:
        return astr


def dbgMsg(message='entering function'):
    """Automatically log the current function details."""
    func = inspect.currentframe().f_back.f_code
    logging.debug('%s: %s in %s:%i' % (
     message,
     func.co_name,
     func.co_filename,
     func.co_firstlineno))