# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shinsheel/Documents/Data-Gathering/Pypi/anarcute/anarcute/lib.hy
# Compiled at: 2019-09-03 05:21:27
# Size of source mod 2**32: 11762 bytes
import hy.macros
from hy import HyExpression, HyInteger, HyList, HyString, HySymbol
from hy.core.language import butlast, distinct, first, last, name
from hy.core.shadow import hyx_Xplus_signX
import os, csv, json, time, sys
hy.macros.require('hy.extra.anaphoric', None, assignments='ALL', prefix='')
import hy.contrib.walk as walk
import multiprocessing_on_dill as mp, hy
hy.macros.tag('r')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('&rest')] + [HySymbol('rest')] + [HySymbol('&kwargs')] + [HySymbol('kwargs')])] + [HyExpression([] + [f] + [HyExpression([] + [HySymbol('unpack-iterable')] + [HyExpression([] + [HySymbol('reversed')] + [HySymbol('rest')])])] + [HyExpression([] + [HySymbol('unpack-mapping')] + [HySymbol('kwargs')])])]))

def list_dict(arr, key):
    return dict(zip(list(map(lambda x: x[key], arr)), arr))


import hy
hy.macros.macro('get-o')(lambda hyx_XampersandXname, *args: HyExpression([] + [HySymbol('try')] + [HyExpression([] + [HySymbol('get')] + list(butlast(args) or []))] + [HyExpression([] + [HySymbol('except')] + [HyList([] + [HySymbol('Exception')])] + [last(args)])]))
import hy
hy.macros.tag('try')(lambda expr: HyExpression([] + [HySymbol('try')] + [expr] + [HyExpression([] + [HySymbol('except')] + [HyList([] + [HySymbol('Exception')])] + [HyString('')])]))

def apply_mask(obj, mask):
    for k, v in obj.items():
        if k in mask:
            obj[k] = mask[k](v)
            _hy_anon_var_2 = None
        else:
            _hy_anon_var_2 = None

    return obj


enmask = apply_mask
import hy
hy.macros.macro('print-n-pass')(lambda hyx_XampersandXname, x: HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol('print')] + [x])] + [x]))

def route(obj, direction=None):
    if direction:
        direction = direction
    else:
        try:
            _hy_anon_var_4 = sys.argv[1]
        except Exception:
            _hy_anon_var_4 = None

        direction = _hy_anon_var_4
    if direction in obj:
        return (obj[direction])(*sys.argv[slice(2, None)])
    return None


def enroute(*args):
    compiler = 'hy' if first(sys.argv).endswith('.hy') else 'python3'
    cmd = '{} {} {}'.format(compiler, first(sys.argv), ' '.join(list(map(lambda x: json.dumps(x), args))))
    return os.popen(cmd)


def avg(*args):
    if len(args):
        return hyx_Xplus_signX(*(0, 0), *args) / len(args)
    return 0


def roll_avg(*args):
    if not args:
        return 0
    if 1 == len(args):
        return roll_avg(*first(args)) if type(first(args)) in [list, tuple] else first(args)
    return 0.8 * roll_avg(first(split_arr(args, 0.8, from_end=True))) + 0.2 * roll_avg(last(split_arr(args, 0.8, from_end=True)))


def photo_finish_fn(f):
    start = time.time()
    res = f()
    return (time.time() - res,)


import hy
hy.macros.macro('photo-finish')(lambda hyx_XampersandXname, *args: HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol('setv')] + [HySymbol('start')] + [HyExpression([] + [HySymbol('time.time')])])] + list(args or []) + [
 HyExpression([] + [HySymbol('-')] + [HyExpression([] + [HySymbol('time.time')])] + [HySymbol('start')])]))
import hy
hy.macros.macro('do-not-faster-than')(lambda hyx_XampersandXname, t, *args: HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol('setv')] + [HySymbol('start')] + [HyExpression([] + [HySymbol('time.time')])])] + list(args or []) + [
 HyExpression([] + [HySymbol('setv')] + [HySymbol('delta')] + [HyExpression([] + [HySymbol('-')] + [HyExpression([] + [HySymbol('time.time')])] + [HySymbol('start')])])] + [
 HyExpression([] + [HySymbol('if')] + [HyExpression([] + [HySymbol('<')] + [HyInteger(0)] + [HySymbol('delta')])] + [HyExpression([] + [HySymbol('time.sleep')] + [HyExpression([] + [HySymbol('min')] + [HySymbol('delta')] + [t])])])]))

