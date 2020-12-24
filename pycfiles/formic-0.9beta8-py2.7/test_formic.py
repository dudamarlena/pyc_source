# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/formic/test_formic.py
# Compiled at: 2013-07-14 08:37:12
"""Tests on formic"""
from formic import get_version, MatchType, Matcher, ConstantMatcher, FNMatcher, FormicError, Section, Pattern, PatternSet, FileSetState, FileSet, get_path_components, reconstitute_path, walk_from_list, get_path_components
import pytest, os

def create_starstar(glob):
    ps = Pattern.create(glob)
    for pattern in ps.patterns:
        if pattern.file_pattern == '*':
            pattern_dir = pattern
        else:
            pattern_file = pattern

    return (
     pattern_dir, pattern_file)


def match(matcher, original, expected):
    matched = set()
    unmatched = set(original)
    matcher.match_files(matched, unmatched)
    assert set(expected) == matched
    assert unmatched == set(original) - matched


NOT_PRESENT = -1
MATCHED_INHERIT = 0
MATCHED_AND_SUBDIR = 1
MATCHED_NO_SUBDIR = 2
UNMATCHED = 3

def file_set_state_location--- This code section failed: ---

 L.  53         0  LOAD_CONST               'MATCHED_INHERIT'
                3  LOAD_CONST               'MATCHED_AND_SUBDIR'
                6  LOAD_CONST               'MATCHED_NO_SUBDIR'
                9  LOAD_CONST               'UNMATCHED'
               12  BUILD_LIST_4          4 
               15  STORE_FAST            3  'msg'

 L.  54        18  LOAD_FAST             0  'file_set_state'
               21  LOAD_ATTR             0  'matched_inherit'
               24  LOAD_ATTR             1  'patterns'

 L.  55        27  LOAD_FAST             0  'file_set_state'
               30  LOAD_ATTR             2  'matched_and_subdir'
               33  LOAD_ATTR             1  'patterns'

 L.  56        36  LOAD_FAST             0  'file_set_state'
               39  LOAD_ATTR             3  'matched_no_subdir'
               42  LOAD_ATTR             1  'patterns'

 L.  57        45  LOAD_FAST             0  'file_set_state'
               48  LOAD_ATTR             4  'unmatched'
               51  LOAD_ATTR             1  'patterns'
               54  BUILD_LIST_4          4 
               57  STORE_FAST            4  'locations'

 L.  58        60  BUILD_LIST_0          0 
               63  LOAD_FAST             4  'locations'
               66  GET_ITER         
               67  FOR_ITER             18  'to 88'
               70  STORE_FAST            5  'patterns'
               73  LOAD_FAST             1  'pattern'
               76  LOAD_FAST             5  'patterns'
               79  COMPARE_OP            6  in
               82  LIST_APPEND           2  None
               85  JUMP_BACK            67  'to 67'
               88  STORE_FAST            6  'found'

 L.  59        91  LOAD_GLOBAL           5  'len'
               94  BUILD_LIST_0          0 
               97  LOAD_FAST             6  'found'
              100  GET_ITER         
              101  FOR_ITER             18  'to 122'
              104  STORE_FAST            7  'b'
              107  LOAD_FAST             7  'b'
              110  POP_JUMP_IF_FALSE   101  'to 101'
              113  LOAD_FAST             7  'b'
              116  LIST_APPEND           2  None
              119  JUMP_BACK           101  'to 101'
              122  CALL_FUNCTION_1       1  None
              125  STORE_FAST            8  'count'

 L.  60       128  LOAD_FAST             8  'count'
              131  LOAD_CONST               0
              134  COMPARE_OP            2  ==
              137  POP_JUMP_IF_FALSE   185  'to 185'

 L.  61       140  LOAD_FAST             2  'location'
              143  LOAD_GLOBAL           6  'NOT_PRESENT'
              146  COMPARE_OP            2  ==
              149  POP_JUMP_IF_FALSE   155  'to 155'

 L.  62       152  JUMP_ABSOLUTE       381  'to 381'

 L.  64       155  LOAD_GLOBAL           7  'False'
              158  POP_JUMP_IF_TRUE    381  'to 381'
              161  LOAD_ASSERT              AssertionError
              164  LOAD_CONST               '{0} was not found anywhere in {1}'
              167  LOAD_ATTR             9  'format'
              170  LOAD_FAST             1  'pattern'
              173  LOAD_FAST             0  'file_set_state'
              176  CALL_FUNCTION_2       2  None
              179  RAISE_VARARGS_2       2  None
              182  JUMP_FORWARD        196  'to 381'

 L.  65       185  LOAD_FAST             8  'count'
              188  LOAD_CONST               1
              191  COMPARE_OP            4  >
              194  POP_JUMP_IF_FALSE   230  'to 230'

 L.  66       197  LOAD_GLOBAL           7  'False'
              200  POP_JUMP_IF_TRUE    381  'to 381'
              203  LOAD_ASSERT              AssertionError
              206  LOAD_CONST               '{0} was found in {1} locations in {2}'
              209  LOAD_ATTR             9  'format'
              212  LOAD_FAST             1  'pattern'
              215  LOAD_FAST             8  'count'
              218  LOAD_FAST             0  'file_set_state'
              221  CALL_FUNCTION_3       3  None
              224  RAISE_VARARGS_2       2  None
              227  JUMP_FORWARD        151  'to 381'

 L.  68       230  SETUP_LOOP           37  'to 270'
              233  LOAD_GLOBAL          10  'range'
              236  LOAD_CONST               0
              239  LOAD_CONST               4
              242  CALL_FUNCTION_2       2  None
              245  GET_ITER         
              246  FOR_ITER             20  'to 269'
              249  STORE_FAST            9  'i'

 L.  69       252  LOAD_FAST             6  'found'
              255  LOAD_FAST             9  'i'
              258  BINARY_SUBSCR    
              259  POP_JUMP_IF_FALSE   246  'to 246'

 L.  70       262  BREAK_LOOP       
              263  JUMP_BACK           246  'to 246'
              266  JUMP_BACK           246  'to 246'
              269  POP_BLOCK        
            270_0  COME_FROM           230  '230'

 L.  71       270  LOAD_FAST             2  'location'
              273  LOAD_GLOBAL           6  'NOT_PRESENT'
              276  COMPARE_OP            2  ==
              279  POP_JUMP_IF_FALSE   322  'to 322'

 L.  72       282  LOAD_GLOBAL           7  'False'
              285  POP_JUMP_IF_TRUE    381  'to 381'
              288  LOAD_ASSERT              AssertionError
              291  LOAD_CONST               '{0} was in {1} but should have been NOT PRESENT for path {2}'
              294  LOAD_ATTR             9  'format'

 L.  73       297  LOAD_FAST             1  'pattern'
              300  LOAD_FAST             3  'msg'
              303  LOAD_FAST             9  'i'
              306  BINARY_SUBSCR    
              307  LOAD_FAST             0  'file_set_state'
              310  LOAD_ATTR            11  'path_elements'
              313  CALL_FUNCTION_3       3  None
              316  RAISE_VARARGS_2       2  None
              319  JUMP_FORWARD         59  'to 381'

 L.  76       322  LOAD_FAST             9  'i'
              325  LOAD_FAST             2  'location'
              328  COMPARE_OP            3  !=
              331  POP_JUMP_IF_FALSE   381  'to 381'

 L.  77       334  LOAD_GLOBAL           7  'False'
              337  POP_JUMP_IF_TRUE    381  'to 381'
              340  LOAD_ASSERT              AssertionError
              343  LOAD_CONST               '{0} was in {1} but should have been in {2} for path {3}'
              346  LOAD_ATTR             9  'format'

 L.  78       349  LOAD_FAST             1  'pattern'
              352  LOAD_FAST             3  'msg'
              355  LOAD_FAST             9  'i'
              358  BINARY_SUBSCR    
              359  LOAD_FAST             3  'msg'
              362  LOAD_FAST             2  'location'
              365  BINARY_SUBSCR    
              366  LOAD_FAST             0  'file_set_state'
              369  LOAD_ATTR            11  'path_elements'
              372  CALL_FUNCTION_4       4  None
              375  RAISE_VARARGS_2       2  None
              378  JUMP_FORWARD          0  'to 381'
            381_0  COME_FROM           378  '378'
            381_1  COME_FROM           319  '319'
            381_2  COME_FROM           227  '227'
            381_3  COME_FROM           182  '182'

