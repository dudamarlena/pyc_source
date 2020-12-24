# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marx/venv3/lib/python3.6/site-packages/tsr/modules/general.py
# Compiled at: 2018-06-27 08:14:39
# Size of source mod 2**32: 10003 bytes
import datetime, json
from .os_info import path
import os.path
from dateutil.relativedelta import relativedelta
users = {}
username_colour_dict = {}
username_to_id = {}
users = json.load(open(os.path.join(path.settings, 'users.json')))
for entry in users:
    if 'colour' not in users[entry]:
        users[entry]['colour'] = 'end'

settings = json.load(open(os.path.join(path.settings, 'settings.json')))

def level_domain(level, domain):
    if not is_int(level):
        raise ValueError('level_domain(level_number, domain_string)')
    neglevel = -int(level)
    return '.'.join(domain.split('.')[neglevel:])


def dictfind(original_dict, **kwargs):
    """ eg
    >>>d={
        'foo':{
            'bar': 11,
            'bob': 'george',
        },
        'gimli':{
            'gandalf':{
                'frodo':5,
                'samwise':7,
            },
            'radagast':11,
        },
        'jones':{
            'gandalf':{
                'frodo':1,
                'samwise':2,
            },
            'radagast':3,
        },
    }
    >>>find(d, bar='>5')
    ['foo']
    >>>find(d, gandalf_frodo='>3')
    ['gimli']
    """
    ListOnlyKeys = True
    if '_ListOnlyKeys' in kwargs:
        ListOnlyKeys = kwargs['_ListOnlyKeys']
    d = dict(original_dict)
    for kw in kwargs:
        if kw[0] != '_':
            kw_value = kwargs[kw]
            kw_relation = None
            if kw_value[0] in ('*', '>', '<', '='):
                kw_relation = kw_value[0]
                kw_value = kw_value[1:]
            kw_relation_end = None
            if kw_value[(-1)] in ('*', ):
                kw_relation_end = kw_value[(-1)]
                kw_value = kw_value[:-1]
            new_d = {}
            key0 = None
            if '_' in kw:
                key0 = kw.split('_')[0]
                key1 = kw.split('_')[1]
                for key in d:
                    if key0 in d[key]:
                        if key1 in d[key][key0]:
                            this_value = d[key][key0][key1]
                            if kw_relation == '>':
                                kw_value = int(kw_value)
                                if this_value > kw_value:
                                    new_d[key] = d[key]
                                else:
                                    if kw_relation == '<':
                                        kw_value = int(kw_value)
                                        if this_value > kw_value:
                                            new_d[key] = d[key]
                                    elif kw_relation == '=' and this_value == kw_value:
                                        pass
                                new_d[key] = d[key]

            else:
                if kw_relation_end == '*':
                    kw_value = kw_value[:-1]
                    for key in d:
                        if key.startswith(kw_value):
                            new_d[key] = d[key]

                else:
                    if kw_relation == '*':
                        kw_value = kw_value
                        for key in d:
                            if key.endswith(kw_value):
                                new_d[key] = d[key]

                    else:
                        if kw_relation == '>':
                            kw_value = int(kw_value)
                            for key in d:
                                if d[key][kw] > kw_value:
                                    print(('       {}>{}'.format(d[key][kw], kw_value)), end='\r')
                                    new_d[key] = d[key]

                        else:
                            if kw_relation == '<':
                                kw_value = int(kw_value)
                                for key in d:
                                    if d[key][kw] < kw_value:
                                        new_d[key] = d[key]

                            else:
                                for key in d:
                                    if d[key][kw] == kw_value:
                                        new_d[key] = d[key]

            d = dict(new_d)

    if ListOnlyKeys:
        return [key for key in d]
    else:
        return d


def userid_colour(userid):
    if type(userid) != 'str':
        userid = str(userid)
    try:
        return users[userid]['colour']
    except:
        raise Exception('userid {0} has no colour. users[{0}] = {1}'.format(userid, users[userid]))


def make_n_char_long(x, n, spacing=' '):
    y = str(x)
    while len(y) < n:
        y += spacing

    if len(y) > n:
        y = y[:n]
    return y


