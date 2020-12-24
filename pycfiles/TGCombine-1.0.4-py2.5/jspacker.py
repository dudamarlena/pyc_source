# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgcombine/jspacker.py
# Compiled at: 2008-05-21 00:28:01
"""  ParseMaster, version 1.0 (pre-release) (2005/05/12) x6
  Copyright 2005, Dean Edwards
  Web: http://dean.edwards.name/

  This software is licensed under the CC-GNU LGPL
  Web: http://creativecommons.org/licenses/LGPL/2.1/

  Ported to Python by Florian Schulze
  Ported to TG Combine by Vince Spicer
  """
import os, re

class Pattern:

    def __init__(self, expression, replacement, length):
        self.expression = expression
        self.replacement = replacement
        self.length = length

    def __str__(self):
        return '(' + self.expression + ')'


class Patterns(list):

    def __str__(self):
        return ('|').join([ str(e) for e in self ])


class ParseMaster:
    EXPRESSION = 0
    REPLACEMENT = 1
    LENGTH = 2
    GROUPS = re.compile('\\(', re.M)
    SUB_REPLACE = re.compile('\\$\\d', re.M)
    INDEXED = re.compile('^\\$\\d+$', re.M)
    TRIM = re.compile('([\'"])\\1\\+(.*)\\+\\1\\1$', re.M)
    ESCAPE = re.compile('\\\\.', re.M)
    DELETED = re.compile('\x01[^\x01]*\x01', re.M)

    def __init__(self):
        self._patterns = Patterns()
        self._escaped = []
        self.ignoreCase = False
        self.escapeChar = None
        return

    def DELETE(self, match, offset):
        return '\x01' + match.group(offset) + '\x01'

    def _repl(self, a, o, r, i):
        while i:
            m = a.group(o + i - 1)
            if m is None:
                s = ''
            else:
                s = m
            r = r.replace('$' + str(i), s)
            i = i - 1

        r = ParseMaster.TRIM.sub('$1', r)
        return r

    def add(self, expression='^$', replacement=None):
        if replacement is None:
            replacement = self.DELETE
        length = len(ParseMaster.GROUPS.findall(self._internalEscape(str(expression)))) + 1
        if isinstance(replacement, str) and ParseMaster.SUB_REPLACE.match(replacement):
            if ParseMaster.INDEXED.match(replacement):
                replacement = int(replacement[1:]) - 1
            else:
                i = length
                r = replacement
                replacement = lambda a, o: self._repl(a, o, r, i)
        self._patterns.append(Pattern(expression, replacement, length))
        return

    def execute(self, string):
        if self.ignoreCase:
            r = re.compile(str(self._patterns), re.I | re.M)
        else:
            r = re.compile(str(self._patterns), re.M)
        string = self._escape(string, self.escapeChar)
        string = r.sub(self._replacement, string)
        string = self._unescape(string, self.escapeChar)
        string = ParseMaster.DELETED.sub('', string)
        return string

    def reset(self):
        self._patterns = Patterns()

    def _replacement(self, match):
        i = 1
        for pattern in self._patterns:
            if match.group(i) is not None:
                replacement = pattern.replacement
                if callable(replacement):
                    return replacement(match, i)
                elif isinstance(replacement, (int, long)):
                    return match.group(replacement + i)
                else:
                    return replacement
            else:
                i = i + pattern.length

        return

    def _escape(self, string, escapeChar=None):

        def repl(match):
            char = match.group(1)
            self._escaped.append(char)
            return escapeChar

        if escapeChar is None:
            return string
        r = re.compile('\\' + escapeChar + '(.)', re.M)
        result = r.sub(repl, string)
        return result

    def _unescape(self, string, escapeChar=None):

        def repl(match):
            try:
                result = escapeChar + self._escaped.pop(0)
                return result
            except IndexError:
                return escapeChar

        if escapeChar is None:
            return string
        r = re.compile('\\' + escapeChar, re.M)
        result = r.sub(repl, string)
        return result

    def _internalEscape(self, string):
        return ParseMaster.ESCAPE.sub('', string)


