# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kanzen/kanzen/code_completion.py
# Compiled at: 2012-08-23 23:22:25
from __future__ import absolute_import
import re, token as tkn
from tokenize import generate_tokens, TokenError
from StringIO import StringIO
from kanzen import utils
from kanzen import model
from kanzen import analyzer
from kanzen import completer
from kanzen import completion_daemon
_TOKEN_NL = 54

class CodeCompletion(object):

    def __init__(self):
        self.analyzer = analyzer.Analyzer()
        self.cdaemon = completion_daemon.CompletionDaemon()
        model.MODULES = self.cdaemon.modules
        self.module_id = None
        self.patIndent = re.compile('^\\s+')
        self.patClass = re.compile('class (\\w+?)\\(')
        self.patFunction = re.compile('(\\w+?)\\(')
        self.patWords = re.compile('\\W+')
        self._valid_op = (')', '}', ']')
        self._invalid_op = ('(', '{', '[')
        self._invalid_words = ('if', 'elif', 'for', 'while', 'in', 'return', 'and',
                               'or', 'del', 'except', 'from', 'import', 'is', 'print',
                               'super', 'yield')
        return

    def unload_module(self):
        self.cdaemon.unload_module(self.module_id)

    def analyze_file(self, path, source=None):
        if source is None:
            with open(path) as (f):
                source = f.read()
        split_last_lines = source.rsplit('\n', 2)
        if len(split_last_lines) > 1 and split_last_lines[(-2)].endswith(':') and split_last_lines[(-1)] == '':
            indent = utils.get_indentation(split_last_lines[(-2)])
            source += '%spass;' % indent
        self.module_id = path
        if not self.cdaemon.daemon.is_alive():
            completion_daemon.shutdown_daemon()
            del self.cdaemon
            self.cdaemon = completion_daemon.CompletionDaemon()
            model.MODULES = self.cdaemon.modules
        module = self.cdaemon.get_module(self.module_id)
        module = self.analyzer.analyze(source, module)
        self.cdaemon.inspect_module(self.module_id, module)
        return

    def _tokenize_text(self, code):
        token_code = []
        try:
            for tkn_type, tkn_str, pos, _, line in generate_tokens(StringIO(code).readline):
                token_code.append((tkn_type, tkn_str, pos, line))

        except TokenError:
            pass
        except IndentationError:
            return []

        while token_code[(-1)][0] in (tkn.ENDMARKER, tkn.DEDENT, tkn.NEWLINE):
            token_code.pop()

        return token_code

    def _search_for_scope(self, token_code):
        if not token_code or not token_code[(-1)][3].startswith(' '):
            return
        scopes = []
        indent = self.patIndent.match(token_code[(-1)][3])
        if indent is not None:
            indent = len(indent.group())
        else:
            indent = 0
        previous_line = ('', '')
        keep_exploring = True
        iterate = reversed(token_code)
        line = iterate.next()
        while keep_exploring:
            is_indented = line[3].startswith(' ')
            is_definition = line[1] in ('def', 'class')
            if is_indented and is_definition:
                new_indent = self.patIndent.match(line[3])
                if new_indent is not None:
                    new_indent = len(new_indent.group())
                if new_indent < indent:
                    indent = new_indent
                    scopes.insert(0, previous_line)
            else:
                if not is_indented and is_definition:
                    scopes.insert(0, previous_line)
                    keep_exploring = False
                previous_line = line[1]
                try:
                    line = iterate.next()
                except StopIteration:
                    keep_exploring = False

        return scopes

    def _search_for_completion_segment(self, token_code):
        tokens = []
        keep_iter = True
        iterate = reversed(token_code)
        while keep_iter:
            try:
                value = iterate.next()
                if value[0] in (tkn.NEWLINE, tkn.INDENT, tkn.DEDENT):
                    keep_iter = False
                tokens.append(value)
            except:
                keep_iter = False

        segment = ''
        brace_stack = 0
        first_element = True
        for t in tokens:
            token_str = t[1]
            if token_str in self._invalid_words and not first_element:
                break
            elif token_str in self._valid_op:
                if brace_stack == 0:
                    segment = token_str + segment
                brace_stack += 1
            elif token_str in self._invalid_op:
                brace_stack -= 1
                if brace_stack == 0:
                    segment = token_str + segment
                    continue
            first_element = False
            if brace_stack != 0:
                continue
            op = t[0]
            if op == tkn.NAME or token_str == '.':
                segment = token_str + segment
            elif op == tkn.OP:
                break

        return segment

    def get_prefix(self, code, offset):
        """Return the prefix of the word under the cursor and a boolean
        saying if it is a valid completion area."""
        token_code = self._tokenize_text(code[:offset])
        var_segment = self._search_for_completion_segment(token_code)
        words_final = var_segment.rsplit('.', 1)
        final_word = ''
        if not var_segment.endswith('.') and len(words_final) > 1:
            final_word = words_final[1].strip()
        elif var_segment != '' and len(words_final) == 1:
            final_word = words_final[0].strip()
        return (
         final_word, var_segment != '')

    def get_completion(self, code, offset):
        token_code = self._tokenize_text(code[:offset])
        scopes = self._search_for_scope(token_code)
        var_segment = self._search_for_completion_segment(token_code)
        words = var_segment.split('.', 1)
        words_final = var_segment.rsplit('.', 1)
        main_attribute = words[0].strip().split('(', 1)
        attr_name = main_attribute[0]
        word = ''
        final_word = ''
        if var_segment.count('.') > 0:
            word = words[1].strip()
        if not var_segment.endswith('.') and len(words_final) > 1:
            final_word = words_final[1].strip()
            word = word.rsplit('.', 1)[0].strip()
            if final_word == word:
                word = ''
        self.cdaemon.lock.acquire()
        module = self.cdaemon.get_module(self.module_id)
        imports = module.get_imports()
        result = module.get_type(attr_name, word, scopes)
        self.cdaemon.lock.release()
        if result['found'] and result['type'] is not None:
            prefix = attr_name
            if result['type'] != attr_name:
                prefix = result['type']
                word = final_word
            to_complete = '%s.%s' % (prefix, word)
            if result.get('main_attr_replace', False):
                to_complete = var_segment.replace(attr_name, result['type'], 1)
            imports = [ imp.split('.')[0] for imp in imports ]
            data = completer.get_all_completions(to_complete, imports)
            __attrib = [ d for d in data.get('attributes', []) if d[:2] == '__' ]
            if __attrib:
                map(lambda i: data['attributes'].remove(i), __attrib)
                data['attributes'] += __attrib
            if data:
                return data
            result = {'found': None, 'type': None}
        if result['type'] is not None and len(result['type']) > 0:
            data = {'attributes': result['type']['attributes'], 'functions': result['type']['functions']}
        else:
            clazzes = sorted(set(self.patClass.findall(code)))
            funcs = sorted(set(self.patFunction.findall(code)))
            attrs = sorted(set(self.patWords.split(code)))
            if final_word in attrs:
                attrs.remove(final_word)
            if attr_name in attrs:
                attrs.remove(attr_name)
            filter_attrs = lambda x: x not in funcs and not str(x).isdigit() and x not in utils.KEYWORDS
            attrs = filter(filter_attrs, attrs)
            funcs = filter(lambda x: x not in clazzes, funcs)
            data = {'attributes': attrs, 'functions': funcs, 
               'classes': clazzes}
        return data