def timeit(method):

    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        if 'log_time' in kwargs:
            name = kw.get('log_name', method.__name__.upper())
            kwargs['log_time']['name'] = int(1000 * (te - ts))
            _hy_anon_var_11 = None
        else:
            _hy_anon_var_11 = print('%r %2.2f ms' % (method.__name__, 1000 * (te - ts)))
        return result

    return timed


import hy
hy.macros.macro('car')(lambda hyx_XampersandXname, arr: HyExpression([] + [HySymbol('get')] + [arr] + [HyInteger(0)]))
import hy
hy.macros.macro('cdr')(lambda hyx_XampersandXname, arr: HyExpression([] + [HySymbol('get')] + [arr] + [HyExpression([] + [HySymbol('slice')] + [HyInteger(1)] + [HySymbol('None')])]))
import hy
hy.macros.macro('defun')(lambda hyx_XampersandXname, *args: HyExpression([] + [HySymbol('defn')] + list(args or [])))
import hy
hy.macros.macro('setf')(lambda hyx_XampersandXname, *args: HyExpression([] + [HySymbol('setv')] + list(args or [])))
import hy
hy.macros.macro('eql')(lambda hyx_XampersandXname, *args: HyExpression([] + [HySymbol('=')] + list(list(map(repr, args)) or [])))
HyExpression([] + [HySymbol('setv')] + [HySymbol('T')] + [HySymbol('True')] + [
 HySymbol('F')] + [HySymbol('False')] + [
 HySymbol('N')] + [HySymbol('None')] + [
 HySymbol('s')] + [HySymbol('setv')] + [
 HySymbol('c')] + [HySymbol('cond')] + [
 HySymbol('df')] + [HySymbol('defn')] + [
 HySymbol('ds')] + [HySymbol('defseq')])

def in_or(needles, haystack):
    for n in needles:
        if n in haystack:
            return True
        _hy_anon_var_14 = None

    return False


def is_if(a, b):
    if a:
        return a
    return b


def mapp(f, arr, processes=None):
    processes = processes if processes else mp.cpu_count()
    return mp.Pool(processes).map(f, arr)


def filterp(f, arr, processes=None):
    verdict = mapp(f, arr, processes)
    return mapp(last, list(filter(lambda iv: verdict[first(iv)], enumerate(arr))))


import hy
hy.macros.tag('mapp')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [HyExpression([] + [HySymbol('mapp')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('filterp')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [HyExpression([] + [HySymbol('filterp')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('map')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [HyExpression([] + [HySymbol('map')] + [f] + [HySymbol('arr')])])]))
import hy
hy.macros.tag('filter')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [HyExpression([] + [HySymbol('filter')] + [f] + [HySymbol('arr')])])]))

def filter_or_keep(arr, f):
    filtered = list(filter(f, arr))
    if filtered:
        return filtered
    return arr


def r_filter(is_condition, item, key=None):
    res = []
    res.append(item) if is_condition(item) else None
    if type(item) in [list, tuple]:
        for elem in item:
            r = r_filter(is_condition, elem)
            if r:
                res += r
                _hy_anon_var_20 = None
            else:
                _hy_anon_var_20 = None

        _hy_anon_var_23 = None
    else:
        if type(item) in [dict]:
            for k, v in item.items():
                r = r_filter(is_condition, v, key=k)
                if r:
                    res += r
                    _hy_anon_var_21 = None
                else:
                    _hy_anon_var_21 = None

            _hy_anon_var_22 = None
        else:
            _hy_anon_var_22 = None
        _hy_anon_var_23 = _hy_anon_var_22
    return res


import hy
hy.macros.tag('r-filter')(lambda f: HyExpression([] + [HySymbol('fn')] + [HyList([] + [HySymbol('arr')])] + [HyExpression([] + [HySymbol('list')] + [HyExpression([] + [HySymbol('r-filter')] + [f] + [HySymbol('arr')])])]))

