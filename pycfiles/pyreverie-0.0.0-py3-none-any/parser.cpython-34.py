# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/pyrev/parser.py
# Compiled at: 2017-02-20 23:06:33
# Size of source mod 2**32: 54287 bytes
import os, re, string
from logging import getLogger, NullHandler
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from functools import reduce
local_logger = getLogger(__name__)
local_logger.addHandler(NullHandler())
r_chap = re.compile('^(?P<level>={1,5})(?P<column>[column]?)(?P<sp>\\s*)(?P<title>.*)$')
r_end_block = re.compile('^//}(?P<junk>.*)$')
r_begin_block = re.compile('^(?P<prefix>//)(?P<content>.+)$')
r_manual_warn = re.compile('^#@(?P<type>.+)\\((?P<message>.+)\\)$')

class ParseProblem(Exception):

    def __init__(self, source_name, line_num, desc, raw_content):
        """
        source_name:
        line_num: can be None
        desc:
        raw_content: can be None, list, etc.
        """
        self.source_name = source_name
        self.line_num = line_num
        self.desc = desc
        self.raw_content = raw_content

    def __str__(self):
        if self.line_num:
            line = 'L{}'.format(self.line_num)
        else:
            line = 'L?'
        if self.raw_content:
            if type(self.raw_content) in [str, str]:
                content = '"{}"'.format(self.raw_content.rstrip())
            elif type(self.raw_content) == list:
                lst = []
                for rc_part in self.raw_content:
                    lst.append(rc_part.rstrip())

                content = '\n' + '\n'.join(lst)
        else:
            content = ''
        return '"{}" {} {}, content: {}'.format(self.source_name, line, self.desc, content)


class ParseError(ParseProblem):
    """ParseError"""
    LEVEL = ERROR


class ParseWarning(ParseProblem):
    """ParseWarning"""
    LEVEL = WARNING


class ParseInfo(ParseProblem):
    """ParseInfo"""
    LEVEL = INFO


class ParseDebug(ParseProblem):
    LEVEL = DEBUG


class ProblemReporter(object):
    """ProblemReporter"""

    def __init__(self, ignore_threshold, abort_threshold, logger=local_logger):
        self.problems = []
        self.ignore_threshold = ignore_threshold
        self.abort_threshold = abort_threshold
        self.logger = logger

    def report(self, error_level, source_name, line_num, desc, raw_content, logger=None):
        """
        Prepares an Exception (ParseProblem) most relevant
        to a given error_level.
        Remembers and returns it if it does not hit any threshold.
        Otherwise ignores it, or raises it appropriately.
        """
        logger = logger or self.logger
        if error_level < self.ignore_threshold:
            return
        if error_level >= ParseError.LEVEL:
            problem = ParseError(source_name, line_num, desc, raw_content)
        else:
            if error_level >= ParseWarning.LEVEL:
                problem = ParseWarning(source_name, line_num, desc, raw_content)
            else:
                if error_level >= ParseInfo.LEVEL:
                    problem = ParseInfo(source_name, line_num, desc, raw_content)
                else:
                    problem = ParseDebug(source_name, line_num, desc, raw_content)
            if error_level >= self.abort_threshold:
                raise problem
            else:
                self.problems.append(problem)
                return problem

    def error(self, source_name, line_num, desc, raw_content, logger=None):
        return self.report(ERROR, source_name, line_num, desc, raw_content, logger)

    def warning(self, source_name, line_num, desc, raw_content, logger=None):
        return self.report(WARNING, source_name, line_num, desc, raw_content, logger)

    def info(self, source_name, line_num, desc, raw_content, logger=None):
        return self.report(INFO, source_name, line_num, desc, raw_content, logger)

    def debug(self, source_name, line_num, desc, raw_content, logger=None):
        return self.desc(DEBUG, source_name, line_num, desc, raw_content, logger)


class Inline(object):

    def __init__(self, name, raw_content, line_num, position=None):
        self.name = name
        self.raw_content = raw_content
        self.line_num = line_num
        self.position = position

    def __str__(self):
        return 'name: "{}", L{} C{}, "{}"'.format(self.name, self.line_num, self.position, self.raw_content)


class Block(object):

    def __init__(self, name, params, has_content, lines, line_num):
        """
        has_content: True if the block has content and thus needs to be ended
                     with "//}" line. This is False typically with
                     "footnote", "label", etc.
        lines: a list of string(unicode) lines
        """
        self.name = name
        self.params = tuple(params)
        self.has_content = has_content
        self.lines = lines
        self.line_num = line_num

    def __str__(self):
        if self.has_content:
            return 'L{} "{}" {} (lines: {})'.format(self.line_num, self.name, self.params, len(self.lines))
        else:
            return 'L{} "{}" {} (no content)'.format(self.line_num, self.name, self.params)


