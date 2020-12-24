# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcmp/tests.py
# Compiled at: 2013-09-24 13:19:07
"""
tests for rcmp.
"""
from __future__ import unicode_literals, print_function
__docformat__ = b'restructuredtext en'
import abc, os, shutil, subprocess, tempfile, time, nose
from nose.tools import assert_false, assert_equal, raises
import rcmp
verbose_logging = False
if verbose_logging:
    import logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def assert_isfile(filename):
    assert os.path.isfile(filename), (b'missing {}').format(filename)


rcmp_py = os.path.join(b'rcmp', b'__init__.py')
tests_py = os.path.join(b'rcmp', b'tests.py')

def rmtree(dir):
    for i in range(5):
        try:
            shutil.rmtree(dir)
        except:
            print((b'tic {} {}').format(i, dir))
            print(os.listdir(dir))
            if i < 4:
                time.sleep(1)
                continue
            else:
                print((b'clunk! {}\n').format(dir))
                raise
        else:
            break


class testBasics(object):
    nosuch = b'nosuchfileordirectory'
    exit_asap = True

    def __init__(self):
        self.testfilenames = [
         rcmp_py, tests_py]
        self.itestfiles = [ rcmp.Items.find_or_create(f, rcmp.root) for f in self.testfilenames ]

    def setUp(self):
        rcmp.Items.reset()

    def tearDown(self):
        rcmp.Items.reset()

    @raises(rcmp.IndeterminateResult)
    def testEmpty(self):
        rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[0], comparators=[], exit_asap=self.exit_asap).cmp()

    @raises(rcmp.IndeterminateResult)
    def testMissing(self):
        rcmp.Comparison(lname=self.testfilenames[0], rname=self.nosuch, comparators=[], exit_asap=self.exit_asap).cmp()

    @raises(rcmp.IndeterminateResult)
    def testEmptyList(self):
        rcmp.ComparisonList([[self.testfilenames[0]], [self.testfilenames[0]]], comparators=[], exit_asap=self.exit_asap).cmp()

    def testNoSuchRight(self):
        assert_equal(rcmp.Comparison(lname=self.testfilenames[0], rname=self.nosuch, comparators=[
         rcmp.NoSuchFileComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)

    def testNoSuchLeft(self):
        assert_equal(rcmp.Comparison(lname=self.nosuch, rname=self.testfilenames[0], comparators=[
         rcmp.NoSuchFileComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)

    def testNoSuchBoth(self):
        assert_equal(rcmp.Comparison(lname=self.nosuch, rname=self.nosuch, comparators=[
         rcmp.NoSuchFileComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    @raises(rcmp.IndeterminateResult)
    def testNoSuchNeither(self):
        assert_false(rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[0], comparators=[
         rcmp.NoSuchFileComparator], exit_asap=self.exit_asap).cmp())

    def testInode(self):
        assert_equal(rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[0], comparators=[
         rcmp.InodeComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testInodeList(self):
        assert_equal(rcmp.ComparisonList([[self.testfilenames[0]], [self.testfilenames[0]]], comparators=[
         rcmp.InodeComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    @raises(rcmp.IndeterminateResult)
    def testInodeIndeterminate(self):
        assert_equal(rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[1], comparators=[
         rcmp.InodeComparator], exit_asap=self.exit_asap).cmp(), False)

    @raises(rcmp.IndeterminateResult)
    def testInodeIndeterminateList(self):
        assert_equal(rcmp.ComparisonList([[self.testfilenames[0]], [self.testfilenames[1]]], comparators=[
         rcmp.InodeComparator], exit_asap=self.exit_asap).cmp(), False)

    def testBitwise(self):
        assert_equal(rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[0], comparators=[
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testBitwiseList(self):
        assert_equal(rcmp.ComparisonList([[self.testfilenames[0]], [self.testfilenames[0]]], comparators=[
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    @raises(rcmp.IndeterminateResult)
    def testBitwiseIndeterminate(self):
        assert_equal(rcmp.Comparison(lname=self.testfilenames[0], rname=self.testfilenames[1], comparators=[
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), False)

    @raises(rcmp.IndeterminateResult)
    def testBitwiseIndeterminateList(self):
        assert_equal(rcmp.ComparisonList([[self.testfilenames[0]], [self.testfilenames[1]]], comparators=[
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), False)

    def testElf(self):
        lname = os.path.join(b'testfiles', b'left', b'main.o')
        rname = os.path.join(b'testfiles', b'right', b'main.o')
        assert_isfile(lname)
        assert_isfile(rname)
        assert_equal(rcmp.Comparison(lname=lname, rname=rname, comparators=[
         rcmp.ElfComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)


class testBasicsSlow(testBasics):
    exit_asap = False


class testDirDirect(object):
    emptydirname = b'emptydir'
    dirnotemptybase = b'notempty'
    foilername = b'foiler'
    exit_asap = True

    def setUp(self):
        rcmp.Items.reset()
        os.makedirs(self.emptydirname)
        os.makedirs(os.path.join(self.dirnotemptybase, self.foilername))

    def tearDown(self):
        rcmp.Items.reset()
        rmtree(self.emptydirname)
        rmtree(self.dirnotemptybase)

    def testDirDirect(self):
        itestdir = rcmp.Items.find_or_create(self.emptydirname, rcmp.root)
        itestdir2 = rcmp.Items.find_or_create(self.dirnotemptybase, rcmp.root)
        assert_equal(rcmp.Comparison(litem=itestdir, ritem=itestdir, comparators=[
         rcmp.DirComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)
        assert_equal(rcmp.ComparisonList([[self.emptydirname], [self.emptydirname]], comparators=[
         rcmp.DirComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)
        assert_equal(rcmp.Comparison(litem=itestdir, ritem=itestdir2, comparators=[
         rcmp.DirComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)
        assert_equal(rcmp.ComparisonList([[self.emptydirname], [self.dirnotemptybase]], comparators=[
         rcmp.DirComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)
        assert_equal(rcmp.ComparisonList([[self.emptydirname], [self.dirnotemptybase]], comparators=[
         rcmp.DirComparator], ignores=rcmp.fntore([b'*' + self.foilername]), exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testReal(self):
        itestdir = rcmp.Items.find_or_create(self.emptydirname, rcmp.root)
        r = rcmp.Comparison(litem=itestdir, ritem=itestdir, exit_asap=self.exit_asap)
        assert_equal(r.cmp(), rcmp.Same)


class testDirDirectSlow(testDirDirect):
    exit_asap = False


class TreeBase(object):
    exit_asap = True

    def setUp(self):
        rcmp.Items.reset()
        self.tdir = tempfile.mkdtemp()
        self.dirs = [ os.path.join(self.tdir, dir) for dir in [b'red', b'blue'] ]
        dirs2 = [ os.path.join(p, q) for p in self.dirs for q in [b'ham', b'eggs', b'spam', b'sam',
         b'I', b'am', b'do', b'not',
         b'like']
                ]
        for dir in self.dirs + dirs2:
            os.makedirs(dir)
            for filename in [b'foo', b'bar', b'baz', b'bim',
             b'george', b'fred', b'carol', b'ted',
             b'alice']:
                with open(os.path.join(dir, filename), b'wb') as (f):
                    print(filename, file=f)

    def tearDown(self):
        rcmp.Items.reset()
        rmtree(self.tdir)


class testTree(TreeBase):

    def testCase1(self):
        assert_equal(rcmp.Comparison(lname=self.dirs[0], rname=self.dirs[1], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testFallThrough(self):
        r = rcmp.Comparison(lname=os.path.join(self.dirs[0], b'ham', b'foo'), rname=os.path.join(self.dirs[1], b'eggs', b'bar'), exit_asap=self.exit_asap)
        assert_equal(r.cmp(), rcmp.Different)


class testTreeSlow(testTree):
    exit_asap = False


class testTreeAux(TreeBase):

    def setUp(self):
        rcmp.Items.reset()
        TreeBase.setUp(self)
        for dir in self.dirs:
            filename = os.path.abspath(os.path.join(dir, b'ham', b'foo.pyc'))
            with open(filename, b'wb') as (f):
                print(filename, file=f)

    def testBuried(self):
        assert_equal(rcmp.Comparison(lname=os.path.join(self.dirs[0], b'ham', b'foo.pyc'), rname=os.path.join(self.dirs[1], b'ham', b'foo.pyc'), comparators=[
         rcmp.BuriedPathComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testIgnore(self):
        assert_equal(rcmp.Comparison(lname=self.dirs[0], rname=self.dirs[1], ignores=rcmp.fntore([b'*.pyc']), exit_asap=self.exit_asap).cmp(), rcmp.Same)


class testTreeAuxSlow(testTreeAux):
    exit_asap = False


class testSymlinks(TreeBase):

    def setUp(self):
        rcmp.Items.reset()
        TreeBase.setUp(self)
        self.red_sausage = os.path.join(self.dirs[0], b'sausage')
        self.red_bacon = os.path.join(self.dirs[0], b'bacon')
        self.red_bird = os.path.join(self.dirs[0], b'bird')
        self.blue_sausage = os.path.join(self.dirs[1], b'sausage')
        self.blue_bacon = os.path.join(self.dirs[1], b'bacon')
        self.blue_bird = os.path.join(self.dirs[1], b'bird')
        os.symlink(b'foo', self.red_bird)
        os.symlink(b'nonexistent', self.red_sausage)
        os.symlink(b'ham', self.red_bacon)
        os.symlink(b'foo', self.blue_bird)
        os.symlink(b'nonexistent', self.blue_sausage)
        os.symlink(b'ham', self.blue_bacon)

    def testBird(self):
        assert_equal(rcmp.Comparison(lname=self.red_bird, rname=self.blue_bird, exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testBacon(self):
        assert_equal(rcmp.Comparison(lname=self.red_bacon, rname=self.blue_bacon, exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testSausage(self):
        assert_equal(rcmp.Comparison(lname=self.red_sausage, rname=self.blue_sausage, exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testDir(self):
        assert_equal(rcmp.Comparison(lname=self.dirs[0], rname=self.dirs[1], exit_asap=self.exit_asap).cmp(), rcmp.Same)


class testSymlinksSlow(testSymlinks):
    exit_asap = False


class FakeComparator(rcmp.Comparator):
    """
    Raise IndeterminateResult for files named 'ham' and return Different
    for others.
    """

    @staticmethod
    def _applies(thing):
        return True

    @classmethod
    def cmp(self, comparison):
        if comparison.pair[0].name.endswith(b'bar'):
            raise rcmp.IndeterminateResult
        return rcmp.Different


class testSlow(TreeBase):

    def setUp(self):
        rcmp.Items.reset()
        TreeBase.setUp(self)
        with open(os.path.join(self.dirs[0], b'I', b'alice'), b'w') as (fff):
            print(b'ho', file=fff)
            print(b'ho', file=fff)
            print(b'ho', file=fff)

    def testShort(self):
        assert_equal(rcmp.Comparison(lname=self.dirs[0], rname=self.dirs[1], comparators=[
         rcmp.DirComparator,
         FakeComparator], exit_asap=True).cmp(), rcmp.Different)

    @raises(rcmp.IndeterminateResult)
    def testLong(self):
        rcmp.Comparison(lname=self.dirs[0], rname=self.dirs[1], comparators=[
         rcmp.DirComparator,
         FakeComparator], exit_asap=False).cmp()


class testCommonSuffix(object):

    def testSimple(self):
        assert_equal(rcmp._findCommonSuffix(b'a/b/c', b'a/b/c'), ('', '', 'a/b/c'))
        assert_equal(rcmp._findCommonSuffix(b'a/b/c', b'd/e/f'), ('a/b/c', 'd/e/f',
                                                                  ''))
        assert_equal(rcmp._findCommonSuffix(b'b/a', b'c/a'), ('b', 'c', 'a'))
        assert_equal(rcmp._findCommonSuffix(b'a/b/c', b'd/e/c'), ('a/b', 'd/e', 'c'))
        assert_equal(rcmp._findCommonSuffix(b'a/b/c/d', b'e/f/c/d'), ('a/b', 'e/f',
                                                                      'c/d'))
        assert_equal(rcmp._findCommonSuffix(b'a/b/c/d', b'e/f/g/d'), ('a/b/c', 'e/f/g',
                                                                      'd'))
        assert_equal(rcmp._findCommonSuffix(b'a/b/c/d', b'e/b/c/d'), ('a', 'e', 'b/c/d'))


class testAr(object):
    empty = b'empty.a'
    first = b'first.a'
    second = b'second.a'
    third = b'third.a'
    left = os.path.join(b'testfiles', b'left', b'archive.a')
    assert_isfile(left)
    right = os.path.join(b'testfiles', b'right', b'archive.a')
    assert_isfile(right)
    exit_asap = True

    def setUp(self):
        rcmp.Items.reset()
        with open(self.empty, b'wb') as (f):
            f.write(b'!<arch>\n')
        subprocess.check_call([b'ar', b'cr', self.first, rcmp_py])
        subprocess.check_call([b'ar', b'cr', self.second, rcmp_py])
        subprocess.check_call([b'ar', b'cr', self.third, rcmp_py, tests_py])

    def tearDown(self):
        rcmp.Items.reset()
        for i in [self.empty, self.first, self.second, self.third]:
            os.remove(i)

    def testEmpty(self):
        assert_equal(rcmp.Comparison(lname=self.empty, rname=self.empty, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testIdentical(self):
        r = rcmp.Comparison(lname=self.first, rname=self.first, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator,
         rcmp.BitwiseComparator], exit_asap=self.exit_asap)
        assert_equal(r.cmp(), rcmp.Same)

    def testTwo(self):
        assert_equal(rcmp.Comparison(lname=self.first, rname=self.second, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator,
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), rcmp.Same)

    def testDifferent(self):
        assert_equal(rcmp.Comparison(lname=self.first, rname=self.third, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator,
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)

    def testOtherDifferent(self):
        assert_equal(rcmp.Comparison(lname=self.third, rname=self.first, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator,
         rcmp.BitwiseComparator], exit_asap=self.exit_asap).cmp(), rcmp.Different)

    def testArElf(self):
        r = rcmp.Comparison(lname=self.left, rname=self.right, comparators=[
         rcmp.ArMemberMetadataComparator,
         rcmp.ArComparator,
         rcmp.ElfComparator], exit_asap=self.exit_asap)
        assert_equal(r.cmp(), rcmp.Same)


class testArSlow(testAr):
    exit_asap = False


class SimpleAbstract(object):
    __metaclass__ = abc.ABCMeta
    exit_asap = True

    @abc.abstractproperty
    def filenames(self):
        return

    @abc.abstractproperty
    def comparators(self):
        return []

    sides = [
     b'left', b'right']

    def __init__(self, exit_asap=True):
        self.lefts, self.rights = [ [ os.path.join(b'testfiles', side, filename) for filename in self.filenames ] for side in self.sides
                                  ]
        for f in self.lefts + self.rights:
            assert_isfile(f)

        self.exit_asap = exit_asap

    def testIdentical(self):
        for left in self.lefts:
            r = rcmp.Comparison(lname=left, rname=left, comparators=self.comparators, exit_asap=self.exit_asap)
            assert_equal(r.cmp(), rcmp.Same)

    def testOne(self):
        for left, right in zip(self.lefts, self.rights):
            r = rcmp.Comparison(lname=left, rname=right, comparators=self.comparators, exit_asap=self.exit_asap)
            assert_equal(r.cmp(), rcmp.Same)

    def testReal(self):
        for left, right in zip(self.lefts, self.rights):
            r = rcmp.Comparison(lname=left, rname=right, exit_asap=self.exit_asap)
            assert_equal(r.cmp(), rcmp.Same)

    @raises(rcmp.IndeterminateResult)
    def testBad(self):
        for left in self.lefts:
            r = rcmp.Comparison(lname=left, rname=b'/dev/null', comparators=self.comparators, exit_asap=self.exit_asap)
            assert_equal(r.cmp(), rcmp.Different)


class testEmpty(SimpleAbstract):
    filenames = [
     b'empty']
    comparators = [
     rcmp.EmptyFileComparator]


class testEmptySlow(testEmpty):
    exit_asap = False


class testAr2(SimpleAbstract):
    filenames = [
     b'archive.a']
    comparators = [
     rcmp.BitwiseComparator,
     rcmp.ArMemberMetadataComparator,
     rcmp.ArComparator]

    def setUp(self):
        rcmp.Items.reset()
        for side in [b'left', b'right']:
            fname = os.path.join(b'testfiles', side, b'stumper')
            try:
                os.remove(fname)
            except:
                pass

            with open(fname, b'wb'):
                pass
            os.chmod(fname, 0)

    def tearDown(self):
        rcmp.Items.reset()
        for side in [b'left', b'right']:
            try:
                os.remove(os.path.join(b'testfiles', side, b'stumper'))
            except OSError as val:
                if val is 2:
                    pass
                else:
                    raise


class testAr2Slow(testAr2):
    exit_asap = False


class testAM(SimpleAbstract):
    filenames = [
     b'Makefile']
    comparators = [rcmp.AMComparator]


class testConfigLog(SimpleAbstract):
    not_filenames = [
     b'2config.log', b'db-config.log', b'3config.log']
    filenames = [b'config.log', b'config.status']
    comparators = [rcmp.ConfigLogComparator]


class testGzip(SimpleAbstract):
    filenames = [
     b'Makefile.in.gz', b'yo.gz.gz.gz']
    comparators = [rcmp.GzipComparator, rcmp.BitwiseComparator]


class testBZ2(SimpleAbstract):
    filenames = [
     b'Makefile.in.bz2', b'yo.bz2.bz2.bz2']
    comparators = [rcmp.BZ2Comparator, rcmp.BitwiseComparator]


if rcmp.lzma:

    class testXZ(SimpleAbstract):
        filenames = [b'Makefile.in.xz', b'yo.xz.xz.xz']
        comparators = [rcmp.XZComparator, rcmp.BitwiseComparator]


class testZip(SimpleAbstract):
    filenames = [
     b'zipfile.zip']
    comparators = [
     rcmp.ZipMemberMetadataComparator,
     rcmp.ZipComparator,
     rcmp.BitwiseComparator]
    testdir = b'testfiles'
    nullfilename = b'nullfile.zip'
    emptyfilename = b'emptyfile.zip'
    fnames = []

    def __init__(self):
        self.fnames = []
        SimpleAbstract.__init__(self)

    def setUp(self):
        rcmp.Items.reset()
        for fname in [ os.path.join(self.testdir, side, self.nullfilename) for side in [b'left', b'right'] ]:
            self.fnames.append(fname)
            with open(fname, b'wb'):
                pass

        for fname in [ os.path.join(self.testdir, side, self.emptyfilename) for side in [b'left', b'right'] ]:
            self.fnames.append(fname)
            with rcmp.openzip(fname, b'w') as (f):
                pass

    def tearDown(self):
        rcmp.Items.reset()
        for fname in self.fnames:
            os.remove(fname)


class testCpio(SimpleAbstract):
    filenames = [
     b'cpiofile.cpio']
    comparators = [
     rcmp.BitwiseComparator,
     rcmp.SymlinkComparator,
     rcmp.CpioMemberMetadataComparator,
     rcmp.CpioComparator]


class testTar(SimpleAbstract):
    filenames = [
     b'tarfile.tar']
    comparators = [
     rcmp.BitwiseComparator,
     rcmp.SymlinkComparator,
     rcmp.TarMemberMetadataComparator,
     rcmp.TarComparator]


class SimilarAbstract(SimpleAbstract):
    sides = [
     b'red', b'black']


class testMap(SimilarAbstract):
    filenames = [
     b'x.map']
    comparators = [rcmp.MapComparator]


class testScript(object):

    def testHelp(self):
        with open(b'/dev/null', b'w') as (devnull):
            assert_equal(subprocess.call((b'rcmp --help').split(), stdout=devnull, stderr=devnull), 0)

    def testBasic(self):
        assert_equal(subprocess.call((b'rcmp testfiles/left testfiles/left').split()), 0)

    def testFail(self):
        assert_equal(subprocess.call((b'rcmp testfiles/main.c testfiles/configure.ac').split()), 1)

    def testBasicv(self):
        assert_equal(subprocess.call((b'rcmp -v testfiles/left testfiles/right').split()), 0)

    def testIgnores(self):
        ignorefile = b'ignorefile'
        with open(ignorefile, b'w') as (fileobj):
            fileobj.write(b'*main.c\n*configure.ac\n')
        with open(b'/dev/null', b'w') as (devnull):
            assert_equal(subprocess.call((b'rcmp -i {} testfiles/main.c testfiles/configure.ac').format(ignorefile).split(), stdout=devnull, stderr=devnull), 1)
        os.remove(ignorefile)


if __name__ == b'__main__':
    nose.main()