class JavaScriptPacker:

    def __init__(self):
        self._basicCompressionParseMaster = self.getCompressionParseMaster(False)
        self._specialCompressionParseMaster = self.getCompressionParseMaster(True)

    def basicCompression(self, script):
        return self._basicCompressionParseMaster.execute(script)

    def specialCompression(self, script):
        return self._specialCompressionParseMaster.execute(script)

    def getCompressionParseMaster(self, specialChars):
        IGNORE = '$1'
        parser = ParseMaster()
        parser.escapeChar = '\\'
        parser.add("'[^']*?'", IGNORE)
        parser.add('"[^"]*?"', IGNORE)
        parser.add('//[^\\n\\r]*?[\\n\\r]')
        parser.add('/\\*[^*]*?\\*+([^/][^*]*?\\*+)*?/')
        parser.add('\\s+(\\/[^\\/\\n\\r\\*][^\\/\\n\\r]*\\/g?i?)', '$2')
        parser.add('[^\\w\\$\\/\'"*)\\?:]\\/[^\\/\\n\\r\\*][^\\/\\n\\r]*\\/g?i?', IGNORE)
        if specialChars:
            parser.add(';;;[^\n\r]+[\n\r]')
        parser.add(';+\\s*([};])', '$2')
        parser.add('(\\b|\\$)\\s+(\\b|\\$)', '$2 $3')
        parser.add('([+\\-])\\s+([+\\-])', '$2 $3')
        parser.add('\\s+', '')
        return parser

    def getEncoder(self, ascii):
        mapping = {}
        base = ord('0')
        mapping.update(dict([ (i, chr(i + base)) for i in range(10) ]))
        base = ord('a')
        mapping.update(dict([ (i + 10, chr(i + base)) for i in range(26) ]))
        base = ord('A')
        mapping.update(dict([ (i + 36, chr(i + base)) for i in range(26) ]))
        base = 161
        mapping.update(dict([ (i + 62, chr(i + base)) for i in range(95) ]))

        def encode10(charCode):
            return str(charCode)

        def encode36(charCode):
            l = []
            remainder = charCode
            while 1:
                (result, remainder) = divmod(remainder, 36)
                l.append(mapping[remainder])
                if not result:
                    break
                remainder = result

            l.reverse()
            return ('').join(l)

        def encode62(charCode):
            l = []
            remainder = charCode
            while 1:
                (result, remainder) = divmod(remainder, 62)
                l.append(mapping[remainder])
                if not result:
                    break
                remainder = result

            l.reverse()
            return ('').join(l)

        def encode95(charCode):
            l = []
            remainder = charCode
            while 1:
                (result, remainder) = divmod(remainder, 95)
                l.append(mapping[(remainder + 62)])
                if not result:
                    break
                remainder = result

            l.reverse()
            return ('').join(l)

        if ascii <= 10:
            return encode10
        elif ascii <= 36:
            return encode36
        elif ascii <= 62:
            return encode62
        return encode95

    def escape(self, script):
        script = script.replace('\\', '\\\\')
        script = script.replace("'", "\\'")
        script = script.replace('\n', '\\n')
        return script

    def escape95(self, script):
        result = []
        for x in script:
            if x > b'\xa1':
                x = '\\x%0x' % ord(x)
            result.append(x)

        return ('').join(result)

    def encodeKeywords(self, script, encoding, fastDecode):
        if encoding > 62:
            script = self.escape95(script)
        parser = ParseMaster()
        encode = self.getEncoder(encoding)
        if encoding > 62:
            regexp = '\\w\\w+'
        else:
            regexp = '\\w+'
        keywords = self.analyze(script, regexp, encode)
        encoded = keywords['encoded']

        def repl(match, offset):
            return encoded.get(match.group(offset), '')

        parser.add(regexp, repl)
        script = parser.execute(script)
        script = self.bootStrap(script, keywords, encoding, fastDecode)
        return script

    def analyze(self, script, regexp, encode):
        regexp = re.compile(regexp, re.M)
        all = regexp.findall(script)
        sorted = []
        encoded = {}
        protected = {}
        if all:
            unsorted = []
            _protected = {}
            values = {}
            count = {}
            all.reverse()
            for word in all:
                word = '$' + word
                if word not in count:
                    count[word] = 0
                    j = len(unsorted)
                    unsorted.append(word)
                    values[j] = encode(j)
                    _protected['$' + values[j]] = j
                count[word] = count[word] + 1

            sorted = [
             None] * len(unsorted)
            for word in unsorted:
                if word in _protected and isinstance(_protected[word], int):
                    sorted[_protected[word]] = word[1:]
                    protected[_protected[word]] = True
                    count[word] = 0

            unsorted.sort(lambda a, b: count[b] - count[a])
            j = 0
            for i in range(len(sorted)):
                if sorted[i] is None:
                    sorted[i] = unsorted[j][1:]
                    j = j + 1
                encoded[sorted[i]] = values[i]

        return {'sorted': sorted, 'encoded': encoded, 'protected': protected}

    def encodePrivate(self, charCode):
        return '_' + str(charCode)

    def encodeSpecialChars(self, script):
        parser = ParseMaster()

        def repl(match, offset):
            length = len(match.group(offset + 2))
            start = length - max(length - len(match.group(offset + 3)), 0)
            return match.group(offset + 1)[start:start + length] + match.group(offset + 4)

        parser.add('((\\$+)([a-zA-Z\\$_]+))(\\d*)', repl)
        regexp = '\\b_[A-Za-z\\d]\\w*'
        keywords = self.analyze(script, regexp, self.encodePrivate)
        encoded = keywords['encoded']

        def repl(match, offset):
            return encoded.get(match.group(offset), '')

        parser.add(regexp, repl)
        return parser.execute(script)

    def bootStrap(self, packed, keywords, encoding, fastDecode):
        ENCODE = re.compile('\\$encode\\(\\$count\\)')
        packed = "'" + self.escape(packed) + "'"
        count = len(keywords['sorted'])
        ascii = min(count, encoding) or 1
        for i in keywords['protected']:
            keywords['sorted'][i] = ''

        keywords = "'" + ('|').join(keywords['sorted']) + "'.split('|')"
        encoding_functions = {10: ' function($charCode) {\n                        return $charCode;\n                    }', 
           36: ' function($charCode) {\n                        return $charCode.toString(36);\n                    }', 
           62: ' function($charCode) {\n                        return ($charCode < _encoding ? "" : arguments.callee(parseInt($charCode / _encoding))) +\n                            (($charCode = $charCode % _encoding) > 35 ? String.fromCharCode($charCode + 29) : $charCode.toString(36));\n                    }', 
           95: ' function($charCode) {\n                        return ($charCode < _encoding ? "" : arguments.callee($charCode / _encoding)) +\n                            String.fromCharCode($charCode % _encoding + 161);\n                    }'}
        encode = encoding_functions[encoding]
        encode = encode.replace('_encoding', '$ascii')
        encode = encode.replace('arguments.callee', '$encode')
        if ascii > 10:
            inline = '$count.toString($ascii)'
        else:
            inline = '$count'
        if fastDecode:
            decode = "// does the browser support String.replace where the\n                        //  replacement value is a function?\n                        if (!''.replace(/^/, String)) {\n                            // decode all the values we need\n                            while ($count--) $decode[$encode($count)] = $keywords[$count] || $encode($count);\n                            // global replacement function\n                            $keywords = [function($encoded){return $decode[$encoded]}];\n                            // generic match\n                            $encode = function(){return'\\\\w+'};\n                            // reset the loop counter -  we are now doing a global replace\n                            $count = 1;\n                        }"
            if encoding > 62:
                decode = decode.replace('\\\\w', '[\\xa1-\\xff]')
            elif ascii < 36:
                decode = ENCODE.sub(inline, decode)
            if not count:
                raise NotImplemented
        unpack = 'function($packed, $ascii, $count, $keywords, $encode, $decode) {\n                        while ($count--)\n                            if ($keywords[$count])\n                                $packed = $packed.replace(new RegExp("\\\\b" + $encode($count) + "\\\\b", "g"), $keywords[$count]);\n                        return $packed;\n                    }'
        if fastDecode:
            unpack = unpack.replace('{', '{' + decode + ';', 1)
        if encoding > 62:
            unpack = re.sub("'\\\\\\\\b'\\s*\\+|\\+\\s*'\\\\\\\\b'", '', unpack)
        if ascii > 36 or encoding > 62 or fastDecode:
            unpack = unpack.replace('{', '{$encode=' + encode + ';', 1)
        else:
            unpack = ENCODE.sub(inline, unpack)
        unpack = self.pack(unpack, 0, False, True)
        params = [
         packed, str(ascii), str(count), keywords]
        if fastDecode:
            params.extend(['0', '{}'])
        return 'eval(' + unpack + '(' + (',').join(params) + '))\n'

    def pack(self, script, encoding=0, fastDecode=False, specialChars=False, compaction=True):
        script = script + '\n'
        self._encoding = encoding
        self._fastDecode = fastDecode
        if specialChars:
            script = self.specialCompression(script)
            script = self.encodeSpecialChars(script)
        elif compaction:
            script = self.basicCompression(script)
        if encoding:
            script = self.encodeKeywords(script, encoding, fastDecode)
        return script