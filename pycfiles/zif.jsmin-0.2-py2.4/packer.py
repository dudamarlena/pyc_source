# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/zif/jsmin/thirdparty/packer.py
# Compiled at: 2006-12-16 06:43:22
import re

class KeywordMapper:
    __module__ = __name__

    def __init__(self, regexp, encoder):
        if isinstance(regexp, (str, unicode)):
            self.regexp = re.compile(regexp)
        else:
            self.regexp = regexp
        self.encoder = encoder
        self.mapping = {}

    def analyseKeywords(self, input):
        matches = self.regexp.findall(input)
        protected = {}
        keyword_count = {}
        index = 0
        for match in matches:
            if match not in keyword_count:
                keyword_count[match] = 0
                protected[self.encoder(index)] = index
                index = index + 1
            keyword_count[match] = keyword_count[match] + 1

        for match in matches:
            if match in protected and keyword_count[match]:
                keyword_count[match] = 0

        protected = {}
        for match in keyword_count:
            if not keyword_count[match]:
                protected[match] = None

        sorted_matches = []
        for (value, count) in keyword_count.iteritems():
            weight = count * len(value)
            if len(value) >= weight:
                keyword_count[value] = 0
                sorted_matches.append((0, value))
            else:
                sorted_matches.append((weight, value))

        sorted_matches.sort()
        sorted_matches.reverse()
        sorted_matches = [ x[(-1)] for x in sorted_matches ]
        index = 0
        mapping = {}
        for match in sorted_matches:
            if not keyword_count[match]:
                if match not in protected:
                    mapping[match] = (
                     -1, match)
                continue
            while 1:
                encoded = self.encoder(index)
                index = index + 1
                if encoded in protected:
                    mapping[encoded] = (
                     index - 1, encoded)
                    continue
                else:
                    break

            mapping[match] = (
             index - 1, encoded)

        return mapping

    def analyse(self, input):
        self.mapping = self.analyseKeywords(input)

    def getKeywords(self):
        sorted = zip(self.mapping.itervalues(), self.mapping.iterkeys())
        sorted.sort()
        keywords = []
        for ((index, encoded), value) in sorted:
            if index >= 0:
                if encoded != value:
                    keywords.append(value)
                else:
                    keywords.append('')

        return keywords

    def sub(self, input):

        def repl(m):
            return self.mapping.get(m.group(0), ('', m.group(0)))[1]

        return self.regexp.sub(repl, input)


