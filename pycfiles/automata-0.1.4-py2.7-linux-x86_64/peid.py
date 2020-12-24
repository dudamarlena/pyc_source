# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/automata/peid.py
# Compiled at: 2012-12-20 01:24:56
import re, logging, random
from automata import NFA

class dotini(list):
    """the worst .ini file "parser" ever"""
    section = re.compile('^\\[(.*)\\]')
    item = re.compile('\\s*(\\w+)\\s*=\\s*(.*)$')
    comment = re.compile(';.*$')

    def __init__(self):
        self.state = {'name': ''}

    def read(self, filename):
        input = file(filename, 'rt')
        for r in input:
            if self.parse(r.strip()):
                continue
            logging.warning('ini : %s : unable to parse : %s', self.state['name'], repr(r))

    def parse(self, line):
        if line.startswith('#'):
            return True
        line = dotini.comment.sub('', line).strip()
        if len(line) == 0:
            return True
        _ = dotini.section.match(line)
        if _:
            self.parse_section(_)
            return True
        _ = dotini.item.match(line)
        if _:
            self.parse_item(_)
            return True
        return False

    def parse_section(self, m):
        sectionname = m.group(1)
        self.state = {}
        logging.debug('ini : %s : adding section', sectionname)
        self.append((sectionname, self.state))

    def parse_item(self, m):
        itemname, itemvalue = m.group(1), m.group(2)
        self.state[itemname] = itemvalue


class db(list):

    def __init__(self, *filenames):
        for f in filenames:
            self.parse(f)

    def search(self, string):
        return [ p for p in self if p.name == string ]

    def parse(self, filename):
        input = dotini()
        input.read(filename)
        validitems = set(('ep_only', 'signature', 'section_start_only'))
        items = set()
        [ items.update(res.keys()) for signame, res in input ]
        if items.difference(validitems):
            raise NotImplementedError('db : %s : not sure how to process signature fields : %s' % (filename, items.difference(validitems)))
        for signame, res in input:
            try:
                p = signature(signame, res)
                self.append(p)
            except Exception as e:
                logging.warn('db : %s : unable to load signature for %s : %s', filename, repr(signame), type(e))

            continue


class signature(object):

    @staticmethod
    def boolean(string):
        if string.lower() == 'true':
            return True
        if string.lower() == 'false':
            return False
        raise TypeError(string)

    @staticmethod
    def hextoken(ch):
        if ch == '??' or ch in ('v3', 'v4') or ':' in ch:
            return None
        if ch[0] == '?':
            y = int(ch[1], 16)
            return set(x * 16 + y for x in range(16))
        else:
            if len(ch) == 1:
                y = int(ch[0], 16)
                return set(y * 16 + x for x in range(16))
            if ch[1] == '?':
                y = int(ch[0], 16)
                return set(y * 16 + x for x in range(16))
            return set((int(ch, 16),))

    def __init__(self, name, res):
        string = res['signature'].lower()
        self.name, self.string = name, string
        self.sig = self.parse_signature(string)
        self.ep_only = signature.boolean(res.get('ep_only', 'false'))
        self.section_start_only = signature.boolean(res.get('section_start_only', 'false'))
        if (self.ep_only or self.section_start_only) and self.ep_only == self.section_start_only:
            raise ValueError('%s ep:%s ss:%s' % (repr(name), self.ep_only, self.section_start_only))

    def __eq__(self, other):
        return (
         self.name, self.string) == (other.name, other.string)

    def __hash__(self):
        return (
         self.name, self.string).__hash__()

    signature = re.compile('^[a-f0-9v: ?]+$')

    def parse_signature(self, string):
        if not signature.signature.match(string):
            raise ValueError('%s %s' % (repr(self.name), repr(string)))
        sig = self.sig = [ signature.hextoken(x.lower()) for x in string.split(' ') ]
        return sig

    def match(self, string):
        zig = self.sig
        for i, (a, b) in enumerate(zip(zig, string)):
            if a is None:
                continue
            if ord(b) not in a:
                return False
                continue

        return i + 1 == len(zig)

    def generate(self):
        result = []
        for x in self.sig:
            if x is None:
                x = random.randint(0, 255)
            else:
                x, = random.sample(x, 1)
            result.append(x)

        return ('').join(map(chr, result))

    def __repr__(self):
        if self.ep_only:
            type = 'entrypoint'
        elif self.section_start_only:
            type = 'sectionstart'
        else:
            type = 'anywhere'
        return (' ').join((repr(signature), type, repr(self.name)))


def compile(db):
    state = {}
    res = NFA(-1)
    res.add_transition(-1, NFA.ANY, -1)
    for row in db:
        res.add_transition(-1, NFA.EPSILON, (0, row))
        for i, v in enumerate(row.sig):
            v = (NFA.ANY,) if v is None else (chr(x) for x in v)
            [ res.add_transition((i, row), x, (i + 1, row)) for x in v ]

        res.add_transition((i + 1, row), NFA.ANY, (i + 1, row))
        res.add_final_state((i + 1, row))
        state.setdefault((i + 1, row), []).append(row)

    return (
     state, res)


if __name__ == '__main__' and False:
    import peid
    reload(peid)
    db = peid.db('userdb.txt')
    while True:
        a, = random.sample(db, 1)
        if '??' in a.string:
            continue
        break

    print a
    s = a.generate()
    state, res = peid.compile(db)
    print 'executing nfa'
    res.bytecode(nondeterministic=False)
    print res.execute(s, debug=True)
elif __name__ == '__main__':
    import peid
    db = peid.db('userdb.txt')
    _ = '00 58 35 4F 21 50 25 40 41 50 5B 34 5C 50 5A 58 35 34 28 50 5E 29 37 43 43 29 37 7D 24 45 49 43 41 52 2D 53 54 41 4E 44 41 52 44 2D 41 4E 54 49 56 49 52 55 53 2D 54 45 53 54 2D 46 49 4C 45 21 24 48 2B 48 2A'
    s = ('').join(chr(int(x, 16)) for x in _.split(' '))
    print 'records', len(db)
    states, res = peid.compile(db)
    print 'compiled', len(states)
    print 'transitions', len(res._transitions)
    print res, 'versus', s
    print 'compiling to bytecode'
    print 'made bytecode'
    for i, x in enumerate(res.execute(s)):
        print i, x