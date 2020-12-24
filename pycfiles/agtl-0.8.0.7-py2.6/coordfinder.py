# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/coordfinder.py
# Compiled at: 2011-04-23 08:43:29
from __future__ import division
TEST = (
 '\n\n\n\n', {'A': 2, 'D': 4, 'G': 3, 'T': 1, 'R': 2, 'S': 1, 'H': 4, 'B': 2, 'C': 9, 'E': 0, 'F': 1})
HTML = '\n\n<br /></p> \n<p><font face="Arial, sans-serif"><font size=\n"4"><b>Final:</b></font></font></p> \n<p style="font-style: normal"><font color="#000000"><font face=\n"Arial, sans-serif"><font size="3"><b><span style=\n"background: transparent">N 49°\n(B-C+A+0,5*D).(F+D)(F-G)(C-2*A)</span></b></font></font></font></p> \n<p style="font-style: normal"><font color="#000000"><font face=\n"Arial, sans-serif"><font size="3"><b><span style=\n"background: transparent">E 6°\n(2*A+C).(G-E)(B-C+0,5*D)(F-D)</span></b></font></font></font></p> \n<p style="font-style: normal; font-weight: normal"><font color=\n"#000000"><font face="Arial, sans-serif"><font size=\n"3"><span style="background: transparent">Es müssen keine Zäune\noder Mauern überwunden werden.</span></font></font></font></p>\nN 49°\n(B-C+A+0,5*D).(F+D)(F-G)(D-2*B)\n<p><br /> \n<br /></p></span> \n                \n            </div> \n            <p> \n</p> \n'
import geo, re, logging
logger = logging.getLogger('coordfinder')

class CalcCoordinateManager(object):

    def __init__(self, vars):
        self.__vars = vars
        self.__known_signatures = []
        self.__filtered_signatures = []
        self.requires = set()
        self.coords = []
        logger.debug('New coordfinder started')

    def add_text(self, text, source):
        logger.debug('Adding Text with length %d from source %s' % (len(text), source))
        self.__add_coords(CalcCoordinate.find(text, source))

    def __add_coords(self, coords, apply_filter=True):
        for x in coords:
            logger.debug('Adding: %s, apply_filter = %s' % (x, apply_filter))
            if x.signature in self.__known_signatures:
                continue
            if apply_filter and x.signature in self.__filtered_signatures:
                continue
            self.__known_signatures.append(x.signature)
            self.requires |= x.requires
            self.coords.append(x)

        logger.debug('Now having %d coords, %d requires' % (len(self.coords), len(self.requires)))

    def __remove_coord(self, signature):
        self.__filtered_signatures.append(signature)
        self.__known_signatures = []
        self.requires = set()
        logger.debug('Removing: %s' % signature)
        new_coords = []
        for x in self.coords:
            if x.signature != signature:
                self.requires |= x.requires
                new_coords.append(x)
                self.__known_signatures.append(x.signature)

        self.coords = new_coords
        logger.debug('Now having %d coords, %d requires' % (len(self.coords), len(self.requires)))

    def add_replacement(self, signature, replacement_text, source):
        self.__remove_coord(signature)
        self.__add_coords(CalcCoordinate.find(replacement_text, source), False)

    def set_var(self, char, value):
        if value != '':
            self.__vars[char] = value
        else:
            del self.__vars[char]
        self.update()

    def update(self):
        logger.debug('updating...')
        for c in self.coords:
            c.set_vars(self.__vars)
            if c.has_requires():
                c.try_get_solution()

    def get_solutions(self):
        return [ (c.result, c.source) for c in self.coords if c.has_requires() if len(c.requires) > 0 ]

    def get_plain_coordinates(self):
        return [ (c.result, c.source) for c in self.coords if len(c.requires) == 0 ]

    def get_vars(self):
        return self.__vars


