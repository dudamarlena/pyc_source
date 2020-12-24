# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Performance.py
# Compiled at: 2019-09-22 10:12:27
import hotshot, hotshot.stats, os, sys, unittest
from test import pystone
import time, Cheetah.NameMapper, Cheetah.Template
from Cheetah.compat import unicode
DEBUG = False
kPS = 1000
TOLERANCE = 0.5 * kPS

class DurationError(AssertionError):
    pass


_pystone_calibration_mark = None

def _pystone_calibration():
    global _pystone_calibration_mark
    if not _pystone_calibration_mark:
        _pystone_calibration_mark = pystone.pystones(loops=pystone.LOOPS)
    return _pystone_calibration_mark


def perftest(max_num_pystones, current_pystone=None):
    """
        Performance test decorator based off the 'timedtest'
        decorator found in this Active State recipe:
            http://code.activestate.com/recipes/440700/
    """
    if not isinstance(max_num_pystones, float):
        max_num_pystones = float(max_num_pystones)
    if not current_pystone:
        current_pystone = _pystone_calibration()

    def _test(function):

        def wrapper(*args, **kw):
            global DEBUG
            start_time = time.time()
            try:
                return function(*args, **kw)
            finally:
                total_time = time.time() - start_time
                if total_time == 0:
                    pystone_total_time = 0
                else:
                    pystone_rate = current_pystone[0] / current_pystone[1]
                    pystone_total_time = total_time / pystone_rate
                if DEBUG:
                    print 'The test "%s" took: %s pystones' % (
                     function.__name__, pystone_total_time)
                elif pystone_total_time > max_num_pystones + TOLERANCE:
                    raise DurationError('Test too long (%.2f Ps, need at most %.2f Ps)' % (
                     pystone_total_time, max_num_pystones))

        return wrapper

    return _test


class DynamicTemplatePerformanceTest(unittest.TestCase):
    loops = 10

    def test_BasicDynamic(self):
        template = '\n            #def foo(arg1, arg2)\n                #pass\n            #end def\n        '
        for i in range(self.loops):
            klass = Cheetah.Template.Template.compile(template)
            assert klass

    test_BasicDynamic = perftest(1200)(test_BasicDynamic)


class PerformanceTest(unittest.TestCase):
    iterations = 100000
    display = False
    save = False

    def runTest(self):
        self.prof = hotshot.Profile('%s.prof' % self.__class__.__name__)
        self.prof.start()
        for i in range(self.iterations):
            if hasattr(self, 'performanceSample'):
                self.display = True
                self.performanceSample()

        self.prof.stop()
        self.prof.close()
        if self.display:
            print '>>> %s (%d iterations) ' % (self.__class__.__name__,
             self.iterations)
            stats = hotshot.stats.load('%s.prof' % self.__class__.__name__)
            stats.sort_stats('time', 'calls')
            stats.print_stats(50)
        if not self.save:
            os.unlink('%s.prof' % self.__class__.__name__)


class DynamicMethodCompilationTest(PerformanceTest):

    def performanceSample(self):
        template = '\n            #import sys\n            #import os\n            #def testMethod()\n                #set foo = [1, 2, 3, 4]\n                #return $foo[0]\n            #end def\n        '
        template = Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False)
        template = template()
        value = template.testMethod()


class BunchOfWriteCalls(PerformanceTest):
    iterations = 1000

    def performanceSample(self):
        template = '\n            #import sys\n            #import os\n            #for i in range(1000)\n                $i\n            #end for\n        '
        template = Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False)
        template = template()
        value = template.respond()
        del value


class DynamicSimpleCompilationTest(PerformanceTest):

    def performanceSample(self):
        template = "\n            #import sys\n            #import os\n            #set foo = [1,2,3,4]\n\n            Well hello there! This is basic.\n\n            Here's an array too: $foo\n        "
        template = Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False)
        template = template()
        template = unicode(template)


class FilterTest(PerformanceTest):
    template = None

    def setUp(self):
        super(FilterTest, self).setUp()
        template = '\n            #import sys\n            #import os\n            #set foo = [1, 2, 3, 4]\n\n            $foo, $foo, $foo\n        '
        template = Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False)
        self.template = template()

    def performanceSample(self):
        value = unicode(self.template)


class LongCompileTest(PerformanceTest):
    """ Test the compilation on a sufficiently large template """

    def compile(self, template):
        return Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False)

    def performanceSample(self):
        template = '\n            #import sys\n            #import Cheetah.Template\n\n            #extends Cheetah.Template.Template\n\n            #def header()\n                <center><h2>This is my header</h2></center>\n            #end def\n\n            #def footer()\n                #return "Huzzah"\n            #end def\n\n            #def scripts()\n                #pass\n            #end def\n\n            #def respond()\n                <html>\n                    <head>\n                        <title>${title}</title>\n\n                        $scripts()\n                    </head>\n                    <body>\n                        $header()\n\n                        #for $i in $range(10)\n                            This is just some stupid page!\n                            <br/>\n                        #end for\n\n                        <br/>\n                        $footer()\n                    </body>\n                    </html>\n            #end def\n\n        '
        return self.compile(template)


class LongCompile_CompilerSettingsTest(LongCompileTest):

    def compile(self, template):
        return Cheetah.Template.Template.compile(template, keepRefToGeneratedCode=False, compilerSettings={'useStackFrames': True, 'useAutocalling': True})


class LongCompileAndRun(LongCompileTest):

    def performanceSample(self):
        template = super(LongCompileAndRun, self).performanceSample()
        template = template(searchList=[{'title': 'foo'}])
        template = template.respond()


if __name__ == '__main__':
    if '--debug' in sys.argv:
        DEBUG = True
        sys.argv = [ arg for arg in sys.argv if not arg == '--debug' ]
    unittest.main()