class InlineStateMachine(object):
    """InlineStateMachine"""
    _inline_escape_allowed = set(['}', '\\'])
    ISM_NONE = 'ISM_NONE'
    ISM_AT = 'ISM_AT'
    ISM_INLINE_TAG = 'ISM_INLINE_TAG'
    ISM_END_INLINE_TAG = 'ISM_END_INLINE_TAG'
    ISM_INLINE_CONTENT = 'ISM_INLINE_CONTENT'
    ISM_INLINE_CONTENT_BS = 'ISM_INLINE_CONTENT_BS'
    ISM_INLINE_CONTENT_AT = 'ISM_INLINE_CONTENT_AT'

    def __init__(self, line_num, line, parser=None, reporter=None, source_name=None, logger=local_logger):
        """
        line: used when problem happened
        """
        self.line_num = line_num
        self.line = line
        self.logger = logger
        self.parser = parser
        self.reporter = reporter
        self.source_name = source_name
        self.reset()

    def reset(self):
        """
        Resets current parsing state.
        """
        self.unprocessed = []
        self.name = None
        self.state = self.ISM_NONE

    def _error(self, desc):
        self.reporter.error(self.source_name, self.line_num, desc, self.line)

    def _warning(self, desc):
        self.reporter.warning(self.source_name, self.line_num, desc, self.line)

    def _info(self, desc):
        self.reporter.info(self.source_name, self.line_num, desc, self.line)

    def parse_ch(self, ch, pos, logger=None):
        """
        Parses a single character.

        Returns None if this state machine is still parsing the content.
        In that case this object keeps the unresolved data.

        Returns an Inline object if inline parsing is finished.
        Returns a string (unicode) if the content is found to be non-inline,
        so the state machine consideres a caller should handle it.

        A caller must be responsible for returned not-None data since
        this object forgets about them.

        Obviously, this function should look like just returning
        ch as is, unless '@' is given.
        It is definitely an expected behavior.
        """
        logger = logger or self.logger
        assert type(ch) in [str, str] and len(ch) == 1
        ISM_NONE = self.ISM_NONE
        ISM_AT = self.ISM_AT
        ISM_INLINE_TAG = self.ISM_INLINE_TAG
        ISM_END_INLINE_TAG = self.ISM_END_INLINE_TAG
        ISM_INLINE_CONTENT = self.ISM_INLINE_CONTENT
        ISM_INLINE_CONTENT_AT = self.ISM_INLINE_CONTENT_AT
        ISM_INLINE_CONTENT_BS = self.ISM_INLINE_CONTENT_BS
        logger.debug(' C{} {} {}'.format(pos, self.state, ch))
        if self.state == ISM_NONE:
            if ch == '@':
                self.state = ISM_AT
                return
            else:
                if self.unprocessed:
                    ret = ''.join(self.unprocessed) + ch
                    self.reset()
                    return ret
                return ch
        else:
            if self.state == ISM_AT:
                if ch == '<':
                    assert len(self.unprocessed) == 0
                    self.state = ISM_INLINE_TAG
                    return
                else:
                    if ch == '@':
                        return '@'
                    self.reset()
                    return '@' + ch
            else:
                if self.state == ISM_INLINE_TAG:
                    if ch == '>':
                        assert self.unprocessed is not None
                        assert self.name is None
                        name = ''.join(self.unprocessed)
                        if len(name) == 0:
                            self._error('Empty inline name')
                        self.name = name
                        alnum = string.ascii_letters + string.digits
                        all_alnum = reduce(lambda x, y: x and y in alnum, self.name, True)
                        if not all_alnum:
                            self._error('Inline name "{}" has non-alnum'.format(self.name))
                        is_upper = lambda y: y in string.ascii_uppercase
                        has_uppercase = reduce(lambda x, y: x or is_upper(y), self.name, False)
                        if has_uppercase:
                            self._info('Inline name "{}" has uppercase'.format(self.name))
                        self.unprocessed = []
                        self.state = ISM_END_INLINE_TAG
                    else:
                        self.unprocessed.append(ch)
                    return
                if self.state == ISM_END_INLINE_TAG:
                    if ch == '{':
                        self.state = ISM_INLINE_CONTENT
                        return
                    else:
                        self._error('Wrong charactor at C{} ("{{" != "{}")'.format(pos, ch))
                        new_inline = Inline(self.name, '', self.line_num, pos)
                        if self.parser:
                            self.parser._inline_postparse_check(new_inline)
                        self.reset()
                        if ch == '@':
                            self.state = ISM_AT
                        else:
                            self.unprocessed.append(ch)
                            self.state = ISM_NONE
                        return new_inline
                else:
                    if self.state == ISM_INLINE_CONTENT:
                        if ch == '}':
                            content = ''.join(self.unprocessed)
                            new_inline = Inline(self.name, content, self.line_num, pos)
                            if self.parser:
                                self.parser._inline_postparse_check(new_inline)
                            self.reset()
                            return new_inline
                        else:
                            if ch == '@':
                                self.state = ISM_INLINE_CONTENT_AT
                                return
                            if ch == '\\':
                                self.state = ISM_INLINE_CONTENT_BS
                                return
                            self.unprocessed.append(ch)
                            return
                    else:
                        if self.state == ISM_INLINE_CONTENT_AT:
                            if ch == '}':
                                content = ''.join(self.unprocessed) + '@'
                                new_inline = Inline(self.name, content, self.line_num, pos)
                                if self.parser:
                                    self.parser._inline_postparse_check(new_inline)
                                self.reset()
                                return new_inline
                            else:
                                if ch == '<':
                                    self._info('Possible nested inline tag at C{}'.format(pos))
                                    self.unprocessed.append('@')
                                    self.unprocessed.append(ch)
                                    self.state = ISM_INLINE_CONTENT
                                    return
                                if ch == '@':
                                    self.unprocessed.append('@')
                                    return
                                self.unprocessed.append('@')
                                self.unprocessed.append(ch)
                                self.state == ISM_INLINE_CONTENT
                                return
                        elif self.state == ISM_INLINE_CONTENT_BS:
                            if ch in self._inline_escape_allowed:
                                self.unprocessed.append(ch)
                                self.state = ISM_INLINE_CONTENT
                                return
                            else:
                                self._info('Backslash inside inline "{}" is not effective toward "{}".'.format(self.name, ch))
                                self.unprocessed.append('\\')
                                self.unprocessed.append(ch)
                                self.state = ISM_INLINE_CONTENT
                                return
        logger.error('Unexpected state. line_num: {}, line: {}, pos: {}, state: {}'.format(self.line_num, self.line.rstrip(), pos, self.state))
        raise RuntimeError()

    def end(self):
        """
        Let the state machine handle the end of content.
        
        Returns remaining unprocessed content as a single string.
        Otherwise return None.
        """
        ISM_NONE = self.ISM_NONE
        ISM_AT = self.ISM_AT
        ISM_INLINE_TAG = self.ISM_INLINE_TAG
        ISM_END_INLINE_TAG = self.ISM_END_INLINE_TAG
        ISM_INLINE_CONTENT = self.ISM_INLINE_CONTENT
        ISM_INLINE_CONTENT_AT = self.ISM_INLINE_CONTENT_AT
        if self.state == ISM_NONE:
            assert not self.unprocessed
            return
        if self.state == ISM_AT:
            return '@'
        if self.state in [ISM_INLINE_TAG, ISM_END_INLINE_TAG,
         ISM_INLINE_CONTENT, ISM_INLINE_CONTENT_AT]:
            self._error('Invalid state')
        else:
            raise NotImplementedError()

    @classmethod
    def is_start_inline(cls, ch):
        return ch == '@'