class CalcCoordinate:
    WARNING_NEGATIVE = 'Negative intermediate result (%d).'
    WARNING_VERY_HIGH = 'Very high intermediate result (%d).'
    WARNING_FLOAT = "Intermediate result with decimal point ('%s')."
    WARNING_WRONG_LENGTH = '%d digits where %s digits were expected (%s).'
    WARNING_CANNOT_PARSE = 'Cannot parse result: %s.'
    WARNING_SYNTAX = 'Could not parse formula.'
    HIGH_RESULT_THRESHOLD = 1000
    EXPECTED_LENGTHS = [
     (1, 2), (1, 2), (3, ), (1, 2, 3), (1, 2), (3, )]

    def __init__(self, ns, lat_deg, lat_min, lat_min_2, ew, lon_deg, lon_min, lon_min_2, source):
        self.ns = ns
        self.ew = ew
        self.lat_deg = self.__prepare(lat_deg)
        self.lat_min = self.__prepare(lat_min)
        self.lat_min_2 = self.__prepare(lat_min_2)
        self.lon_deg = self.__prepare(lon_deg)
        self.lon_min = self.__prepare(lon_min)
        self.lon_min_2 = self.__prepare(lon_min_2)
        self.orig = '%s%s %s.%s %s%s %s.%s' % (self.ns, self.lat_deg, self.lat_min, self.lat_min_2, self.ew, self.lon_deg, self.lon_min, self.lon_min_2)
        self.requires = set(x for i in [self.lat_deg, self.lat_min, self.lat_min_2, self.lon_deg, self.lon_min, self.lon_min_2] for x in re.sub('[^A-Za-z]', '', i))
        self.warnings = []
        self.vars = {}
        self.signature = ('|').join([ns, self.lat_deg, self.lat_min, self.lat_min_2, ew, self.lon_deg, self.lon_min, self.lon_min_2])
        self.source = source

    def __prepare(self, text):
        return re.sub('[^A-Za-z()+*/0-9-.,]', '', text).replace(',', '.')

    def set_vars(self, var):
        self.warnings = []
        self.vars = var

    def has_requires(self):
        for i in self.requires:
            if i not in self.vars:
                return False

        return True

    def try_get_solution(self):
        replaced = [ self.__replace(x) for x in [self.lat_deg, self.lat_min, self.lat_min_2, self.lon_deg, self.lon_min, self.lon_min_2] ]
        self.replaced_result = '%%s%s %s.%s %%s%s %s.%s' % tuple(replaced) % (self.ns, self.ew)
        results = [ self.resolve(x) for x in replaced ]
        for i in range(len(results)):
            if len(results[i]) not in self.EXPECTED_LENGTHS[i]:
                self.warnings.append(self.WARNING_WRONG_LENGTH % (len(results[i]), (' or ').join([ str(x) for x in self.EXPECTED_LENGTHS[i] ]), results[i]))

        result = '%%s%s %s.%s %%s%s %s.%s' % tuple(results) % (self.ns, self.ew)
        try:
            self.result = geo.try_parse_coordinate(result)
            self.result.name = self.orig
        except Exception:
            self.warnings.append(self.WARNING_CANNOT_PARSE % result)
            self.result = False

    def __replace(self, text):
        for (char, value) in self.vars.items():
            text = text.replace(char, str(value))

        return text

    def resolve(self, text):
        c = 1
        while c > 0:
            (text, c) = re.subn('\\([^()]+\\)', lambda match: self.__safe_eval(match.group(0)), text)

        if re.match('^[0-9]+$', text) == None:
            text = self.__safe_eval(text)
            try:
                text = '%03d' % int(text)
            except Exception:
                text = '?'

        return text

    def __safe_eval(self, text):
        try:
            tmp = eval(text, {'__builtins__': None}, {})
        except (SyntaxError, Exception):
            self.warnings.append(self.WARNING_SYNTAX)
            return '?'
        else:
            if round(tmp) != round(tmp, 1):
                self.warnings.append(self.WARNING_FLOAT % text)
            tmp = int(tmp)
            if tmp < 0:
                self.warnings.append(self.WARNING_NEGATIVE % tmp)
            if tmp > self.HIGH_RESULT_THRESHOLD:
                self.warnings.append(self.WARNING_VERY_HIGH % tmp)

        return str(tmp)

    def __str__(self):
        return '<%s> from %s' % (self.orig, self.source)

    SINGLE_CALC_PART = '((?:\\([A-Za-z +*/0-9-.,]+\\)|[A-Za-z ()+*/0-9-])+)'

    @staticmethod
    def find(text, source):
        text = re.sub('(?u)\\s[^\\W\\d_]{2,}\\s', ' | ', text)
        text = re.sub('(?u)\\b[^\\W\\d_]{4,}\\b', ' | ', text)
        text = text.replace('°', '|')
        text = text.decode('utf-8', 'replace').encode('utf-8')
        text = text.replace(unichr(160), ' ')
        text = re.sub(' +', ' ', text)
        matches = re.findall("(?<![a-zA-Z])([NSns])\\s?([A-Z() -+*/0-9]+?)[\\s|]{1,2}%(calc)s[.,\\s]%(calc)s['`\\s,/]+([EOWeow])\\s?([A-Z() -+*/0-9]+?)[\\s|]{1,2}%(calc)s[.,\\s]%(calc)s[\\s'`]*(?![a-zA-Z])" % {'calc': CalcCoordinate.SINGLE_CALC_PART}, text)
        return [ CalcCoordinate(*match, **{'source': source}) for match in matches ]

    @staticmethod
    def is_calc_string(text):
        regex = "^([NSns])\\s?([A-Z() -+*/0-9]+?)[\\s|]{1,2}%(calc)s[.,\\s]%(calc)s['`\\s,/]+([EOWeow])\\s?([A-Z() -+*/0-9]+?)[\\s|]{1,2}%(calc)s[.,\\s]%(calc)s[\\s'`]*$" % {'calc': CalcCoordinate.SINGLE_CALC_PART}
        return re.match(regex, text) != None


if __name__ == '__main__':
    from simplegui import SimpleGui
    print '\n\n========================================================='
    h = SimpleGui._strip_html(HTML)
    print h
    print '---------------------------------------------------------'
    for instance in CalcCoordinate.find(h)[0]:
        print 'Found: %s' % instance.orig