def myjoin(*args):
    string = ''
    for arg in args:
        string += '  ' + str(arg)

    return string[2:]


def standardise_datetime(datestr):
    if isinstance(datestr, datetime.datetime):
        return datestr
    else:
        if isinstance(datestr, datetime.date):
            return datetime.datetime.combine(datestr, datetime.time(0, 0))
        try:
            return datetime.datetime.strptime(datestr, '%d-%m-%Y')
        except:
            try:
                return datetime.datetime.strptime(datestr, '%Y-%m-%d')
            except:
                datestr = datestr.strip().lower()
                if datestr == 'yesterday':
                    return datetime.datetime.now() - datetime.timedelta(days=1)
                if 'ago' in datestr:
                    date_ls = datestr.split(' ')
                    try:
                        n = int(date_ls[0])
                        formatIs_n_obj_ago = True
                    except:
                        formatIs_n_obj_ago = False

                    if formatIs_n_obj_ago:
                        date_type = date_ls[1]
                        if date_type in ('second', 'seconds'):
                            return datetime.datetime.now() - datetime.timedelta(seconds=n)
                        if date_type in ('minute', 'minutes'):
                            return datetime.datetime.now() - relativedelta(minutes=n)
                        if date_type in ('hour', 'hours'):
                            return datetime.datetime.now() - relativedelta(hours=n)
                        if date_type in ('day', 'days'):
                            return datetime.datetime.now() - datetime.timedelta(days=n)
                        if date_type in ('week', 'weeks'):
                            return datetime.datetime.now() - datetime.timedelta(days=(n * 7))
                        if date_type in ('month', 'months'):
                            return datetime.datetime.now() - relativedelta(months=n)
                        if date_type in ('year', 'years'):
                            return datetime.datetime.now() - relativedelta(years=n)
                        if date_type in ('decade', 'decades'):
                            return datetime.datetime.now() - relativedelta(years=(n * 10))
                else:
                    for char in ('T', ' ', '_'):
                        if len(datestr) > 18:
                            try:
                                try:
                                    datestr = datestr[:19]
                                    return datetime.datetime.strptime(datestr, '%Y-%m-%d' + char + '%H:%M:%S')
                                except:
                                    datestr = datestr[:19]
                                    return datetime.datetime.strptime(datestr, '%d-%m-%Y' + char + '%H:%M:%S')

                            except:
                                pass

                        try:
                            try:
                                return datetime.datetime.strptime(datestr, '%Y-%m-%d' + char + '%H:%M')
                            except:
                                return datetime.datetime.strptime(datestr, '%d-%m-%Y' + char + '%H:%M')

                        except:
                            pass

    raise Exception('Unknown datetime string: ' + str(datestr))


def standardise_datetime_str(datestr):
    return str(standardise_datetime(datestr))


def standardise_date(string):
    return standardise_datetime(string).date()


def standardise_date_str(datestr):
    return str(standardise_date(datestr))


def standardise_time(timestr):
    return datetime.datetime.strptime(timestr, '%H:%M').time()


def is_number(x):
    try:
        dummy = float(x)
        return True
    except:
        return False


def is_int(x):
    try:
        dummy = int(x)
        return True
    except:
        return False


def ls_rm_dupl(ls):
    l = []
    for x in ls:
        if x not in l:
            l.append(x)

    return l


def ls_in_str(ls, string):
    for element in ls:
        try:
            if element in string:
                return True
        except:
            pass

    return False


def mystrip(text):
    while '  ' in text:
        text = text.replace('  ', ' ')

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    while ' \n' in text:
        text = text.replace(' \n', '\n')

    while '\n ' in text:
        text = text.replace('\n ', '\n')

    while '\n> > ' in text:
        text = text.replace('\n> > ', '\n> ')

    while '>\n' in text:
        text = text.replace('>\n', '')

    while '~\n' in text:
        text = text.replace('~\n', '\n')

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    while '\r\n' in text:
        text = text.replace('\r\n', '\n')

    while '\n\r' in text:
        text = text.replace('\n\r', '\n')

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    return text.strip()