class BlockStateMachine(object):
    BSM_NONE = 'BSM_NONE'
    BSM_PARSE_NAME = 'BSM_PARSE_NAME'
    BSM_IN_PARAM = 'BSM_IN_PARAM'
    BSM_IN_PARAM_BS = 'BSM_IN_PARAM_BS'
    BSM_END_PARAM = 'BSM_END_PARAM'
    BSM_IN_BLOCK = 'BSM_IN_BLOCK'

    def __init__(self, parser=None, reporter=None, source_name=None, logger=local_logger):
        self.logger = logger
        self.parser = parser
        self.reporter = reporter
        self.source_name = source_name
        self.all_inlines = []
        self.reset()

    def reset(self):
        self.state = self.BSM_NONE
        self.name = None
        self.start_line_num = None
        self.params = []
        self.lines = []
        self._unfinished_block = None

    def _remember_inline(self, inline):
        self.all_inlines.append(inline)
        if self.parser:
            self.parser._remember_inline(inline)

    def _error(self, line_num, desc, raw_content):
        self.reporter.error(self.source_name, line_num, desc, raw_content)

    def _warning(self, line_num, desc, raw_content):
        self.reporter.warning(self.source_name, line_num, desc, raw_content)

    def _info(self, line_num, desc, raw_content):
        self.reporter.info(self.source_name, line_num, desc, raw_content)

    def parse_line(self, line_num, line, logger=None):
        """
        Parses a single line.

        Returns None if this state machine is parsing the line.
        In that case this object keeps the unresolved content.

        Returns a Block object if block parsing is finished.

        Returns a string (unicode) if the content is found to be non-block.
        For the string, it will most likely same as the given "line".
        """
        logger = logger or self.logger
        BSM_NONE = self.BSM_NONE
        BSM_IN_BLOCK = self.BSM_IN_BLOCK
        assert self.state in [BSM_NONE, BSM_IN_BLOCK]
        rstripped = line.rstrip()
        m_end = r_end_block.match(rstripped)
        m_begin = r_begin_block.match(rstripped)
        if self.state == BSM_NONE:
            if m_end:
                self._error(line_num, 'Invalid block end', line)
        else:
            if m_begin:
                logger.debug('Block started at L{}'.format(line_num))
                prefix_len = len(m_begin.group('prefix'))
                content = m_begin.group('content').rstrip()
                ret = self._parse_block_start(line_num, line, content, prefix_len, logger)
                assert self.state in [BSM_NONE, BSM_IN_BLOCK], self.state
                if ret:
                    assert type(ret) == Block
                    self.reset()
                    return ret
                assert self.name is not None
                self.start_line_num = line_num
                return
            return line
        if self.state == BSM_IN_BLOCK:
            if m_end:
                logger.debug('Block "{}" ended at L{}'.format(self.name, line_num))
                if m_end.group('junk'):
                    self._error(line_num, 'Junk after block end.', line)
                new_block = self._unfinished_block
                assert new_block
                new_block.lines = self.lines
                if self.parser:
                    self.parser._block_lastline_check(new_block)
                self.reset()
                return new_block
            self.lines.append(line)
        else:
            raise NotImplementedError()

    def _parse_block_start(self, line_num, line, content, pos_start, logger=None):
        """
        Returns Block if the block ends in this line.
        (A typical example for it is footnote block.)
        Return None otherwise, which means we are still in a block.

        For instance, if the following line is available..

        //block[param1][param2]{
        
        .. then this function will handle '[param1][param2]{'
        """
        logger = logger or self.logger
        BSM_PARSE_NAME = self.BSM_PARSE_NAME
        BSM_IN_PARAM = self.BSM_IN_PARAM
        BSM_IN_PARAM_BS = self.BSM_IN_PARAM_BS
        BSM_END_PARAM = self.BSM_END_PARAM
        BSM_IN_BLOCK = self.BSM_IN_BLOCK

        def __bsm_name_end():
            assert self._tmp_lst is not None
            assert self.name is None, 'name: {}'.format(self.name)
            alnum = string.ascii_letters + string.digits
            name = ''.join(self._tmp_lst)
            self._tmp_lst = []
            if len(name) == 0:
                self._error(line_num, 'Empty block name', line)
            all_alnum = reduce(lambda x, y: x and y in alnum, name, True)
            if not all_alnum:
                reason = 'Block name "{}" contains non-alnum'.format(name)
                self._error(line_num, reason, line)
            has_uppercase = reduce(lambda x, y: x or y in string.ascii_uppercase, name, False)
            if has_uppercase:
                reason = 'Block name "{}" contains uppercase'.format(name)
                self._info(line_num, reason, line)
            self.name = name

        self._tmp_lst = []
        self._ism = InlineStateMachine(line_num, line, parser=self.parser, reporter=self.reporter, source_name=self.source_name, logger=logger)
        self.state = BSM_PARSE_NAME
        for pos, ch in enumerate(content, pos_start):
            logger.debug("C{} ({}) '{}'".format(pos, self.state, ch))
            if self.state == BSM_PARSE_NAME:
                if ch == '[':
                    _BlockStateMachine__bsm_name_end()
                    self.state = BSM_IN_PARAM
                else:
                    if ch == ']':
                        self._error(line_num, 'Invalid param end at C{}'.format(pos), line)
                        self.state = BSM_END_PARAM
                    else:
                        if ch == '{':
                            _BlockStateMachine__bsm_name_end()
                            self.state = BSM_IN_BLOCK
                            self._unfinished_block = Block(name=self.name, params=(), has_content=True, lines=[], line_num=line_num)
                            if self.parser:
                                self.parser._block_firstline_check(self._unfinished_block)
                        else:
                            self._tmp_lst.append(ch)
            elif self.state == BSM_IN_PARAM:
                if ch == ']':
                    if self._ism.state != InlineStateMachine.ISM_NONE:
                        self._error(line_num, "Inline is not finished while ']' is found at C{}".format(pos, ch), line)
                        ret = self._ism.parse_ch(ch, pos)
                        if ret is None:
                            pass
                        else:
                            if type(ret) is Inline:
                                self._remember_inline(ret)
                            else:
                                self._tmp_lst.append(ret)
                    else:
                        new_param = '{}{}'.format(''.join(self._tmp_lst), ''.join(self._ism.unprocessed))
                        self.params.append(new_param)
                        self._ism.reset()
                        self._tmp_lst = []
                        self.state = BSM_END_PARAM
                else:
                    if ch == '\\':
                        self.state = BSM_IN_PARAM_BS
                    else:
                        ret = self._ism.parse_ch(ch, pos)
                        if ret is None:
                            pass
                        else:
                            if type(ret) is Inline:
                                self._remember_inline(ret)
                            else:
                                self._tmp_lst.append(ret)
            elif self.state == BSM_IN_PARAM_BS:
                if ch == ']':
                    ret = self._ism.parse_ch(ch, pos)
                    if ret is None:
                        pass
                    else:
                        if type(ret) is Inline:
                            self._remember_inline(ret)
                        else:
                            self._tmp_lst.append(ret)
                else:
                    ret = self._ism.parse_ch('\\', pos)
                if ret is None:
                    pass
                else:
                    if type(ret) is Inline:
                        self._remember_inline(ret)
                    else:
                        self._tmp_lst.append(ret)
                    ret = self._ism.parse_ch(ch, pos)
                    if ret is None:
                        pass
                    else:
                        if type(ret) is Inline:
                            self._remember_inline(ret)
                        else:
                            self._tmp_lst.append(ret)
                        self.state = BSM_IN_PARAM
            elif self.state == BSM_END_PARAM:
                if ch == '[':
                    self._ism.reset()
                    self.state = BSM_IN_PARAM
                else:
                    if ch == '{':
                        self.state = BSM_IN_BLOCK
                        self._unfinished_block = Block(name=self.name, params=self.params, has_content=True, lines=[], line_num=line_num)
                        if self.parser:
                            self.parser._block_firstline_check(self._unfinished_block)
                    else:
                        desc = "Junk at C{} ('{}')".format(pos, ch)
                        self._error(line_num, desc, line)
            elif self.state == BSM_IN_BLOCK:
                desc = "Junk at C{} ('{}')".format(pos, ch)
                self._error(line_num, desc, line)
                continue

        if self._ism.state != InlineStateMachine.ISM_NONE:
            self._error(line_num, 'Inline is not finished.', line)
        elif self.state == BSM_PARSE_NAME:
            _BlockStateMachine__bsm_name_end()
            new_block = Block(name=self.name, params=(), has_content=False, lines=[], line_num=line_num)
            if self.parser:
                self.parser._block_firstline_check(new_block)
            self.reset()
            return new_block
        if self._tmp_lst:
            self._error(line_num, line, 'Unprocessed data is remaining ("{}")'.format(''.join(self._tmp_lst)))
        if self.state == BSM_END_PARAM:
            new_block = Block(name=self.name, params=self.params, has_content=False, lines=[], line_num=line_num)
            if self.parser:
                self.parser._block_firstline_check(new_block)
            self.reset()
            return new_block


