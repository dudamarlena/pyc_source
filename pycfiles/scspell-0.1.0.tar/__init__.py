# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/src/scspell-0.1/scspell_lib/__init__.py
# Compiled at: 2009-06-06 00:05:46
"""
scspell -- an interactive, conservative spell-checker for source code.
"""
from __future__ import with_statement
import os, re, sys, shutil
from bisect import bisect_left
import ConfigParser, _portable
from _corpus import CorporaFile
from _util import *
VERSION = '0.1.0'
CONFIG_SECTION = 'Settings'
CONTEXT_SIZE = 4
LEN_THRESHOLD = 3
CTRL_C = '\x03'
CTRL_D = '\x04'
CTRL_Z = '\x1a'
USER_DATA_DIR = _portable.get_data_dir('scspell')
DICT_DEFAULT_LOC = os.path.join(USER_DATA_DIR, 'dictionary.txt')
SCSPELL_DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data'))
SCSPELL_CONF = os.path.join(USER_DATA_DIR, 'scspell.conf')
token_regex = re.compile('(?<![^\\\\]\\\\)\\w+')
hex_regex = re.compile('0x[0-9a-fA-F]+')
us_regex = re.compile('[_\\d]+')
camel_word_regex = re.compile('([A-Z][a-z]*)')
file_id_regex = re.compile('scspell-id:[ \\t]*([a-zA-Z0-9_\\-]+)')

class MatchDescriptor(object):
    """A MatchDescriptor captures the information necessary to represent a token
    matched within some source code.
    """

    def __init__(self, text, matchobj):
        self._data = text
        self._pos = matchobj.start()
        self._token = matchobj.group()
        self._context = None
        self._line_num = None
        return

    def get_token(self):
        return self._token

    def get_string(self):
        """Get the entire string in which the match was found."""
        return self._data

    def get_ofs(self):
        """Get the offset within the string where the match is located."""
        return self._pos

    def get_prefix(self):
        """Get the string preceding this match."""
        return self._data[:self._pos]

    def get_remainder(self):
        """Get the string consisting of this match and all remaining characters."""
        return self._data[self._pos:]

    def get_context(self):
        """Compute the lines of context associated with this match, as a sequence of
        (line_num, line_string) pairs.
        """
        if self._context is not None:
            return self._context
        lines = self._data.split('\n')
        offsets = []
        for i in xrange(len(lines)):
            if i == 0:
                offsets.append(0)
            else:
                offsets.append(offsets[(i - 1)] + len(lines[(i - 1)]) + 1)

        for (i, ofs) in enumerate(offsets):
            if ofs > self._pos:
                self._line_num = i
                break

        if self._line_num is None:
            self._line_num = len(lines)
        self._context = [ (i + 1, line.strip('\r\n')) for (i, line) in enumerate(lines) if i + 1 - self._line_num in range(-CONTEXT_SIZE / 2, CONTEXT_SIZE / 2 + 1)
                        ]
        return self._context

    def get_line_num(self):
        """Computes the line number of the match."""
        if self._line_num is None:
            self.get_context()
        return self._line_num


def make_unique(items):
    """Remove duplicate items from a list, while preserving list order."""
    seen = set()

    def first_occurrence(i):
        if i not in seen:
            seen.add(i)
            return True
        return False

    return [ i for i in items if first_occurrence(i) ]


def decompose_token(token):
    """Divide a token into a list of strings of letters.

    Tokens are divided by underscores and digits, and capital letters will begin
    new subtokens.

    :param token: string to be divided
    :returns: sequence of subtoken strings
    """
    us_parts = us_regex.split(token)
    if ('').join(us_parts).isupper():
        subtokens = us_parts
    else:
        camelcase_parts = [ camel_word_regex.split(us_part) for us_part in us_parts ]
        subtokens = sum(camelcase_parts, [])
    return [ st.lower() for st in subtokens if st != '' ]


def handle_new_filetype(extension, dicts):
    """Handle creation of a new file-type for the given extension.
    
    :returns: True if created, False if canceled.
    """
    while True:
        descr = raw_input('            Enter a descriptive name for the programming language: ').strip()
        if descr == '':
            print '            (Canceled.)\n'
            return False
        if ':' in descr or ';' in descr:
            print '            Illegal characters in descriptive name.'
            continue
        if descr in dicts.get_filetypes():
            print '            That name is already in use.'
            continue
        dicts.new_filetype(descr, [extension])
        return True


def handle_new_extension(ext, dicts):
    """Handle creation of a new file-type extension.

    :returns: True if new extension was registered, False if canceled.
    """
    print '            Extension "%s" is not registered.  With which programming language\n            should "%s" be associated?' % (ext, ext)
    type_format = '               %3u: %s'
    filetypes = dicts.get_filetypes()
    for (i, ft) in enumerate(filetypes):
        print type_format % (i, ft)

    print type_format % (len(filetypes), '(Create new language file-type)')
    while True:
        selection = raw_input('            Enter number of desired file-type: ')
        if selection == '':
            print '            (Canceled.)\n'
            return False
        try:
            selection = int(selection)
        except ValueError:
            continue

        if selection == len(filetypes):
            return handle_new_filetype(ext, dicts)
        elif selection >= 0 and selection < len(filetypes):
            dicts.register_extension(ext, filetypes[selection])
            return True


