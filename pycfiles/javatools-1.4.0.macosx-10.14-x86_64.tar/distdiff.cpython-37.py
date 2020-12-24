# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/distdiff.py
# Compiled at: 2019-06-21 15:26:13
# Size of source mod 2**32: 20220 bytes
"""
Utility for comparing two distributions.

Distributions are directories. Any JAR files (eg: jar, sar, ear, war)
will be deeply checked for their class members. And Class files will
be checked for deep differences.

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL
"""
import sys
from argparse import ArgumentParser
from multiprocessing import cpu_count
from os.path import join
from six.moves import range, zip_longest
from . import unpack_classfile
from .change import GenericChange, SuperChange, Addition, Removal
from .change import squash, yield_sorted_by_type
from .classdiff import JavaClassChange, JavaClassReport
from .classdiff import add_classdiff_optgroup, add_general_optgroup
from .dirutils import compare, fnmatches
from .dirutils import LEFT, RIGHT, SAME, DIFF
from .manifest import Manifest, ManifestChange
from .jardiff import JarChange, JarReport, add_jardiff_optgroup
from .jarinfo import JAR_PATTERNS
__all__ = ('TEXT_PATTERNS', 'DistChange', 'DistContentChange', 'DistContentAdded',
           'DistContentRemoved', 'DistTextChange', 'DistManifestChange', 'DistClassChange',
           'DistClassAdded', 'DistClassRemoved', 'DistJarChange', 'DistJarAdded',
           'DistJarRemoved', 'DistReport', 'DistClassReport', 'DistJarReport', 'cli',
           'main', 'cli_dist_diff', 'default_distdiff_options')
TEXT_PATTERNS = ('*.bat', '*.cert', '*.cfg', '*.conf', '*.dtd', '*.html', '*.ini',
                 '*.properties', '*.sh', '*.text', '*.txt', '*.xml')

class DistContentChange(SuperChange):
    label = 'Distributed Content'

    def __init__(self, ldir, rdir, entry, change=True):
        super(DistContentChange, self).__init__(ldir, rdir)
        self.entry = entry
        self.changed = change

    def left_fn(self):
        return join(self.ldata, self.entry)

    def right_fn(self):
        return join(self.rdata, self.entry)

    def open_left(self, mode='rb'):
        return open(self.left_fn(), mode)

    def open_right(self, mode='rb'):
        return open(self.right_fn(), mode)

    def collect_impl(self):
        """ Content changes refer to more concrete children, but by
        default are empty """
        return tuple()

    def get_description(self):
        c = 'has changed' if self.is_change() else 'is unchanged'
        return '%s %s: %s' % (self.label, c, self.entry)

    def is_ignored(self, options):
        return fnmatches(self.entry, *options.ignore_filenames) or SuperChange.is_ignored(self, options)


class DistContentAdded(DistContentChange, Addition):
    label = 'Distributed Content Added'

    def get_description(self):
        return '%s: %s' % (self.label, self.entry)


class DistContentRemoved(DistContentChange, Removal):
    label = 'Distributed Content Removed'

    def get_description(self):
        return '%s: %s' % (self.label, self.entry)


class DistTextChange(DistContentChange):
    label = 'Distributed Text'

    def __init__(self, l, r, entry, change=True):
        super(DistTextChange, self).__init__(l, r, entry, change)
        self.lineending = False

    def check(self):
        with self.open_left(mode='rt') as (lfd):
            with self.open_right(mode='rt') as (rfd):
                for li, ri in zip_longest(lfd, rfd, fillvalue=''):
                    if li.rstrip() != ri.rstrip():
                        self.lineending = False
                        break
                else:
                    self.lineending = True

        return super(DistTextChange, self).check()

    def is_ignored(self, options):
        return DistContentChange.is_ignored(self, options) or self.lineending and options.ignore_trailing_whitespace

    def collect_impl(self):
        with self.open_left(mode='rt') as (lfd):
            with self.open_right(mode='rt') as (rfd):
                left = lfd.read()
                right = rfd.read()
                if left != right:
                    yield GenericChange(left, right)