class Parser(object):
    """Parser"""
    BM_TITLE = 'title'
    BM_LEVEL = 'level'
    BM_SOURCE_FILE_NAME = 'source_file_name'
    BM_SOURCE_CHAP_INDEX = 'source_chap_index'
    BM_SP = 'sp'
    BM_IS_COLUMN = 'is_column'

    def _error(self, line_num, desc, raw_content):
        self.reporter.error(self.source_name, line_num, desc, raw_content)

    def _warning(self, line_num, desc, raw_content):
        self.reporter.warning(self.source_name, line_num, desc, raw_content)

    def _info(self, line_num, desc, raw_content):
        self.reporter.info(self.source_name, line_num, desc, raw_content)

    def __init__(self, project=None, ignore_threshold=INFO, abort_threshold=CRITICAL, logger=local_logger):
        """
        project: a base project for this parser. Can be None, in which case
          no base project is available and some lint checks will not
          be executed (e.g. image existence in a project).
          parse_project() requires this.

        ignore_threshold: Specifies a lint-level which is minimum lint to be
          reported.
        abort_threshold: Specifies a lint-level which is minimum lint to be
          aborted.
        """
        self.project = project
        self.logger = logger
        self.ignore_threshold = ignore_threshold
        self.abort_threshold = abort_threshold

        def __block_exist(inline, block_names):
            if type(block_names) == str:
                block_names = (
                 block_names,)
            inline_id = inline.raw_content
            for block in self.all_blocks:
                if block.name in block_names and len(block.params) > 0 and block.params[0] == inline_id:
                    return

            self._error(inline.line_num, 'Inline for id "{}" found but no block for it.'.format(inline_id), None)

        def __list_block_exist(inline):
            _Parser__block_exist(inline, ['list', 'listnum'])

        def __image_block_exist(inline):
            _Parser__block_exist(inline, ['image'])

        def __image_file_exist(block):
            if not self.project:
                return
            assert block.name == 'image', block.name
            source_id, _ = os.path.splitext(self.source_name)
            image_id = block.params[0]
            imgs = self.project.images.get(self.source_name)
            if not imgs:
                self._error(block.line_num, 'Image file for image "{}" does not exist'.format(image_id), block.lines)
                return
            image_exist = reduce(lambda x, y: x or image_id == y.id, imgs, False)
            if not image_exist:
                image_id_wrong = reduce(lambda x, y: x or image_id == '{}-{}'.format(source_id, y.id), imgs, False)
                if image_id_wrong:
                    self._warning(block.line_num, '"{}" includes prefix ("{}-")'.format(image_id, source_id), block.lines)
                else:
                    self._error(block.line_num, 'Image file for image "{}" does not exist'.format(image_id), block.lines)

        def __check_block_default(block, num_params):
            if len(block.params) != num_params:
                self._error(block.line_num, 'Illegal number of params ("{}": {} > {})'.format(block.name, len(block.params), num_params), block.lines)

        def __check_param_num_range(block, num_params_min, num_params_max):
            err = None
            if len(block.params) < num_params_min:
                err = 'Illegal number of params ("{}": {} < {})'.format(block.name, len(block.params), num_params_min)
            elif len(block.params) > num_params_max:
                err = 'Illegal number of params ("{}": {} < {})'.format(block.name, num_params_max, len(block.params))
            if err:
                self._error(block.line_num, err, block.lines)

        cbd_0 = lambda block: _Parser__check_block_default(block, 0)
        cbd_1 = lambda block: _Parser__check_block_default(block, 1)
        cbd_2 = lambda block: _Parser__check_block_default(block, 2)
        cpnr_23 = lambda block: _Parser__check_param_num_range(block, 2, 3)
        self.allowed_inlines = {'list': (None, _Parser__list_block_exist),  'img': (
                 None, _Parser__image_block_exist), 
         'table': (None, None), 
         'href': (None, None), 
         'fn': (None, None), 
         'title': (None, None), 
         'ami': (None, None), 
         'chapref': (None, None), 
         'b': (None, None), 
         'i': (None, None), 
         'u': (None, None), 
         'm': (None, None), 
         'em': (None, None), 
         'kw': (None, None), 
         'tt': (None, None), 
         'tti': (None, None), 
         'ttb': (None, None), 
         'bou': (None, None), 
         'br': (None, None), 
         'code': (None, None), 
         'chap': (None, None), 
         'uchar': (None, None), 
         'raw': (None, None), 
         'comment': (None, None)}
        self.allowed_blocks = {'table': (None, cbd_2, None),  'list': (
                  None, cbd_2, None), 
         'emlist': (
                    None, cbd_1, None), 
         'listnum': (
                     None, cbd_2, None), 
         'image': (
                   _Parser__image_file_exist, cpnr_23, None), 
         'lead': (
                  None, cbd_0, None), 
         'footnote': (
                      None, cbd_2, None), 
         'noindent': (
                      None, cbd_0, None), 
         'cmd': (
                 None, cbd_0, None), 
         'indepimage': (
                        None, cbd_2, None), 
         'graph': (
                   None, cpnr_23, None), 
         'quote': (
                   None, cbd_0, None), 
         'bibpaper': (
                      None, cbd_2, None), 
         'texequation': (
                         None, cbd_0, None)}
        self.source_name = None
        self.reporter = ProblemReporter(ignore_threshold=INFO, abort_threshold=CRITICAL, logger=logger)
        self.chap_index = None
        self.bsm = None
        self.all_blocks = []
        self._current_inlines = []
        self.all_inlines = []
        self.footnote_pointers = []
        self.list_pointers = []
        self.bookmarks = []
        self.chap_to_bookmark = {}

    def parse_project(self):
        pass

    def parse_file(self, path, base_level, source_name, logger=None):
        logger = logger or self.logger
        f = None
        try:
            f = open(path, encoding='utf-8-sig')
            self._parse_file_inter(f, base_level, source_name, logger)
        finally:
            if f:
                f.close()

    def _parse_file_inter(self, f, base_level, source_name, logger=None):
        """
        content: file, or file-like object
        """
        logger = logger or self.logger
        self.source_name = source_name
        self.base_level = base_level
        self.bsm = BlockStateMachine(parser=self, reporter=self.reporter, source_name=self.source_name, logger=self.logger)
        self.chap_index = 0
        for line_num, line in enumerate(f, 1):
            self._parse_line(line_num, line)

        if self.bsm.state != BlockStateMachine.BSM_NONE:
            self._error(None, 'Block "{}" is not ended'.format(self.bsm.name), None)
        self._end_of_document()

    def _end_of_document(self):
        for inline in self._current_inlines:
            self._inline_endfile_check(inline)
            self.all_inlines.append(inline)

        self._current_inlines = []
        for block in self.all_blocks:
            self._block_endfile_check(block)

    def _parse_line(self, line_num, line, logger=None):
        logger = logger or self.logger
        BSM_IN_BLOCK = BlockStateMachine.BSM_IN_BLOCK
        rstripped = line.rstrip()
        logger.debug('_parse_line({}): {}'.format(self.bsm.state, rstripped))
        if self.bsm.state == BSM_IN_BLOCK:
            if rstripped[:3] == '#@#':
                self._info(line_num, line, 'Re:VIEW comment in block "{}". It will be included in the block'.format(self.bsm.name))
        elif rstripped[:2] == '#@':
            m = r_manual_warn.match(rstripped)
            if m:
                self._warning(line_num, 'Manual warning in block "{}": "{}". It will be included in the block'.format(self.bsm.name, m.group('message')), line)
        m = r_chap.match(rstripped)
        if m and not m.group('column') and not m.group('sp'):
            if not m.group('title').startswith('='):
                self._warning(line_num, 'Bookmark in block', line)
            ret = self.bsm.parse_line(line_num, line)
            if ret is None:
                pass
            elif type(ret) is Block:
                self.all_blocks.append(ret)
        else:
            if self._handle_chap(line_num, line):
                pass
            elif rstripped[:3] == '#@#':
                return
        if rstripped[:2] == '#@':
            m = r_manual_warn.match(rstripped)
            if m:
                if m.group('type') != 'warn':
                    self._error(line_num, line, 'Unknown warn-like operation "{}". May be "warn". Message: "{}"'.format(m.group('type'), m.group('message')))
                else:
                    self._warning(line_num, 'Manual warning "{}"'.format(m.group('message')), line)
                return
        else:
            if rstripped[:1] == '*':
                self._warning(line_num, 'Unordered list operator ("*") without a single space', line)
            else:
                if len(rstripped) > 1 and rstripped[0] in string.digits and rstripped[1] == '.':
                    self._warning(line_num, 'Ordered list operator ("{}") without a space'.format(rstripped[:2]), line)
                if not self.bookmarks:
                    self._info(line_num, 'No bookmark found yet', line)
                ret = self.bsm.parse_line(line_num, line)
                if type(ret) is Block:
                    self.all_blocks.append(ret)
                    return
                if ret is None:
                    return
                ism = InlineStateMachine(line_num, line, parser=self, reporter=self.reporter, source_name=self.source_name, logger=logger)
                for pos, ch in enumerate(rstripped):
                    ret = ism.parse_ch(ch, pos)
                    if ret is None:
                        continue
                        if type(ret) is Inline:
                            self._remember_inline(ret)
                            continue

                ism.end()

    def _append_bookmark(self, bookmark, logger=None):
        self.bookmarks.append(bookmark)
        bm_source_file_name = bookmark.get(self.BM_SOURCE_FILE_NAME)
        bm_chap_index = bookmark.get(self.BM_SOURCE_CHAP_INDEX)
        if bm_source_file_name and bm_chap_index is not None:
            key = (
             bm_source_file_name, bm_chap_index)
            self.chap_to_bookmark[key] = bookmark

    def _handle_chap(self, line_num, line, logger=None):
        logger = logger or self.logger
        rstripped = line.rstrip()
        m = r_chap.match(rstripped)
        if m:
            level = len(m.group('level'))
            is_column = bool(m.group('column'))
            sp = m.group('sp')
            title = m.group('title')
            if is_column:
                if not self.bookmarks:
                    pass
                if level == 1:
                    new_bookmark = {self.BM_LEVEL: self.base_level + level,  self.BM_TITLE: title.strip(), 
                     self.BM_SOURCE_FILE_NAME: self.source_name, 
                     self.BM_SOURCE_CHAP_INDEX: self.chap_index, 
                     self.BM_SP: sp, 
                     self.BM_IS_COLUMN: is_column}
                    self.chap_index += 1
            else:
                new_bookmark = {self.BM_LEVEL: self.base_level + level,  self.BM_TITLE: title.strip(), 
                 self.BM_SOURCE_FILE_NAME: self.source_name, 
                 self.BM_SOURCE_CHAP_INDEX: None, 
                 self.BM_SP: sp, 
                 self.BM_IS_COLUMN: is_column}
            self._append_bookmark(new_bookmark)
            return True
        else:
            return False

    def _format_bookmark(self, bookmark):
        return '{} "{}" (source: {}, index: {})'.format('=' * bookmark.get(self.BM_LEVEL, 10), bookmark[self.BM_TITLE], bookmark.get(self.BM_SOURCE_FILE_NAME), bookmark.get(self.BM_SOURCE_CHAP_INDEX))

    def _inline_postparse_check(self, inline):
        inline_checkers = self.allowed_inlines.get(inline.name)
        if not inline_checkers:
            self._error(inline.line_num, 'Undefined inline "{}" found at C{}'.format(inline.name, inline.position), inline.raw_content)
        elif inline_checkers[0]:
            postparse_checker = inline_checkers[0]
            postparse_checker(inline)

    def _inline_endfile_check(self, inline):
        inline_checkers = self.allowed_inlines.get(inline.name)
        if inline_checkers and inline_checkers[1]:
            endfile_checker = inline_checkers[1]
            endfile_checker(inline)

    def _block_firstline_check(self, block):
        block_checkers = self.allowed_blocks.get(block.name)
        if not block_checkers:
            self._error(block.line_num, 'Undefined block "{}" found'.format(block.name), block.lines)
        elif block_checkers[0]:
            firstline_checker = block_checkers[0]
            firstline_checker(block)

    def _block_lastline_check(self, block):
        block_checkers = self.allowed_blocks.get(block.name)
        if block_checkers and block_checkers[1]:
            lastline_checker = block_checkers[1]
            lastline_checker(block)

    def _block_endfile_check(self, block):
        block_checkers = self.allowed_blocks.get(block.name)
        if block_checkers and block_checkers[2]:
            endfile_checker = block_checkers[2]
            endfile_checker(block)

    def _remember_inline(self, inline):
        self._current_inlines.append(inline)

    def _dump_problems(self, dump_func=None):
        dump_func = dump_func or (lambda x: self.logger.debug(x))
        if not self.reporter:
            dump_func('No reporter')
            return
        if self.reporter.problems:
            dump_func('Problems:')
            problems = self.reporter.problems
            for problem in problems:
                problem_name = type(problem).__name__[5]
                if problem.raw_content:
                    if type(problem.raw_content) in [str, str]:
                        content = '"{}"'.format(problem.raw_content.rstrip())
                    elif type(problem.raw_content) == list:
                        lst = []
                        for rc_part in problem.raw_content:
                            lst.append(rc_part.rstrip())

                        content = '\n' + '\n'.join(lst)
                else:
                    content = ''
                if problem.source_name:
                    dump_func(' [{}] {} L{}: {}'.format(problem_name, problem.source_name, problem.line_num, problem.desc))
                else:
                    dump_func(' [{}] L{}: {}'.format(problem_name, problem.line_num, problem.desc))

        else:
            dump_func('No problem')

    def _dump_blocks(self, dump_func=None):
        dump_func = dump_func or (lambda x: self.logger.debug(x))
        if self.all_blocks:
            dump_func('All-Blocks:')
            for block in self.all_blocks:
                dump_func(str(block))

        else:
            dump_func('No block')

    def _dump_inlines(self, dump_func=None):
        dump_func = dump_func or (lambda x: self.logger.debug(x))
        if self.all_inlines:
            dump_func('All-Inlines:')
            for inline in self.all_inlines:
                dump_func(' L{} name: "{}", "{}"'.format(inline.line_num, inline.name, inline.raw_content))

        else:
            dump_func('No inline')

    def _dump(self, dump_func=None):
        """
        Dump current state.
        dump_func is expected to accept an arg for each line.
        If there's no dump_func, self.logger.debug() will be used
        """
        dump_func = dump_func or (lambda x: self.logger.debug(x))
        if self.bookmarks:
            dump_func('Bookmarks:')
            for i, bookmark in enumerate(self.bookmarks):
                dump_func(' {}:{}'.format(i, self._format_bookmark(bookmark)))

        else:
            dump_func('No bookmark')
        if self.chap_to_bookmark:
            dump_func('chap_to_bookmark:')
            for key in sorted(self.chap_to_bookmark.keys()):
                bookmark = self.chap_to_bookmark[key]
                dump_func(' {}: "{}"'.format(key, bookmark[self.BM_TITLE]))

        self._dump_blocks(dump_func)
        self._dump_inlines(dump_func)
        self._dump_problems(dump_func)