def handle_add(unmatched_subtokens, filename, file_id, dicts):
    """Handle addition of one or more subtokens to a dictionary.

    :param unmatched_subtokens: sequence of subtokens, each of which failed spell check
    :param filename: name of file containing the token
    :param file_id: unique identifier for current file
    :type  file_id: string or None
    :param dicts: dictionary set against which to perform matching
    :type  dicts: CorporaFile
    :returns: True if subtokens were handled, False if canceled
    """
    (_, ext) = os.path.splitext(filename.lower())
    if file_id is None:
        if ext != '':
            prompt = "      Subtoken '%s':\n         (b)ack, (i)gnore, add to (p)rogramming language dictionary, or add to\n         (n)atural language dictionary? [i]"
        else:
            prompt = "      Subtoken '%s':\n         (b)ack, (i)gnore or add to (n)atural language dictionary? [i]"
    elif ext != '':
        prompt = "      Subtoken '%s':\n         (b)ack, (i)gnore, add to (p)rogramming language dictionary, add to\n         (f)ile-specific dictionary, or add to (n)atural language\n         dictionary? [i]"
    else:
        prompt = "      Subtoken '%s':\n         (b)ack, (i)gnore, add to (f)ile-specific dictionary, or add to\n         (n)atural language dictionary? [i]"
    for subtoken in unmatched_subtokens:
        while True:
            print prompt % subtoken
            ch = _portable.getch()
            if ch in (CTRL_C, CTRL_D, CTRL_Z):
                print 'User abort.'
                sys.exit(1)
            elif ch == 'b':
                print '         (Canceled.)\n'
                return False
            elif ch in ('i', '\r', '\n'):
                break
            elif ext != '' and ch == 'p':
                if dicts.add_by_extension(subtoken, ext):
                    break
                elif handle_new_extension(ext, dicts) and dicts.add_by_extension(subtoken, ext):
                    break
            elif ch == 'n':
                dicts.add_natural(subtoken)
                break
            elif file_id is not None and ch == 'f':
                dicts.add_by_fileid(subtoken, file_id)
                break

    return True


def handle_failed_check(match_desc, filename, file_id, unmatched_subtokens, dicts, ignores):
    """Handle a token which failed the spell check operation.

    :param match_desc: description of the token matching instance
    :type  match_desc: MatchDescriptor
    :param filename: name of file containing the token
    :param file_id: unique identifier for current file
    :type  file_id: string or None
    :param unmatched_subtokens: sequence of subtokens, each of which failed spell check
    :param dicts: dictionary set against which to perform matching
    :type  dicts: CorporaFile
    :param ignores: set of tokens to ignore for this session
    :returns: (text, ofs) where ``text`` is the (possibly modified) source contents and
            ``ofs`` is the byte offset within the text where searching shall resume.
    """
    token = match_desc.get_token()
    print "%s:%u: Unmatched '%s' --> {%s}" % (filename, match_desc.get_line_num(), token,
     (', ').join([ st for st in unmatched_subtokens ]))
    match_regex = re.compile(re.escape(match_desc.get_token()))
    while True:
        print '   (i)gnore, (I)gnore all, (r)eplace, (R)eplace all, (a)dd to dictionary, or\n   show (c)ontext? [i]'
        ch = _portable.getch()
        if ch in (CTRL_C, CTRL_D, CTRL_Z):
            print 'User abort.'
            sys.exit(1)
        elif ch in ('i', '\r', '\n'):
            break
        elif ch == 'I':
            ignores.add(token.lower())
            break
        elif ch in ('r', 'R'):
            replacement = raw_input("      Replacement text for '%s': " % token)
            if replacement == '':
                print '      (Canceled.)\n'
            else:
                ignores.add(replacement.lower())
                tail = re.sub(match_regex, replacement, match_desc.get_remainder(), 1 if ch == 'r' else 0)
                print
                return (match_desc.get_prefix() + tail, match_desc.get_ofs() + len(replacement))
        elif ch == 'a':
            if handle_add(unmatched_subtokens, filename, file_id, dicts):
                break
        elif ch == 'c':
            for ctx in match_desc.get_context():
                print '%4u: %s' % ctx

            print

    print
    return (
     match_desc.get_string(), match_desc.get_ofs() + len(match_desc.get_token()))