class JavascriptKeywordMapper(KeywordMapper):
    __module__ = __name__

    def __init__(self, regexp=None, encoder=None):
        if regexp is None:
            self.regexp = re.compile('\\w+')
        elif isinstance(regexp, (str, unicode)):
            self.regexp = re.compile(regexp)
        else:
            self.regexp = regexp
        if encoder is None:
            self.encoder = self._encode
        else:
            self.encoder = encoder
        self.mapping = {}
        return

    def _encode(self, charCode, mapping='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        result = []
        quotient = charCode
        while quotient or not len(result):
            (quotient, remainder) = divmod(quotient, 62)
            result.append(mapping[remainder])

        result.reverse()
        return ('').join(result)

    def getDecodeFunction(self, fast=True, name=None):
        jspacker = JavascriptPacker('full')
        fast_decoder = '\n            // does the browser support String.replace where the\n            //  replacement value is a function?\n            if (!\'\'.replace(/^/, String)) {\n                // decode all the values we need\n                // we have to add the dollar prefix, because $encoded can be\n                // any keyword in the decode function below. For example\n                // \'constructor\' is an attribute of any object and it would\n                // return a false positive match in that case.\n                while ($count--) $decode["$"+$encode($count)] = $keywords[$count] || $encode($count);\n                // global replacement function\n                $keywords = [function($encoded){$result = $decode["$"+$encoded]; return $result!=undefined?$result:$encoded}];\n                // generic match\n                $encode = function(){return\'\\\\w+\'};\n                // reset the loop counter -  we are now doing a global replace\n                $count = 1;\n            };'
        if name is None:
            decoder = '\n                function($packed, $ascii, $count, $keywords, $encode, $decode) {\n                    $encode = function($charCode) {\n                        return ($charCode < $ascii ? "" : $encode(parseInt($charCode / $ascii))) +\n                            (($charCode = $charCode % $ascii) > 35 ? String.fromCharCode($charCode + 29) : $charCode.toString(36));\n                    };\n                    // fastDecodePlaceholder\n                    while ($count--)\n                        if ($keywords[$count])\n                            $packed = $packed.replace(new RegExp("\\\\b" + $encode($count) + "\\\\b", "g"), $keywords[$count]);\n                    return $packed;\n                }'
            if fast:
                decoder = decoder.replace('// fastDecodePlaceholder', fast_decoder)
            decoder = jspacker.pack(decoder)
        else:
            decoder = '\n                var %s = function($ascii, $count, $keywords, $encode, $decode) {\n                    $encode = function($charCode) {\n                        return ($charCode < $ascii ? "" : $encode(parseInt($charCode / $ascii))) +\n                            (($charCode = $charCode %% $ascii) > 35 ? String.fromCharCode($charCode + 29) : $charCode.toString(36));\n                    };\n                    // fastDecodePlaceholder\n                    var decoder = function($packed, $ascii1, $count1, $keywords1, $encode1, $decode1) {\n                        $count1 = $count;\n                        while ($count1--)\n                            if ($keywords[$count1])\n                                $packed = $packed.replace(new RegExp("\\\\b" + $encode($count1) + "\\\\b", "g"), $keywords[$count1]);\n                        return $packed;\n                    };\n                    return decoder;\n                }' % name
            if fast:
                decoder = decoder.replace('// fastDecodePlaceholder', fast_decoder)
            decoder = jspacker.pack(decoder)
            keywords = self.getKeywords()
            decoder = "%s(62, %i, '%s'.split('|'), 0, {});" % (decoder, len(keywords), ('|').join(keywords))
        return decoder

    def getDecoder(self, input, keyword_var=None, decode_func=None):
        if keyword_var is None:
            keywords = self.getKeywords()
            num_keywords = len(keywords)
            keywords = ('|').join(keywords)
            keywords = "'%s'.split('|')" % keywords
        else:
            keywords = keyword_var
            num_keywords = len(self.getKeywords())
        if decode_func is None:
            decode_func = self.getDecodeFunction()
        escaped_single = input.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
        escaped_double = input.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        if len(escaped_single) < len(escaped_double):
            script = "'%s'" % escaped_single
        else:
            script = '"%s"' % escaped_double
        return 'eval(%s(%s,62,%i,%s,0,{}))' % (decode_func, script, num_keywords, keywords)


class Packer:
    __module__ = __name__

    def __init__(self):
        self.patterns = []

    def copy(self):
        result = Packer()
        result.patterns = self.patterns[:]
        return result

    def _repl(self, match):
        self.replacelist.append(match.group(1))
        return '\x00%i' % len(self.replacelist)

    def pack(self, input):
        self.replacelist = []
        output = input.replace('\x00', '\x00\x00')
        for (regexp, replacement, keyword_encoder) in self.patterns:
            if replacement is None:
                if keyword_encoder is None:
                    output = regexp.sub(self._repl, output)
                else:
                    mapper = KeywordMapper(regexp=regexp, encoder=keyword_encoder)
                    mapper.analyse(output)
                    output = mapper.sub(output)
            else:
                output = regexp.sub(replacement, output)

        replacelist = list(enumerate(self.replacelist))
        replacelist.reverse()
        for (index, replacement) in replacelist:
            before = len(output)
            regexp = re.compile('(?<!\x00)\x00%i' % (index + 1))
            output = regexp.sub(lambda m: replacement, output)

        output = output.replace('\x00\x00', '\x00')
        return output

    def protect(self, pattern, flags=None):
        self.keywordSub(pattern, None, flags)
        return

    def sub(self, pattern, replacement, flags=None):
        if flags is None:
            self.patterns.append((re.compile(pattern), replacement, None))
        else:
            self.patterns.append((re.compile(pattern, flags), replacement, None))
        return

    def keywordSub(self, pattern, keyword_encoder, flags=None):
        if flags is None:
            self.patterns.append((re.compile(pattern), None, keyword_encoder))
        else:
            self.patterns.append((re.compile(pattern, flags), None, keyword_encoder))
        return


class JavascriptPacker(Packer):
    __module__ = __name__

    def __init__(self, level='safe'):
        Packer.__init__(self)
        if level == 'full':

            def _dollar_replacement(match):
                length = len(match.group(2))
                start = length - max(length - len(match.group(3)), 0)
                result = match.group(1)[start:start + length] + match.group(4)
                return result

            self.sub('((\\$+)([a-zA-Z\\$_]+))(\\d*)\\b', _dollar_replacement)
            self.keywordSub('\\b_[A-Za-z\\d]\\w*', lambda i: '_%i' % i)
            self.protect('(?<=return|..case|.....[=\\[|(,?:+])\\s*((?P<quote>[\'"])(?:\\\\(?P=quote)|\\\\\\n|.)*?(?P=quote))', re.DOTALL)
        else:
            self.protect("('(?:\\\\'|\\\\\\n|.)*?')")
            self.protect('("(?:\\\\"|\\\\\\n|.)*?")')
        self.protect('\\s+(\\/[^\\/\\n\\r\\*][^\\/\\n\\r]*\\/g?i?)')
        self.protect('([^\\w\\$\\/\'"*)\\?:]\\/[^\\/\\n\\r\\*][^\\/\\n\\r]*\\/g?i?)')
        self.sub('/\\*.*?\\*/', '', re.DOTALL)
        self.sub('\\s*//.*$', '', re.MULTILINE)
        self.sub('^[ \\t\\r\\f\\v]*(.*?)[ \\t\\r\\f\\v]*$', '\\1', re.MULTILINE)
        self.sub('([{;\\[(,=&|\\?:<>%!/])\\s+(?!function)', '\\1')
        self.sub('=\\s+(?=function)', '=')
        if level == 'full':
            self.sub('([};\\):,])\\s+', '\\1')
        self.sub('\\s+([={},&|\\?:\\.()<>%!/\\]])', '\\1')
        self.sub('(?<!\\+)\\s+\\+', '+')
        self.sub('\\+\\s+(?!\\+)', '+')
        self.sub('(?<!-)\\s+-', '-')
        self.sub('-\\s+(?!-)', '-')
        self.sub(';+\\s*([};])', '\\1')
        self.sub('[ \\t\\r\\f\\v]+', ' ')
        self.sub('\\n+', '\n')
        self.sub('^\\n', '')


class CSSPacker(Packer):
    __module__ = __name__

    def __init__(self, level='safe'):
        Packer.__init__(self)
        self.protect("('(?:\\\\'|\\\\\\n|.)*?')")
        self.protect('("(?:\\\\"|\\\\\\n|.)*?")')
        self.sub('^[ \\t\\r\\f\\v]*(.*?)[ \\t\\r\\f\\v]*$', '\\1', re.MULTILINE)
        self.sub('/\\*.*?( ?[\\\\/*]*\\*/)', '/*\\1', re.DOTALL)
        self.sub('^/\\*+\\*/$', '', re.MULTILINE)
        self.sub('\\n+', '\n')
        self.sub('^\\n', '')
        if level == 'full':
            self.sub('([{,;])\\s+', '\\1')