def apply(f, *args, **kwargs):
    return f(*args, **kwargs)


def run(f, args=[], daemon=None):
    p = mp.Process(target=f, args=args, daemon=daemon)
    p.start()
    return p


def load_csv(fname, key=None, delimiter=','):
    if os.path.isfile(fname):
        it = list(csv.DictReader((open(fname, 'r+')), delimiter=delimiter))
        it = map(dict, it)
        arr = list(it)
    else:
        arr = []
    arr = list(map(dict, arr))
    if key:
        obj = {}
        for row in arr:
            obj[row[key]] = row

        _hy_anon_var_28 = obj
    else:
        _hy_anon_var_28 = arr
    return _hy_anon_var_28


def tolist(*args):
    return [
     *args]


def fieldnames(arr):
    return list(set(hyx_Xplus_signX([], *[[]] + list(map(lambda x: list(x.keys()), arr)))))


hyx_XasteriskXfieldnamesXasteriskX = fieldnames

def write_csv(fname, arr, id=None, fieldnames=None):
    writer = csv.DictWriter((open(fname, 'w+')), fieldnames=(fieldnames if fieldnames else hyx_XasteriskXfieldnamesXasteriskX(arr)))
    writer.writeheader()
    for row in arr:
        writer.writerow(row)


def write_csv_add(fname, arr, **kwargs):
    it = fname
    it = load_csv(it)
    it = list(it) + list(arr)
    it = write_csv(fname, it, **kwargs)
    return it


def write_txt(name, txt):
    return open(name, 'w+').write(txt)


def write_txt_add(name, txt):
    return open(name, 'a+').write(txt)


def read_txt(name):
    return open(name, 'r+').read()


load_txt = read_txt

def load_json(fname):
    return json.load(open(fname, 'r+'))


def write_json(fname, obj):
    return open(fname, 'w+').write(json.dumps(obj))