def spell_check_token(match_desc, filename, file_id, dicts, ignores):
    """Spell check a single token.

    :param match_desc: description of the token matching instance
    :type  match_desc: MatchDescriptor
    :param filename: name of file containing the token
    :param file_id: unique identifier for this file
    :type  file_id: string or None
    :param dicts: dictionary set against which to perform matching
    :type  dicts: CorporaFile
    :param ignores: set of tokens to ignore for this session
    :returns: (text, ofs) where ``text`` is the (possibly modified) source contents and
            ``ofs`` is the byte offset within the text where searching shall resume.
    """
    token = match_desc.get_token()
    if token.lower() not in ignores and hex_regex.match(token) is None:
        subtokens = decompose_token(token)
        unmatched_subtokens = [ st for st in subtokens if len(st) > LEN_THRESHOLD if not dicts.match(st, filename, file_id) if st not in ignores
                              ]
        if unmatched_subtokens != []:
            unmatched_subtokens = make_unique(unmatched_subtokens)
            return handle_failed_check(match_desc, filename, file_id, unmatched_subtokens, dicts, ignores)
    return (
     match_desc.get_string(), match_desc.get_ofs() + len(token))


def spell_check_file(filename, dicts, ignores):
    """Spell check a single file.

    :param filename: name of the file to check
    :param dicts: dictionary set against which to perform matching
    :type  dicts: CorporaFile
    :param ignores: set of tokens to ignore for this session
    """
    fq_filename = os.path.normcase(os.path.realpath(filename))
    try:
        with open(fq_filename, 'rb') as (source_file):
            source_text = source_file.read()
    except IOError, e:
        print 'Error: can\'t read source file "%s"; skipping.  (Reason: %s)' % (
         filename, str(e))
        return

    file_id = None
    m_id = file_id_regex.search(source_text)
    if m_id is not None:
        file_id = m_id.group(1)
        mutter(VERBOSITY_DEBUG, '(File contains id "%s".)' % file_id)
    data = source_text
    pos = 0
    while True:
        m = token_regex.search(data, pos)
        if m is None:
            break
        if m_id is not None and m.start() >= m_id.start() and m.start() < m_id.end():
            pos = m_id.end()
            continue
        (data, pos) = spell_check_token(MatchDescriptor(data, m), filename, file_id, dicts, ignores)

    if data != source_text:
        with open(fq_filename, 'wb') as (source_file):
            try:
                source_file.write(data)
            except IOError, e:
                print str(e)
                return

    return


def verify_user_data_dir():
    """Verify that the user data directory is present, or create one
    from scratch.
    """
    if not os.path.exists(USER_DATA_DIR):
        print 'Creating new personal dictionary in %s .\n' % USER_DATA_DIR
        os.makedirs(USER_DATA_DIR)
        shutil.copyfile(os.path.join(SCSPELL_DATA_DIR, 'dictionary.txt'), DICT_DEFAULT_LOC)


def locate_dictionary():
    """Load the location of the dictionary file.  This is either the default
    location, or an override specified in 'scspell.conf'.
    """
    verify_user_data_dir()
    try:
        f = open(SCSPELL_CONF, 'r')
    except IOError:
        return DICT_DEFAULT_LOC

    config = ConfigParser.RawConfigParser()
    try:
        try:
            config.readfp(f)
        except ConfigParser.ParsingError, e:
            print str(e)
            sys.exit(1)

    finally:
        f.close()

    try:
        loc = config.get(CONFIG_SECTION, 'dictionary')
        if os.path.isabs(loc):
            return loc
        else:
            print 'Error while parsing "%s": dictionary must be an absolute path.' % SCSPELL_CONF
            sys.exit(1)
    except ConfigParser.Error:
        return DICT_DEFAULT_LOC


def set_dictionary(filename):
    """Set the location of the dictionary to the specified filename.

    :returns: None
    """
    filename = os.path.realpath(os.path.expandvars(os.path.expanduser(filename)))
    verify_user_data_dir()
    config = ConfigParser.RawConfigParser()
    try:
        config.read(SCSPELL_CONF)
    except ConfigParser.ParsingError, e:
        print str(e)
        sys.exit(1)

    try:
        config.add_section(CONFIG_SECTION)
    except ConfigParser.DuplicateSectionError:
        pass

    config.set(CONFIG_SECTION, 'dictionary', filename)
    with open(SCSPELL_CONF, 'w') as (f):
        config.write(f)


def export_dictionary(filename):
    """Export the current keyword dictionary to the specified file.

    :returns: None
    """
    shutil.copyfile(locate_dictionary(), filename)


def spell_check(source_filenames, override_dictionary=None):
    """Run the interactive spell checker on the set of source_filenames.
    
    If override_dictionary is provided, it shall be used as a dictionary
    filename for this session only.

    :returns: None
    """
    verify_user_data_dir()
    dict_file = locate_dictionary() if override_dictionary is None else override_dictionary
    dict_file = os.path.expandvars(os.path.expanduser(dict_file))
    with CorporaFile(dict_file) as (dicts):
        ignores = set()
        for f in source_filenames:
            spell_check_file(f, dicts, ignores)

    return


__all__ = ['spell_check',
 'set_keyword_dict',
 'export_keyword_dict',
 'set_verbosity',
 'VERSION',
 'VERBOSITY_NORMAL',
 'VERBOSITY_MAX']