class DistManifestChange(DistContentChange):
    __doc__ = '\n    A MANIFEST.MF file found in the directory structure of the\n    distribution\n    '
    label = 'Distributed Manifest'

    def collect_impl(self):
        if self.is_change():
            left_m = Manifest()
            left_m.parse_file(self.left_fn())
            right_m = Manifest()
            right_m.parse_file(self.right_fn())
            yield ManifestChange(left_m, right_m)


class DistJarChange(DistContentChange):
    label = 'Distributed JAR'

    def collect_impl(self):
        if self.is_change():
            yield JarChange(self.left_fn(), self.right_fn())


class DistJarReport(DistJarChange):
    report_name = 'JarReport'

    def __init__(self, ldata, rdata, entry, reporter):
        super(DistJarReport, self).__init__(ldata, rdata, entry, True)
        self.reporter = reporter

    def collect_impl(self):
        if self.is_change():
            yield JarReport(self.left_fn(), self.right_fn(), self.reporter)


class DistJarAdded(DistContentAdded):
    label = 'Distributed JAR Added'


class DistJarRemoved(DistContentRemoved):
    label = 'Distributed JAR Removed'


class DistClassChange(DistContentChange):
    label = 'Distributed Java Class'

    def collect_impl(self):
        if self.is_change():
            linfo = unpack_classfile(self.left_fn())
            rinfo = unpack_classfile(self.right_fn())
            yield JavaClassChange(linfo, rinfo)


class DistClassReport(DistClassChange):
    report_name = 'JavaClassReport'

    def __init__(self, l, r, entry, reporter):
        super(DistClassReport, self).__init__(l, r, entry, True)
        self.reporter = reporter

    def collect_impl(self):
        if self.is_change():
            linfo = unpack_classfile(self.left_fn())
            rinfo = unpack_classfile(self.right_fn())
            yield JavaClassReport(linfo, rinfo, self.reporter)


class DistClassAdded(DistContentAdded):
    label = 'Distributed Java Class Added'


class DistClassRemoved(DistContentRemoved):
    label = 'Distributed Java Class Removed'