def pretty(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def jsonl_json(jstr):
    it = jstr
    it = it.split('\n')
    it = lambda arr: list(filter(thru, arr))(it)
    it = ','.join(it)
    it = '[{}]'.format(it)
    return it


def jsonl_loads(jstr):
    return json.loads(jsonl_json(jstr))


def jsonl_load(f):
    return jsonl_loads(f.read())


def jsonl_dumps(arr):
    return '\n'.join(list(map(json.dumps, arr)))


def jsonl_add(fname, item):
    return open(fname, 'a+').write('{}\n'.format(json.dumps(item)))


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def from_between(hyx_from, a, b):
    return first(last(hyx_from.split(a)).split(b))


between = from_between

def replace(s, obj):
    for k, v in obj.items():
        s = s.replace(k, v)

    return s


def trim(s):
    s = s.replace('\r\n', '\n').replace('\n', ' ')
    while s.endswith(' '):
        s = s[slice(0, -1)]

    while s.startswith(' '):
        s = s[slice(1, None)]

    while '  ' in s:
        s = s.replace('  ', ' ')

    return s


def ascii(s, mode='replace'):
    return s.encode('ascii', mode).decode('ascii')


def leave_only(s, approved):
    res = ''
    for c in s:
        if c in approved:
            res = res + c
            _hy_anon_var_49 = None
        else:
            _hy_anon_var_49 = None

    return res


def dehydrate(s):
    return leave_only(ascii(trim(s)).lower(), 'qwertyuiopasdfghjklzxcvbnm')


def escape(s):
    return lambda hyx_Xpercent_signX1:     if '"' in hyx_Xpercent_signX1:
'"{}"'.format() # Avoid dead code: hyx_Xpercent_signX1(s.replace('"', '\\"'))


def only_pcze(s):
    permitted = '1234567890 qwertyuiopasdfghjklzxcvbnm.:;/-\\?!'
    permitted = permitted + 'ąćęłńóśźż'
    permitted = permitted + permitted.upper()
    it = s
    it = list(it)
    it = filter(lambda c: c in permitted, it)
    it = list(it)
    it = ''.join(it)
    return it


def remove_control(s):
    return re.sub("r'\\p{C}'", '', s)


def json_quotes_single_to_double(j):
    return replace(j, {"{'":'{"',  "':":'":',  ", '":', "',  ": '":': "',  "'}":'"}',  "',":'",',  "']":'"]',  "['":'["'})


json_q_qq = json_quotes_single_to_double

def start_same(a, b):
    limit = min(len(str(a)), len(str(b)))
    return str(a)[slice(0, limit)] == str(b)[slice(0, limit)]


def short_ean(ean):
    if str(ean).replace('.', '').isdigit():
        ean = round(float(ean))
        while 0 == ean % 10:
            ean = ean / 10

        _hy_anon_var_57 = int(ean)
    else:
        _hy_anon_var_57 = ean
    return _hy_anon_var_57


def same_ean(a, b):
    return start_same(short_ean(a), short_ean(b))


def split_arr(arr, rate=2, from_end=False):
    if from_end:
        _hy_anon_var_62 = lambda arr: list(map(lambda x: list(reversed(x)), arr))(split_arr(list(reversed(arr)), rate))
    else:
        if 0 == len(arr):
            _hy_anon_var_61 = [[], []]
        else:
            if 1 == len(arr):
                _hy_anon_var_60 = [
                 [
                  first(arr)], []]
            else:
                part = int(len(arr) * rate)
                _hy_anon_var_60 = [arr[slice(0, part)], arr[slice(part, None)]]
            _hy_anon_var_61 = _hy_anon_var_60
        _hy_anon_var_62 = _hy_anon_var_61
    return _hy_anon_var_62


def get_mass(obj, fields):
    res = {}
    for field in fields:
        if field in obj:
            res[field] = obj[field]
            _hy_anon_var_64 = None
        else:
            _hy_anon_var_64 = None

    return res


def select(arr, fields):
    return list(map(lambda obj: get_mass(obj, fields), arr))


def first_that(arr, f):
    for elem in arr:
        if f(elem):
            return elem
        _hy_anon_var_67 = None

    return None


import hy
hy.macros.macro('last-that')(lambda hyx_XampersandXname, arr, f: HyExpression([] + [HySymbol('first-that')] + [HyExpression([] + [HySymbol('reversed')] + [arr])] + [f]))

def distinct(arr, f):
    res = {}
    for row in arr:
        res[f(row)] = row

    return res


def get_as(what, structure):
    obj = {}
    for k, v in structure.items():
        obj[k] = what[v]

    return obj


def sum_by(arr, key):
    sum = 0
    for row in arr:
        sum += key(row)

    return sum


def pareto(data, coeff, key):
    data = sorted(data, key=key, reverse=True)
    total = sum_by(data, key)
    for i in range(1, len(data)):
        sub_data = data[slice(0, i)]
        sub_total = sum_by(sub_data, key)
        if sub_total > coeff * total:
            return sub_data
        _hy_anon_var_72 = None

    return


def unique(arr, key=None):
    if key:
        obj = {}
        for elem in arr:
            obj[key(elem)] = elem

        _hy_anon_var_74 = obj.values()
    else:
        _hy_anon_var_74 = list(set(arr))
    return _hy_anon_var_74


def thru(x):
    return x


def condense(obj, key=thru, value=thru, operator=hyx_Xplus_signX):
    if obj:
        condense_res = {}
        for k, v in obj.items():
            k = key(k)
            v = value(v)
            if k in condense_res:
                condense_res[k] = operator(condense_res[k], v)
                _hy_anon_var_77 = None
            else:
                condense_res[k] = v
                _hy_anon_var_77 = None

        _hy_anon_var_78 = condense_res
    else:
        _hy_anon_var_78 = {}
    return _hy_anon_var_78


group = condense

def apply_to_chunks(f, arr, size, process=thru):
    """rework it - [[] []]"""
    buffer = []
    results = []
    while arr:
        buffer.append(arr.pop())
        if not len(buffer) >= size:
            arr or results.append(f(buffer))
            buffer = []
            _hy_anon_var_80 = None
        else:
            _hy_anon_var_80 = None

    return process(results)


def col(arr, c):
    return list(map(lambda x: x[c], arr))


def cols(arr, cs):
    return list(map(lambda x: list(map(lambda c: x[c], cs)), arr))


import hy
hy.macros.tag('whatever')(lambda expr: HyExpression([] + [HySymbol('do')] + [expr] + [HySymbol('True')]))