Parse error at or near `COME_FROM' instruction at offset 381_2


def find_count(directory, pattern):
    """Platform-detecting way to count files matching a pattern"""
    if os.name == 'posix':
        return find_count_posix(directory, pattern)
    if os.name == 'nt':
        return find_count_dos(directory, pattern)
    raise Exception('System is neither Posix not Windows')


def find_count_posix(directory, pattern):
    """Runs Unix find command on a directory counting how many files match
    the specified pattern"""
    if pattern is None:
        pattern = '*'
    import subprocess
    process = subprocess.Popen(['find', str(directory), '-type', 'f', '-name', str(pattern)], stdout=subprocess.PIPE)
    lines = 0
    while True:
        line = process.stdout.readline()
        if line:
            lines += 1
        else:
            break

    print 'find', directory, '-type f -name', pattern, ': found', lines, 'files'
    return lines


def find_count_dos(directory, pattern):
    """Runs DOS dir /s command on a directory counting how many files match
    the specified pattern"""
    if pattern is None:
        pattern = '*.*'
    import subprocess
    process = subprocess.Popen(['dir', str(os.path.join(directory, pattern)), '/s', '/a-d', '/b'], stdout=subprocess.PIPE, shell=True)
    lines = 0
    while True:
        line = process.stdout.readline()
        if line:
            lines += 1
        else:
            break

    print 'dir', str(os.path.join(directory, pattern)), '/s : found', lines, 'files'
    return lines


def get_test_directory():
    """Return a platform-suitable directory for bulk-testing"""
    if os.name == 'posix':
        return '/usr'
    if os.name == 'nt':
        return 'C:\\WINDOWS'
    raise Exception('System is neither Posix not Windows')


def formic_count(directory, pattern):
    if pattern is None:
        pattern = '*'
    fs = FileSet(directory=directory, include='/**/' + pattern, default_excludes=False, symlinks=False)
    lines = sum(1 for file in fs.files())
    print 'FileSet found', lines, 'files'
    return lines


def compare_find_and_formic(directory, pattern=None):
    """Runs find and formic on the same directory with the same file pattern;
    both approaches should return the same number of files."""
    assert find_count(directory, pattern) == formic_count(directory, pattern)


def test_path_components():
    d = os.getcwd() + os.path.sep
    drive, folders = get_path_components(d)
    if os.name == 'nt':
        assert drive is not None
        assert d.startswith(drive)
        reconst = reconstitute_path(drive, folders)
        assert d.startswith(reconst)
        assert reconst.endswith(os.path.sep) is False
        drive2, folders2 = get_path_components(drive + os.path.sep)
        assert drive2 == drive
        assert folders2 == []
        reconst = reconstitute_path(drive2, folders2)
        assert reconst.endswith(os.path.sep)
    else:
        assert drive == ''
        reconst = os.path.join(os.path.sep, *folders)
        print d, reconst
        assert d.startswith(reconst)
        assert reconst.endswith(os.path.sep) is False
        drive2, folders2 = get_path_components(os.path.sep)
        assert drive2 == ''
        assert folders2 == []
        reconst = reconstitute_path(drive2, folders2)
        assert reconst.endswith(os.path.sep)
    return


class TestMatchers(object):

    def test_basic(self):
        assert Matcher('test') == Matcher('test')
        assert Matcher('a') != Matcher('b')
        assert isinstance(Matcher.create('a'), ConstantMatcher)
        assert Matcher.create('a').match('a')
        assert not Matcher.create('a').match('b')
        assert Matcher.create('a') == Matcher.create('a')
        assert Matcher.create('test') == Matcher.create('test')
        assert isinstance(Matcher.create('a*'), FNMatcher)
        assert Matcher.create('a*').match('abc')
        assert Matcher.create('a*').match('ape')
        assert not Matcher.create('a*').match('bbc')
        assert Matcher.create('a?').match('ab')
        assert not Matcher.create('a?').match('ba')


class TestSections(object):

    def test_basic(self):
        s = Section(['test'])
        assert s.str == 'test'
        assert s.elements[0] == ConstantMatcher('test')
        s = Section(['test', 'bin'])
        assert s.str == 'test/bin'
        assert s.elements[0] == ConstantMatcher('test')
        assert s.elements[1] == ConstantMatcher('bin')
        s = Section(['????', 'test', 'bin'])
        assert s.str == '????/test/bin'
        assert s.elements[0] == FNMatcher('????')
        assert s.elements[1] == ConstantMatcher('test')
        assert s.elements[2] == ConstantMatcher('bin')

    def test_match_single_no_bindings(self):
        s = Section(['test'])
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [1] == matches
        path = ('not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/util/bin/test/last/test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [1, 4, 6] == matches
        path = ('not/util/bin/test/last/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [4] == matches

    def test_match_single_bound_start(self):
        s = Section(['test'])
        s.bound_start = True
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [1] == matches
        path = ('not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/util/bin/test/last/test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [1] == matches
        path = ('not/util/bin/test/last/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches

    def test_match_single_bound_end(self):
        s = Section(['test'])
        s.bound_end = True
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [1] == matches
        path = ('not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/util/bin/test/last/test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [6] == matches
        path = ('not/util/bin/test/last/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches

    def test_match_twin_elements_no_bindings(self):
        s = Section(['test', 'a*'])
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/bin').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/andrew').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2, 5, 7] == matches
        path = ('not/util/bin/test/ast/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [5] == matches

    def test_match_twin_elements_bound_start(self):
        s = Section(['test', 'a*'])
        s.bound_start = True
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/bin').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/andrew').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2] == matches
        path = ('not/util/bin/test/ast/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches

    def test_match_twin_elements_bound_end(self):
        s = Section(['test', 'a*'])
        s.bound_end = True
        path = []
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/bin').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/andrew').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [7] == matches
        path = ('not/util/bin/test/ast/not').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches

    def test_single_match_not_beginning(self):
        s = Section(['test'])
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 2) ]
        assert [4, 6] == matches
        matches = [ index for index in s.match_iter(path, 3) ]
        assert [4, 6] == matches
        matches = [ index for index in s.match_iter(path, 4) ]
        assert [6] == matches
        matches = [ index for index in s.match_iter(path, 5) ]
        assert [6] == matches
        matches = [ index for index in s.match_iter(path, 6) ]
        assert [] == matches
        matches = [ index for index in s.match_iter(path, 7) ]
        assert [] == matches
        matches = [ index for index in s.match_iter(path, 8) ]
        assert [] == matches

    def test_multi_match_not_beginning(self):
        s = Section(['test', 'a*'])
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 1) ]
        assert [] == matches
        path = ('test/andrew').split('/')
        matches = [ index for index in s.match_iter(path, 1) ]
        assert [] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 2) ]
        assert [5, 7] == matches
        matches = [ index for index in s.match_iter(path, 3) ]
        assert [5, 7] == matches
        matches = [ index for index in s.match_iter(path, 4) ]
        assert [7] == matches
        matches = [ index for index in s.match_iter(path, 5) ]
        assert [7] == matches
        matches = [ index for index in s.match_iter(path, 6) ]
        assert [] == matches
        matches = [ index for index in s.match_iter(path, 7) ]
        assert [] == matches
        matches = [ index for index in s.match_iter(path, 8) ]
        assert [] == matches

    def test_match_bound_start(self):
        s = Section(['test', 'a*'])
        s.bound_start = True
        path = ('test').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 0) ]
        assert [2] == matches
        path = ('test/andrew/bin/test/ast/test/another').split('/')
        matches = [ index for index in s.match_iter(path, 1) ]
        assert [] == matches


class TestPattern(object):

    def test_illegal_glob(self):
        with pytest.raises(FormicError):
            Pattern.create('/test/../**')

    def test_glob_with_pointless_curdir(self):
        simple = ['**', 'test', 'test']
        assert simple == Pattern._simplify(['**', '.', 'test', 'test'])
        assert simple == Pattern._simplify(['**', 'test', '.', 'test'])
        assert simple == Pattern._simplify(['**', 'test', 'test', '.'])
        assert simple == Pattern._simplify(['**', '**', 'test', 'test'])
        assert simple == Pattern._simplify(['**', '**', '**', 'test', 'test'])
        simple = [
         '**', 'test', '**', 'test']
        assert simple == Pattern._simplify(['**', 'test', '**', '**', 'test'])

    def test_compilation_and_str(self):
        patterns = {'/*.py': ['/*.py'], '/test/*.py': [
                        '/test/*.py'], 
           '/test/dir/**/*': [
                            '/test/dir/**/*'], 
           '/start/**/test/*.py': [
                                 '/start/**/test/*.py'], 
           '/start/**/test/**/*.py': [
                                    '/start/**/test/**/*.py'], 
           '**/test/*.py': [
                          'test/*.py', '**/test/*.py'], 
           '**/test/*': [
                       'test/*', '**/test/*'], 
           '**/test/**/*': [
                          'test/**/*', '**/test/**/*'], 
           '**/test/**/*.py': [
                             'test/**/*.py', '**/test/**/*.py'], 
           '**/start/**/test/**/*.py': [
                                      'start/**/test/**/*.py', '**/start/**/test/**/*.py']}
        for normative, options in patterns.iteritems():
            for option in options:
                print ("Testing that Pattern.create('{0}') == '{1}'").format(option, normative)
                assert normative == str(Pattern.create(option))

    def test_compilation_and_str_starstar(self):
        for glob in ['test/', '/test/', '/test/**/', '/test/**', '/1/**/test/']:
            patternset = Pattern.create(glob)
            assert isinstance(patternset, PatternSet)
            assert len(patternset.patterns) == 2
            for pattern in patternset.patterns:
                assert pattern.file_pattern == 'test' or pattern.sections[(-1)].elements[(-1)].pattern == 'test'

    def test_compilation_bound_start(self):
        p = Pattern.create('/*.py')
        assert p.bound_start is True
        assert p.bound_end is True
        assert str(p.file_pattern) == '*.py'
        assert p.sections == []
        p = Pattern.create('/test/*.py')
        assert p.bound_start is True
        assert p.bound_end is True
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('/test/dir/*')
        assert p.bound_start is True
        assert p.bound_end is True
        assert p.file_pattern == '*'
        assert p.sections == [Section(['test', 'dir'])]
        p = Pattern.create('/start/**/test/*.py')
        assert p.bound_start is True
        assert p.bound_end is True
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['start']), Section(['test'])]
        p = Pattern.create('/start/**/test/**/*.py')
        assert p.bound_start is True
        assert p.bound_end is False
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['start']), Section(['test'])]

    def test_compilation_unbound_start(self):
        p = Pattern.create('*.py')
        assert p.bound_start is False
        assert p.bound_end is False
        assert str(p.file_pattern) == '*.py'
        assert p.sections == []
        p = Pattern.create('test/*.py')
        assert p.bound_start is False
        assert p.bound_end is True
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('**/test/*.py')
        assert p.bound_start is False
        assert p.bound_end is True
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('**/test/**/*')
        assert p.bound_start is False
        assert p.bound_end is False
        assert p.file_pattern == '*'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('**/test/*')
        assert p.bound_start is False
        assert p.bound_end is True
        assert p.file_pattern == '*'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('**/test/**/*.py')
        assert p.bound_start is False
        assert p.bound_end is False
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['test'])]
        p = Pattern.create('start/**/test/**/*.py')
        assert p.bound_start is False
        assert p.bound_end is False
        assert str(p.file_pattern) == '*.py'
        assert p.sections == [Section(['start']), Section(['test'])]

    def test_complex_compilation(self):
        p1 = Pattern.create('dir/file.txt')
        p2 = Pattern.create('**/dir/file.txt')
        p3 = Pattern.create('/**/dir/file.txt')
        assert p1.sections == p2.sections
        assert p2.sections == p3.sections
        assert p1.bound_start is False
        assert p1.bound_start == p2.bound_start == p3.bound_start
        assert p1.bound_end == True
        assert p1.bound_end == p2.bound_end == p3.bound_end

    def test_match_pure_file_pattern(self):
        p = Pattern.create('test.py')
        assert p.match_directory([]) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p.match_directory(('test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p.match_directory(('some/where/').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES

    def test_match_bound_start_file_pattern(self):
        p = Pattern.create('/test.py')
        assert p.match_directory([]) == MatchType.MATCH_BUT_NO_SUBDIRECTORIES
        assert p.match_directory(('test').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p.match_directory(('test/sub/').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p.match_directory(('some/where/').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES

    def test_match_single_bound_start_no_sub(self):
        p = Pattern.create('/test/*.py')
        assert p.match_directory([]) == MatchType.NO_MATCH
        assert p.match_directory(('test').split('/')) == MatchType.MATCH_BUT_NO_SUBDIRECTORIES
        assert p.match_directory(('some/where/').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES

    def test_match_single_bound_start_any_sub(self):
        p = Pattern.create('/test/**/*')
        assert p.match_directory([]) == MatchType.NO_MATCH
        assert p.match_directory(('test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p.match_directory(('some/where/test').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p.match_directory(('some/where/').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES

    def test_match_single_unbound_directory(self):
        p_dir, p_file = create_starstar('test/')
        assert p_dir.match_directory([]) == MatchType.NO_MATCH
        assert p_dir.match_directory(('test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('some/where/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('middle/test/middle').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH
        unmatched = set(['1', '2', '3', 'test'])
        matched = set()
        p_file.match_files(matched, unmatched)
        assert len(matched) == 1
        assert 'test' in matched
        assert len(unmatched) == 3
        assert 'test' not in unmatched
        p_dir.match_files(matched, unmatched)
        assert len(matched) == 4
        assert len(unmatched) == 0
        p_dir, p_file = create_starstar('**/test/**')
        assert p_dir.match_directory([]) == MatchType.NO_MATCH
        assert p_dir.match_directory(('test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('some/where/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('middle/test/middle').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH
        unmatched = set(['1', '2', '3', 'test'])
        matched = set()
        p_file.match_files(matched, unmatched)
        assert len(matched) == 1
        assert 'test' in matched
        assert len(unmatched) == 3
        assert 'test' not in unmatched
        p_dir.match_files(matched, unmatched)
        assert len(matched) == 4
        assert len(unmatched) == 0

    def test_match_single_bound_end_directory(self):
        p = Pattern.create('test/*')
        assert p.match_directory([]) == MatchType.NO_MATCH
        assert p.match_directory(('test').split('/')) == MatchType.MATCH
        assert p.match_directory(('some/where/test').split('/')) == MatchType.MATCH
        assert p.match_directory(('middle/test/middle').split('/')) == MatchType.NO_MATCH
        assert p.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH

    def test_match_twin_unbound_directories(self):
        p_dir, p_file = create_starstar('some/**/test/')
        assert p_dir.match_directory([]) == MatchType.NO_MATCH
        assert p_dir.match_directory(('test/test/test/test').split('/')) == MatchType.NO_MATCH
        assert p_dir.match_directory(('some/some/some').split('/')) == MatchType.NO_MATCH
        assert p_dir.match_directory(('some/where/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('a/some/where/test/b').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('some/where/else/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('some/where/a/long/way/apart/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH
        unmatched = set(['1', '2', '3', 'test'])
        matched = set()
        p_file.match_files(matched, unmatched)
        assert len(matched) == 1
        assert 'test' in matched
        assert len(unmatched) == 3
        assert 'test' not in unmatched
        p_dir.match_files(matched, unmatched)
        assert len(matched) == 4
        assert len(unmatched) == 0

    def test_match_twin_directories(self):
        p_dir, p_file = create_starstar('/test/**/test/')
        assert p_dir.match_directory(('test/test/test/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('test/where/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('test/a/very/long/way/apart/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory([]) == MatchType.NO_MATCH
        assert p_dir.match_directory(('test').split('/')) == MatchType.NO_MATCH
        assert p_dir.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p_dir.match_directory(('a/test/where/test/b').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p_dir.match_directory(('some/some/some').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        p = Pattern.create('/test/**/test/*.py')
        assert p.match_directory(('test/test/test/test').split('/')) == MatchType.MATCH
        assert p.match_directory(('test/where/test').split('/')) == MatchType.MATCH
        assert p.match_directory(('test/a/very/long/way/apart/test').split('/')) == MatchType.MATCH
        assert p.match_directory([]) == MatchType.NO_MATCH
        assert p.match_directory(('test').split('/')) == MatchType.NO_MATCH
        assert p.match_directory(('not/a/hope').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p.match_directory(('a/test/where/test/b').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES
        assert p.match_directory(('some/some/some').split('/')) == MatchType.NO_MATCH_NO_SUBDIRECTORIES

    def test_match_multiple_unbound_directories(self):
        p_dir, p_file = create_starstar('a/**/b/**/c/**/d/')
        assert p_dir.match_directory(('test/a/test/test/b/c/test/test/d/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('test/a/test/a/test/b/c/test/c/test/d/test').split('/')) == MatchType.MATCH_ALL_SUBDIRECTORIES
        assert p_dir.match_directory(('test/a/test/b/test/test/d/test/c/test').split('/')) == MatchType.NO_MATCH

    def test_file_pattern(self):
        p = Pattern.create('*.py')
        match(p, [], [])
        match(p, ['a.no', 'py'], [])
        match(p, ['x.px', 'a.py', 'a.pz', 'b.py', 'py'], ['a.py', 'b.py'])
        p = Pattern.create('?bc.txt')
        match(p, ['a.no', 'py'], [])
        match(p, ['abc.txt', 'bbc.txt', 'not.txt'], ['abc.txt', 'bbc.txt'])

    def test_no_file_pattern(self):
        p = Pattern.create('')
        assert p.file_pattern == '*'
        match(p, [], [])
        s = ['a.py', 'b.py']
        match(p, s, s)
        s = ['x.px', 'a.py', 'a.pz', 'b.py', 'py']
        match(p, s, s)
        p = Pattern.create('*')
        assert p.file_pattern == '*'
        match(p, [], [])
        s = ['a.py', 'b.py']
        match(p, s, s)
        s = ['x.px', 'a.py', 'a.pz', 'b.py', 'py']
        match(p, s, s)


class TestPatternSet(object):

    def test_basic(self):
        py = Pattern.create('*.py')
        cvs = Pattern.create('**/CVS/**/*')
        pycache = Pattern.create('__pycache__/**/*')
        ps = PatternSet()
        assert ps.all_files() is False
        assert [ pat for pat in ps.iter() ] == []
        s = ['a.py', 'b.py']
        match(ps, s, [])
        ps.append(py)
        assert ps.all_files() is False
        assert [ pat for pat in ps.iter() ] == [py]
        s = ['a.py', 'b.py']
        match(ps, s, s)
        s = ['a.py', 'b.py', 'anything.goes']
        match(ps, s, ['a.py', 'b.py'])
        ps.append(cvs)
        assert ps.all_files() is True
        assert [ pat for pat in ps.iter() ] == [py, cvs]
        match(ps, s, s)
        ps.remove(cvs)
        ps.append(pycache)
        assert ps.all_files() is True
        assert [ pat for pat in ps.iter() ] == [py, pycache]
        match(ps, s, s)
        ps.remove(pycache)
        assert ps.all_files() is False
        assert [ pat for pat in ps.iter() ] == [py]
        match(ps, s, ['a.py', 'b.py'])

    def test_extend(self):
        py = Pattern.create('*.py')
        cvs = Pattern.create('**/CVS/*')
        pycache = Pattern.create('__pycache__/**/*')
        ps1 = PatternSet()
        ps1.extend([py, cvs, pycache])
        assert [ pat for pat in ps1.iter() ] == [py, cvs, pycache]
        ps2 = PatternSet()
        ps2.extend(ps1)
        assert [ pat for pat in ps2.iter() ] == [py, cvs, pycache]
        ps1 = PatternSet()
        ps1.extend([py])
        assert [ pat for pat in ps1.iter() ] == [py]
        ps1.extend([cvs, pycache])
        assert [ pat for pat in ps1.iter() ] == [py, cvs, pycache]


class TestFileSetState(object):

    def test_parent(self):
        root = FileSetState('Label', '')
        a = FileSetState('Label', 'a', root)
        assert a.parent == root
        b = FileSetState('Label', os.path.join('a', 'b'), a)
        assert b.parent == a
        c = FileSetState('Label', os.path.join('a', 'b', 'c'), b)
        assert c.parent == b
        d = FileSetState('Label', 'd', c)
        assert d.parent == root

    def test_patterns_root(self):
        bound_start_top_all = Pattern.create('/test/*')
        bound_start_top_py = Pattern.create('/test/*.py')
        bound_start_sub_all = Pattern.create('/test/**/*')
        bound_start_sub_py = Pattern.create('/test/**/*.py')
        bound_end_all = Pattern.create('**/test/*')
        bound_end_py = Pattern.create('**/test/*.py')
        bound_start_end = Pattern.create('/test/**/test/*.py')
        unbound_all = Pattern.create('**/*')
        unbound_py = Pattern.create('**/*.py')
        all = [
         bound_start_top_all, bound_start_top_py,
         bound_start_sub_all, bound_start_sub_py,
         bound_end_all, bound_end_py,
         bound_start_end,
         unbound_all, unbound_py]
        fst = FileSetState('Label', '', None, all)
        file_set_state_location(fst, bound_start_top_all, UNMATCHED)
        file_set_state_location(fst, bound_start_top_py, UNMATCHED)
        file_set_state_location(fst, bound_start_sub_all, UNMATCHED)
        file_set_state_location(fst, bound_start_sub_py, UNMATCHED)
        file_set_state_location(fst, bound_end_all, UNMATCHED)
        file_set_state_location(fst, bound_end_py, UNMATCHED)
        file_set_state_location(fst, bound_start_end, UNMATCHED)
        file_set_state_location(fst, unbound_all, MATCHED_INHERIT)
        file_set_state_location(fst, unbound_py, MATCHED_INHERIT)
        assert fst.no_possible_matches_in_subdirs() is False
        assert fst.matches_all_files_all_subdirs() is True
        return

    def test_patterns_test_matching_dir(self):
        bound_start_top_all = Pattern.create('/test/*')
        bound_start_top_py = Pattern.create('/test/*.py')
        bound_start_sub_all = Pattern.create('/test/**/*')
        bound_start_sub_py = Pattern.create('/test/**/*.py')
        bound_end_all = Pattern.create('**/test/*')
        bound_end_py = Pattern.create('**/test/*.py')
        bound_start_end = Pattern.create('/test/**/test/*.py')
        unbound_all = Pattern.create('**/*')
        unbound_py = Pattern.create('**/*.py')
        all = [
         bound_start_top_all, bound_start_top_py,
         bound_start_sub_all, bound_start_sub_py,
         bound_end_all, bound_end_py,
         bound_start_end,
         unbound_all, unbound_py]
        fst = FileSetState('Label', 'test', None, all)
        file_set_state_location(fst, bound_start_top_all, MATCHED_NO_SUBDIR)
        file_set_state_location(fst, bound_start_top_py, MATCHED_NO_SUBDIR)
        file_set_state_location(fst, bound_start_sub_all, MATCHED_INHERIT)
        file_set_state_location(fst, bound_start_sub_py, MATCHED_INHERIT)
        file_set_state_location(fst, bound_end_all, MATCHED_AND_SUBDIR)
        file_set_state_location(fst, bound_end_py, MATCHED_AND_SUBDIR)
        file_set_state_location(fst, bound_start_end, UNMATCHED)
        file_set_state_location(fst, unbound_all, MATCHED_INHERIT)
        file_set_state_location(fst, unbound_py, MATCHED_INHERIT)
        assert fst.no_possible_matches_in_subdirs() is False
        assert fst.matches_all_files_all_subdirs() is True
        return

    def test_patterns_test_no_match(self):
        bound_start_top_all = Pattern.create('/test/*')
        bound_start_top_py = Pattern.create('/test/*.py')
        bound_start_sub_all = Pattern.create('/test/**/*')
        bound_start_sub_py = Pattern.create('/test/**/*.py')
        bound_end_all = Pattern.create('**/test/*')
        bound_end_py = Pattern.create('**/test/*.py')
        bound_start_end = Pattern.create('/test/**/test/*.py')
        unbound_all = Pattern.create('**/*')
        unbound_py = Pattern.create('**/*.py')
        all = [
         bound_start_top_all, bound_start_top_py,
         bound_start_sub_all, bound_start_sub_py,
         bound_end_all, bound_end_py,
         bound_start_end,
         unbound_all, unbound_py]
        fst = FileSetState('Label', 'nottest', None, all)
        file_set_state_location(fst, bound_start_top_all, NOT_PRESENT)
        file_set_state_location(fst, bound_start_top_py, NOT_PRESENT)
        file_set_state_location(fst, bound_start_sub_all, NOT_PRESENT)
        file_set_state_location(fst, bound_start_sub_py, NOT_PRESENT)
        file_set_state_location(fst, bound_end_all, UNMATCHED)
        file_set_state_location(fst, bound_end_py, UNMATCHED)
        file_set_state_location(fst, bound_start_end, NOT_PRESENT)
        file_set_state_location(fst, unbound_all, MATCHED_INHERIT)
        file_set_state_location(fst, unbound_py, MATCHED_INHERIT)
        assert fst.no_possible_matches_in_subdirs() is False
        assert fst.matches_all_files_all_subdirs() is True
        return

    def test_patterns_test_no_possible_match(self):
        bound_start_top_all = Pattern.create('/test/*')
        bound_start_top_py = Pattern.create('/test/*.py')
        bound_start_sub_all = Pattern.create('/test/**/*')
        bound_start_sub_py = Pattern.create('/test/**/*.py')
        bound_start_end = Pattern.create('/test/**/test/*.py')
        all = [
         bound_start_top_all, bound_start_top_py,
         bound_start_sub_all, bound_start_sub_py,
         bound_start_end]
        fst = FileSetState('Label', 'nottest', None, all)
        file_set_state_location(fst, bound_start_top_all, NOT_PRESENT)
        file_set_state_location(fst, bound_start_top_py, NOT_PRESENT)
        file_set_state_location(fst, bound_start_sub_all, NOT_PRESENT)
        file_set_state_location(fst, bound_start_sub_py, NOT_PRESENT)
        file_set_state_location(fst, bound_start_end, NOT_PRESENT)
        assert fst.no_possible_matches_in_subdirs() is True
        assert fst.matches_all_files_all_subdirs() is False
        return

    def test_patterns_inherit_with_file(self):
        pattern1 = Pattern.create('/a/**/*.a')
        pattern2 = Pattern.create('**/b/**/*.b')
        pattern3 = Pattern.create('/a/b/c/*.c')
        all_files = ['not', 'a.a', 'b.b', 'c.c']
        a_files = ['a.a', 'aa.a']
        root = FileSetState('Label', '', None, [pattern1, pattern2, pattern3])
        file_set_state_location(root, pattern1, UNMATCHED)
        file_set_state_location(root, pattern2, UNMATCHED)
        file_set_state_location(root, pattern3, UNMATCHED)
        assert not root.match([])
        assert not root.match(all_files)
        assert not root.match(a_files)
        a = FileSetState('Label', 'a', root)
        file_set_state_location(a, pattern1, MATCHED_INHERIT)
        file_set_state_location(a, pattern2, UNMATCHED)
        file_set_state_location(a, pattern3, UNMATCHED)
        assert not a.match([])
        assert {'a.a'} == a.match(all_files)
        assert {'a.a', 'aa.a'} == a.match(a_files)
        b = FileSetState('Label', os.path.join('a', 'b'), a)
        file_set_state_location(b, pattern1, NOT_PRESENT)
        file_set_state_location(b, pattern2, MATCHED_INHERIT)
        file_set_state_location(b, pattern3, UNMATCHED)
        assert not b.match([])
        assert {'a.a', 'b.b'} == b.match(all_files)
        assert {'a.a', 'aa.a'} == b.match(a_files)
        c = FileSetState('Label', os.path.join('a', 'b', 'c'), b)
        file_set_state_location(c, pattern1, NOT_PRESENT)
        file_set_state_location(c, pattern2, NOT_PRESENT)
        file_set_state_location(c, pattern3, MATCHED_NO_SUBDIR)
        assert not c.match([])
        assert {'a.a', 'b.b', 'c.c'} == c.match(all_files)
        assert {'a.a', 'aa.a'} == c.match(a_files)
        d = FileSetState('Label', os.path.join('a', 'b', 'c', 'd'), b)
        file_set_state_location(d, pattern1, NOT_PRESENT)
        file_set_state_location(d, pattern2, NOT_PRESENT)
        file_set_state_location(d, pattern3, NOT_PRESENT)
        assert not d.match([])
        assert {'a.a', 'b.b'} == d.match(all_files)
        assert {'a.a', 'aa.a'} == b.match(a_files)
        return

    def test_patterns_inherit_all_files(self):
        pattern1 = Pattern.create('/a/**/*')
        all_files = ['not', 'a.a', 'b.b', 'c.c']
        root = FileSetState('Label', '', None, [pattern1])
        file_set_state_location(root, pattern1, UNMATCHED)
        assert not root.match([])
        assert not root.match(all_files)
        a = FileSetState('Label', 'a', root)
        file_set_state_location(a, pattern1, MATCHED_INHERIT)
        assert not a.match([])
        assert set(all_files) == a.match(all_files)
        b = FileSetState('Label', os.path.join('a', 'b'), a)
        file_set_state_location(b, pattern1, NOT_PRESENT)
        file_set_state_location(a, pattern1, MATCHED_INHERIT)
        assert not b.match([])
        assert b.parent == a
        assert set(all_files) == b.match(all_files)
        return


class TestFileSet(object):

    def test_basic(self):
        root = os.path.dirname(os.path.dirname(__file__))
        pattern_all = os.path.sep + os.path.join('**', '*')
        pattern_py = os.path.sep + os.path.join('**', '*.py')
        pattern_pyc = os.path.sep + os.path.join('**', '*.pyc')
        pattern_txt = os.path.sep + os.path.join('**', '*.txt')
        print 'Formic directory=', root, 'include=', pattern_all
        definitive_count = find_count(root, '*.py')
        fs = FileSet(directory=root, include=pattern_py, symlinks=False)
        files = [ os.path.join(root, dir, file) for dir, file in fs.files() ]
        assert definitive_count == len(files)
        assert [] == [ file for file in files if not os.path.isfile(file) ]
        assert files == [ file for file in files if file.endswith('.py') ]
        fs = FileSet(directory=root, include=pattern_all, exclude=[pattern_pyc, pattern_txt])
        files = [ os.path.join(root, dir, file) for dir, file in fs.files() ]
        assert definitive_count <= len(files)
        assert [] == [ file for file in files if not os.path.isfile(file) ]
        assert [] == [ file for file in files if file.endswith('.pyc') ]
        assert [] == [ file for file in files if file.endswith('.txt') ]

    def test_bound_root(self):
        """Unit test to pick up Issue #1"""
        original_dir = os.getcwd()
        curdir = os.path.dirname(os.path.dirname(__file__))
        os.chdir(curdir)
        try:
            import glob
            actual = glob.glob('*.py')
            fs = FileSet(include='/*.py', default_excludes=False)
            count = 0
            for file in fs:
                count += 1
                print 'File:', file
                head, tail = os.path.split(file)
                assert curdir == head
                assert tail in actual
                assert tail.endswith('.py')

            assert len(actual) == count
        finally:
            os.chdir(original_dir)

    def test_cwd(self):
        fs = FileSet(include='*')
        assert fs.directory is None
        assert os.getcwd() == fs.get_directory()
        directory = os.path.dirname(__file__) + os.path.sep + os.path.sep + os.path.sep
        fs = FileSet(directory=directory, include='*')
        assert fs.directory == os.path.dirname(__file__)
        assert fs.get_directory() == os.path.dirname(__file__)
        return

    def test_vs_find(self):
        compare_find_and_formic(get_test_directory())
        compare_find_and_formic(get_test_directory(), 'a*')

    def test_iterator(self):
        fs = FileSet(include='*.py')
        i = fs.__iter__()
        assert {f for f in fs.qualified_files()} == {f for f in i}

    def test_alternate_walk(self):
        files = [
         'CVS/error.py', 'silly/silly1.txt', '1/2/3.py', 'silly/silly3.txt', '1/2/4.py', 'silly/silly3.txt']
        fileset = FileSet(include='*.py', walk=walk_from_list(files))
        found = [ (dir, file) for dir, file in fileset.files() ]
        assert len(found) == 2
        assert ('CVS', 'error.py') not in found
        assert (os.path.join('1', '2'), '3.py') in found
        assert (os.path.join('1', '2'), '4.py') in found

    def test_glob_starstar(self):
        files = [
         'in/test/1.py', 'in/a/b/test/2.py', 'in/a/b/test', 'out/a/3.py', 'out/a/test.py']
        fileset = FileSet(include='in/**/test/', walk=walk_from_list(files))
        found = [ (dir, file) for dir, file in fileset.files() ]
        assert len(found) == 3
        assert (os.path.join('in', 'a', 'b'), 'test') in found
        assert (os.path.join('out', 'a'), 'test.py') not in found
        files = [
         'in/test/1test1.py', 'in/a/b/test/2test2.py', 'in/a/b/4test4', 'out/a/3.py', 'out/a/test.py']
        fileset = FileSet(include='in/**/*test*/', walk=walk_from_list(files))
        found = [ (dir, file) for dir, file in fileset.files() ]
        assert len(found) == 3
        assert (os.path.join('in', 'a', 'b'), '4test4') in found
        assert (os.path.join('out', 'a'), 'test.py') not in found


class TestMiscellaneous(object):

    def test_version(self):
        assert '0.9beta8' == get_version()

    def test_rooted(self):
        curdir = os.getcwd()
        full = os.path.dirname(os.path.dirname(__file__))
        drive, dir = os.path.splitdrive(full)
        wild = '**' + os.path.sep + '*.rst'
        os.chdir(full)
        try:
            fileset = FileSet(include=wild, directory=full)
            for filename in fileset.qualified_files():
                print filename

            absolute = [ filename for filename in FileSet(include=wild, directory=full) ]
            relative = [ filename for filename in FileSet(include=wild) ]
            rooted = [ filename for filename in FileSet(include=os.path.join(dir, wild), directory=drive + os.path.sep) ]
            assert len(relative) == len(absolute) == len(rooted)
            combined = zip(rooted, relative, absolute)
            for root, rel, abso in combined:
                print root, '<->', rel, '<->', abso
                assert root.endswith(rel)
                assert abso.endswith(rel)

        finally:
            os.chdir(curdir)

    def test_search_prune_efficiency(self):
        curdir = os.getcwd()
        formic_root = os.path.dirname(os.path.dirname(__file__))
        print 'Absolute, starting at ', formic_root
        rooted = FileSet(include='/test/lower/lower.txt', directory=formic_root, default_excludes=False)
        files = [ f for f in rooted ]
        assert len(files) == 1
        floating = FileSet(include='/*/lower/lower.txt', directory=formic_root, default_excludes=False)
        files = [ f for f in floating ]
        assert len(files) == 1
        assert rooted._received < floating._received

    def test_filename_case(self):
        root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test')
        for test in ['/lower/lower.txt', 'lower/UPPER.txt', 'UPPER/lower.txt', 'UPPER/UPPER.txt']:
            print 'Testing', test
            found = [ f for f in FileSet(include=test, directory=root) ]
            assert len(found) == 1
            print '   ... found', test

        if os.name == 'posix':
            for test in ['Formic.py', 'VERSION.Txt']:
                print 'Testing for non-match of', test
                found = [ f for f in FileSet(include=test, directory=root) ]
                assert len(found) == 0

    def test_get_path_components(self):
        drive, components = get_path_components(os.path.join('a', 'b', 'c'))
        assert drive == ''
        assert components == ['a', 'b', 'c']
        drive, components = get_path_components(os.path.sep)
        assert drive == ''
        assert components == []
        drive, components = get_path_components(os.path.sep + os.path.sep + 'a' + os.path.sep + 'b')
        assert drive == ''
        assert components == ['a', 'b']