class DistChange(SuperChange):
    __doc__ = '\n    Top-level change for comparing two distributions\n    '
    label = 'Distribution'

    def __init__(self, left, right, shallow=False):
        super(DistChange, self).__init__(left, right)
        self.shallow = shallow

    def get_description(self):
        changed = 'changed' if self.is_change() else 'unchanged'
        return '%s %s from %s to %s' % (
         self.label, changed, self.ldata, self.rdata)

    @yield_sorted_by_type(DistClassAdded, DistClassRemoved, DistClassChange, DistJarAdded, DistJarRemoved, DistJarChange, DistTextChange, DistManifestChange, DistContentAdded, DistContentRemoved, DistContentChange)
    def collect_impl--- This code section failed: ---

 L. 312         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ldata
                4  STORE_FAST               'ld'

 L. 313         6  LOAD_FAST                'self'
                8  LOAD_ATTR                rdata
               10  STORE_FAST               'rd'

 L. 314        12  LOAD_FAST                'self'
               14  LOAD_ATTR                shallow
               16  UNARY_NOT        
               18  STORE_FAST               'deep'

 L. 316     20_22  SETUP_LOOP          646  'to 646'
               24  LOAD_GLOBAL              compare
               26  LOAD_FAST                'ld'
               28  LOAD_FAST                'rd'
               30  CALL_FUNCTION_2       2  '2 positional arguments'
               32  GET_ITER         
             34_0  COME_FROM           624  '624'
            34_36  FOR_ITER            644  'to 644'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'event'
               42  STORE_FAST               'entry'

 L. 317        44  LOAD_FAST                'deep'
               46  POP_JUMP_IF_FALSE   162  'to 162'
               48  LOAD_GLOBAL              fnmatches
               50  LOAD_FAST                'entry'
               52  BUILD_TUPLE_1         1 
               54  LOAD_GLOBAL              JAR_PATTERNS
               56  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               58  CALL_FUNCTION_EX      0  'positional arguments only'
               60  POP_JUMP_IF_FALSE   162  'to 162'

 L. 318        62  LOAD_FAST                'event'
               64  LOAD_GLOBAL              LEFT
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L. 319        70  LOAD_GLOBAL              DistJarRemoved
               72  LOAD_FAST                'ld'
               74  LOAD_FAST                'rd'
               76  LOAD_FAST                'entry'
               78  CALL_FUNCTION_3       3  '3 positional arguments'
               80  YIELD_VALUE      
               82  POP_TOP          
               84  JUMP_FORWARD        160  'to 160'
             86_0  COME_FROM            68  '68'

 L. 320        86  LOAD_FAST                'event'
               88  LOAD_GLOBAL              RIGHT
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   110  'to 110'

 L. 321        94  LOAD_GLOBAL              DistJarAdded
               96  LOAD_FAST                'ld'
               98  LOAD_FAST                'rd'
              100  LOAD_FAST                'entry'
              102  CALL_FUNCTION_3       3  '3 positional arguments'
              104  YIELD_VALUE      
              106  POP_TOP          
              108  JUMP_FORWARD        160  'to 160'
            110_0  COME_FROM            92  '92'

 L. 322       110  LOAD_FAST                'event'
              112  LOAD_GLOBAL              DIFF
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L. 323       118  LOAD_GLOBAL              DistJarChange
              120  LOAD_FAST                'ld'
              122  LOAD_FAST                'rd'
              124  LOAD_FAST                'entry'
              126  LOAD_CONST               True
              128  CALL_FUNCTION_4       4  '4 positional arguments'
              130  YIELD_VALUE      
              132  POP_TOP          
              134  JUMP_FORWARD        160  'to 160'
            136_0  COME_FROM           116  '116'

 L. 324       136  LOAD_FAST                'event'
              138  LOAD_GLOBAL              SAME
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   160  'to 160'

 L. 325       144  LOAD_GLOBAL              DistJarChange
              146  LOAD_FAST                'ld'
              148  LOAD_FAST                'rd'
              150  LOAD_FAST                'entry'
              152  LOAD_CONST               False
              154  CALL_FUNCTION_4       4  '4 positional arguments'
              156  YIELD_VALUE      
              158  POP_TOP          
            160_0  COME_FROM           142  '142'
            160_1  COME_FROM           134  '134'
            160_2  COME_FROM           108  '108'
            160_3  COME_FROM            84  '84'
              160  JUMP_BACK            34  'to 34'
            162_0  COME_FROM            60  '60'
            162_1  COME_FROM            46  '46'

 L. 327       162  LOAD_FAST                'deep'
          164_166  POP_JUMP_IF_FALSE   284  'to 284'
              168  LOAD_GLOBAL              fnmatches
              170  LOAD_FAST                'entry'
              172  LOAD_STR                 '*.class'
              174  CALL_FUNCTION_2       2  '2 positional arguments'
          176_178  POP_JUMP_IF_FALSE   284  'to 284'

 L. 328       180  LOAD_FAST                'event'
              182  LOAD_GLOBAL              LEFT
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 329       188  LOAD_GLOBAL              DistClassRemoved
              190  LOAD_FAST                'ld'
              192  LOAD_FAST                'rd'
              194  LOAD_FAST                'entry'
              196  CALL_FUNCTION_3       3  '3 positional arguments'
              198  YIELD_VALUE      
              200  POP_TOP          
              202  JUMP_FORWARD        282  'to 282'
            204_0  COME_FROM           186  '186'

 L. 330       204  LOAD_FAST                'event'
              206  LOAD_GLOBAL              RIGHT
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   228  'to 228'

 L. 331       212  LOAD_GLOBAL              DistClassAdded
              214  LOAD_FAST                'ld'
              216  LOAD_FAST                'rd'
              218  LOAD_FAST                'entry'
              220  CALL_FUNCTION_3       3  '3 positional arguments'
              222  YIELD_VALUE      
              224  POP_TOP          
              226  JUMP_FORWARD        282  'to 282'
            228_0  COME_FROM           210  '210'

 L. 332       228  LOAD_FAST                'event'
              230  LOAD_GLOBAL              DIFF
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   256  'to 256'

 L. 333       238  LOAD_GLOBAL              DistClassChange
              240  LOAD_FAST                'ld'
              242  LOAD_FAST                'rd'
              244  LOAD_FAST                'entry'
              246  LOAD_CONST               True
              248  CALL_FUNCTION_4       4  '4 positional arguments'
              250  YIELD_VALUE      
              252  POP_TOP          
              254  JUMP_FORWARD        282  'to 282'
            256_0  COME_FROM           234  '234'

 L. 334       256  LOAD_FAST                'event'
              258  LOAD_GLOBAL              SAME
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   642  'to 642'

 L. 335       266  LOAD_GLOBAL              DistClassChange
              268  LOAD_FAST                'ld'
              270  LOAD_FAST                'rd'
              272  LOAD_FAST                'entry'
              274  LOAD_CONST               False
              276  CALL_FUNCTION_4       4  '4 positional arguments'
              278  YIELD_VALUE      
              280  POP_TOP          
            282_0  COME_FROM           254  '254'
            282_1  COME_FROM           226  '226'
            282_2  COME_FROM           202  '202'
              282  JUMP_BACK            34  'to 34'
            284_0  COME_FROM           176  '176'
            284_1  COME_FROM           164  '164'

 L. 337       284  LOAD_FAST                'deep'
          286_288  POP_JUMP_IF_FALSE   412  'to 412'
              290  LOAD_GLOBAL              fnmatches
              292  LOAD_FAST                'entry'
              294  BUILD_TUPLE_1         1 
              296  LOAD_GLOBAL              TEXT_PATTERNS
              298  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              300  CALL_FUNCTION_EX      0  'positional arguments only'
          302_304  POP_JUMP_IF_FALSE   412  'to 412'

 L. 338       306  LOAD_FAST                'event'
              308  LOAD_GLOBAL              LEFT
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   332  'to 332'

 L. 339       316  LOAD_GLOBAL              DistContentRemoved
              318  LOAD_FAST                'ld'
              320  LOAD_FAST                'rd'
              322  LOAD_FAST                'entry'
              324  CALL_FUNCTION_3       3  '3 positional arguments'
              326  YIELD_VALUE      
              328  POP_TOP          
              330  JUMP_FORWARD        410  'to 410'
            332_0  COME_FROM           312  '312'

 L. 340       332  LOAD_FAST                'event'
              334  LOAD_GLOBAL              RIGHT
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   358  'to 358'

 L. 341       342  LOAD_GLOBAL              DistContentAdded
              344  LOAD_FAST                'ld'
              346  LOAD_FAST                'rd'
              348  LOAD_FAST                'entry'
              350  CALL_FUNCTION_3       3  '3 positional arguments'
              352  YIELD_VALUE      
              354  POP_TOP          
              356  JUMP_FORWARD        410  'to 410'
            358_0  COME_FROM           338  '338'

 L. 342       358  LOAD_FAST                'event'
              360  LOAD_GLOBAL              DIFF
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   384  'to 384'

 L. 343       368  LOAD_GLOBAL              DistTextChange
              370  LOAD_FAST                'ld'
              372  LOAD_FAST                'rd'
              374  LOAD_FAST                'entry'
              376  CALL_FUNCTION_3       3  '3 positional arguments'
              378  YIELD_VALUE      
              380  POP_TOP          
              382  JUMP_FORWARD        410  'to 410'
            384_0  COME_FROM           364  '364'

 L. 344       384  LOAD_FAST                'event'
              386  LOAD_GLOBAL              SAME
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   642  'to 642'

 L. 345       394  LOAD_GLOBAL              DistTextChange
              396  LOAD_FAST                'ld'
              398  LOAD_FAST                'rd'
              400  LOAD_FAST                'entry'
              402  LOAD_CONST               False
              404  CALL_FUNCTION_4       4  '4 positional arguments'
              406  YIELD_VALUE      
              408  POP_TOP          
            410_0  COME_FROM           382  '382'
            410_1  COME_FROM           356  '356'
            410_2  COME_FROM           330  '330'
              410  JUMP_BACK            34  'to 34'
            412_0  COME_FROM           302  '302'
            412_1  COME_FROM           286  '286'

 L. 347       412  LOAD_FAST                'deep'
          414_416  POP_JUMP_IF_FALSE   538  'to 538'
              418  LOAD_GLOBAL              fnmatches
              420  LOAD_FAST                'entry'
              422  LOAD_STR                 '*/MANIFEST.MF'
              424  CALL_FUNCTION_2       2  '2 positional arguments'
          426_428  POP_JUMP_IF_FALSE   538  'to 538'

 L. 348       430  LOAD_FAST                'event'
              432  LOAD_GLOBAL              LEFT
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   456  'to 456'

 L. 349       440  LOAD_GLOBAL              DistContentRemoved
              442  LOAD_FAST                'ld'
              444  LOAD_FAST                'rd'
              446  LOAD_FAST                'entry'
              448  CALL_FUNCTION_3       3  '3 positional arguments'
              450  YIELD_VALUE      
              452  POP_TOP          
              454  JUMP_FORWARD        536  'to 536'
            456_0  COME_FROM           436  '436'

 L. 350       456  LOAD_FAST                'event'
              458  LOAD_GLOBAL              RIGHT
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   482  'to 482'

 L. 351       466  LOAD_GLOBAL              DistContentAdded
              468  LOAD_FAST                'ld'
              470  LOAD_FAST                'rd'
              472  LOAD_FAST                'entry'
              474  CALL_FUNCTION_3       3  '3 positional arguments'
              476  YIELD_VALUE      
              478  POP_TOP          
              480  JUMP_FORWARD        536  'to 536'
            482_0  COME_FROM           462  '462'

 L. 352       482  LOAD_FAST                'event'
              484  LOAD_GLOBAL              DIFF
              486  COMPARE_OP               ==
          488_490  POP_JUMP_IF_FALSE   510  'to 510'

 L. 353       492  LOAD_GLOBAL              DistManifestChange
              494  LOAD_FAST                'ld'
              496  LOAD_FAST                'rd'
              498  LOAD_FAST                'entry'
              500  LOAD_CONST               True
              502  CALL_FUNCTION_4       4  '4 positional arguments'
              504  YIELD_VALUE      
              506  POP_TOP          
              508  JUMP_FORWARD        536  'to 536'
            510_0  COME_FROM           488  '488'

 L. 354       510  LOAD_FAST                'event'
              512  LOAD_GLOBAL              SAME
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   642  'to 642'

 L. 355       520  LOAD_GLOBAL              DistManifestChange
              522  LOAD_FAST                'ld'
              524  LOAD_FAST                'rd'
              526  LOAD_FAST                'entry'
              528  LOAD_CONST               False
              530  CALL_FUNCTION_4       4  '4 positional arguments'
              532  YIELD_VALUE      
              534  POP_TOP          
            536_0  COME_FROM           508  '508'
            536_1  COME_FROM           480  '480'
            536_2  COME_FROM           454  '454'
              536  JUMP_BACK            34  'to 34'
            538_0  COME_FROM           426  '426'
            538_1  COME_FROM           414  '414'

 L. 358       538  LOAD_FAST                'event'
              540  LOAD_GLOBAL              LEFT
              542  COMPARE_OP               ==
          544_546  POP_JUMP_IF_FALSE   564  'to 564'

 L. 359       548  LOAD_GLOBAL              DistContentRemoved
              550  LOAD_FAST                'ld'
              552  LOAD_FAST                'rd'
              554  LOAD_FAST                'entry'
              556  CALL_FUNCTION_3       3  '3 positional arguments'
              558  YIELD_VALUE      
              560  POP_TOP          
              562  JUMP_BACK            34  'to 34'
            564_0  COME_FROM           544  '544'

 L. 360       564  LOAD_FAST                'event'
              566  LOAD_GLOBAL              RIGHT
              568  COMPARE_OP               ==
          570_572  POP_JUMP_IF_FALSE   590  'to 590'

 L. 361       574  LOAD_GLOBAL              DistContentAdded
              576  LOAD_FAST                'ld'
              578  LOAD_FAST                'rd'
              580  LOAD_FAST                'entry'
              582  CALL_FUNCTION_3       3  '3 positional arguments'
              584  YIELD_VALUE      
              586  POP_TOP          
              588  JUMP_BACK            34  'to 34'
            590_0  COME_FROM           570  '570'

 L. 362       590  LOAD_FAST                'event'
              592  LOAD_GLOBAL              DIFF
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_FALSE   618  'to 618'

 L. 363       600  LOAD_GLOBAL              DistContentChange
              602  LOAD_FAST                'ld'
              604  LOAD_FAST                'rd'
              606  LOAD_FAST                'entry'
              608  LOAD_CONST               True
              610  CALL_FUNCTION_4       4  '4 positional arguments'
              612  YIELD_VALUE      
              614  POP_TOP          
              616  JUMP_BACK            34  'to 34'
            618_0  COME_FROM           596  '596'

 L. 364       618  LOAD_FAST                'event'
              620  LOAD_GLOBAL              SAME
              622  COMPARE_OP               ==
              624  POP_JUMP_IF_FALSE    34  'to 34'

 L. 365       626  LOAD_GLOBAL              DistContentChange
              628  LOAD_FAST                'ld'
              630  LOAD_FAST                'rd'
              632  LOAD_FAST                'entry'
              634  LOAD_CONST               False
              636  CALL_FUNCTION_4       4  '4 positional arguments'
              638  YIELD_VALUE      
              640  POP_TOP          
            642_0  COME_FROM           516  '516'
            642_1  COME_FROM           390  '390'
            642_2  COME_FROM           262  '262'
              642  JUMP_BACK            34  'to 34'
              644  POP_BLOCK        
            646_0  COME_FROM_LOOP       20  '20'

Parse error at or near `COME_FROM' instruction at offset 284_1


class DistReport(DistChange):
    __doc__ = '\n    This class has side-effects. Running the check method with the\n    reportdir option set to True will cause the deep checks to be\n    written to file in that directory\n    '
    report_name = 'DistReport'

    def __init__(self, l, r, reporter):
        self.reporter = reporter
        options = reporter.options
        shallow = getattr(options, 'shallow', False)
        DistChange.__init__(self, l, r, shallow)

    def collect_impl(self):
        """
        overrides DistJarChange and DistClassChange from the underlying
        DistChange with DistJarReport and DistClassReport instances
        """
        for c in DistChange.collect_impl(self):
            if isinstance(c, DistJarChange):
                if c.is_change():
                    ln = DistJarReport.report_name
                    nr = self.reporter.subreporter(c.entry, ln)
                    c = DistJarReport(c.ldata, c.rdata, c.entry, nr)
            elif isinstance(c, DistClassChange):
                if c.is_change():
                    ln = DistClassReport.report_name
                    nr = self.reporter.subreporter(c.entry, ln)
                    c = DistClassReport(c.ldata, c.rdata, c.entry, nr)
            yield c

    def mp_check_impl(self, process_count):
        """
        a multiprocessing-enabled check implementation. Will create up to
        process_count helper processes and use them to perform the
        DistJarReport and DistClassReport actions.
        """
        from multiprocessing import Process, Queue
        options = self.reporter.options
        func = _mp_run_check
        self.reporter.setup()
        changes = list(self.collect_impl())
        task_count = 0
        tasks = Queue()
        results = Queue()
        try:
            for index in range(0, len(changes)):
                change = changes[index]
                if isinstance(change, (DistJarReport, DistClassReport)):
                    changes[index] = None
                    tasks.put((index, change))
                    task_count += 1

            process_count = min(process_count, task_count)
            for _i in range(0, process_count):
                tasks.put(None)
                process = Process(target=func, args=(tasks, results, options))
                process.daemon = False
                process.start()

            for change in changes:
                if change:
                    change.check()

            for _i in range(0, task_count):
                index, change = results.get()
                changes[index] = change

        except KeyboardInterrupt:
            for _change in iter(tasks.get, None):
                pass

            raise

        c = False
        for change in changes:
            c = c or change.is_change()

        self.changes = changes
        return (c, None)

    def check_impl(self):
        options = self.reporter.options
        forks = getattr(options, 'processes', 0)
        if forks:
            return self.mp_check_impl(forks)
        changes = list()
        c = False
        for change in self.collect_impl():
            change.check()
            c = c or change.is_change()
            if isinstance(change, (DistJarReport, DistClassReport)):
                changes.append(squash(change, options=options))
                change.clear()
            else:
                changes.append(change)

        self.changes = changes
        return (c, None)

    def check(self):
        DistChange.check(self)
        self.reporter.run(self)


def _mp_run_check(tasks, results, options):
    """
    a helper function for multiprocessing with DistReport.
    """
    try:
        for index, change in iter(tasks.get, None):
            change.check()
            squashed = squash(change, options=options)
            change.clear()
            results.put((index, squashed))

    except KeyboardInterrupt:
        return


def cli_dist_diff(options, left, right):
    from .report import quick_report, Reporter
    from .report import JSONReportFormat, TextReportFormat
    reports = getattr(options, 'reports', tuple())
    if reports:
        rdir = options.report_dir or './'
        rpt = Reporter(rdir, 'DistReport', options)
        rpt.add_formats_by_name(reports)
        delta = DistReport(left, right, rpt)
    else:
        delta = DistChange(left, right, options.shallow)
    delta.check()
    if not options.silent:
        if options.json:
            quick_report(JSONReportFormat, delta, options)
        else:
            quick_report(TextReportFormat, delta, options)
    if not delta.is_change() or delta.is_ignored(options):
        return 0
    return 1


def cli(options):
    left, right = options.dist
    return cli_dist_diff(options, left, right)


def add_distdiff_optgroup(parser):
    """
    Option group relating to the use of a DistChange or DistReport
    """
    cpus = cpu_count()
    og = parser.add_argument_group('Distribution Checking Options')
    og.add_argument('--processes', type=int, default=cpus, help=('Number of child processes to spawn to handle sub-reports. Set to 0 to disable multi-processing. Defaults to the number of CPUs (%r)' % cpus))
    og.add_argument('--shallow', action='store_true', default=False, help='Check only that the files of this dist havechanged, do not infer the meaning')
    og.add_argument('--ignore-filenames', action='append', default=[], help='file glob to ignore. Can be specified multiple times')
    og.add_argument('--ignore-trailing-whitespace', action='store_true',
      default=False,
      help='ignore trailing whitespace when comparing text files')


def create_optparser(progname=None):
    """
    an OptionParser instance filled with options and groups
    appropriate for use with the distdiff command
    """
    from . import report
    parser = ArgumentParser(prog=progname)
    parser.add_argument('dist', nargs=2, help='distributions to compare')
    add_general_optgroup(parser)
    add_distdiff_optgroup(parser)
    add_jardiff_optgroup(parser)
    add_classdiff_optgroup(parser)
    report.add_general_report_optgroup(parser)
    report.add_json_report_optgroup(parser)
    report.add_html_report_optgroup(parser)
    return parser


def default_distdiff_options(updates=None):
    """
    generate an options object with the appropriate default values in
    place for API usage of distdiff features. overrides is an optional
    dictionary which will be used to update fields on the options
    object.
    """
    parser = create_optparser()
    options = parser.parse_args(list())
    if updates:
        options._update_careful(updates)
    return options


def main(args=sys.argv):
    """
    entry point for the distdiff command-line utility
    """
    parser = create_optparser(args[0])
    return cli(parser.parse_args(args[1:]))