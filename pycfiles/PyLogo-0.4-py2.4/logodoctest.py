# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylogo/logodoctest.py
# Compiled at: 2007-10-14 14:35:27
"""
More-or-less like doctest, except with Logo
"""
import os, doctest, sys, traceback
from cStringIO import StringIO
import reader, interpreter
from pylogo import builtins
from pylogo import oobuiltins

def testfile(filename, globs=None, name=None, verbose=None, optionflags=0, report=True, master=None, interp=None, verbose_summary=False):
    if globs is None:
        globs = {}
    if interp is None:
        interp = interpreter.RootFrame()
        interp.import_module(builtins)
        interp.import_module(oobuiltins)
    interp.vars.update(globs)
    if name is None:
        name = os.path.basename(filename)
    runner = LogoRunner(interp, verbose=verbose, optionflags=optionflags)
    s = open(filename).read()
    parser = doctest.DocTestParser()
    test = parser.get_doctest(s, globs, name, filename, 0)
    runner.run(test)
    if report:
        runner.summarize(verbose or verbose_summary)
    if master is None:
        master = runner
    else:
        master.merge(runner)
    return (
     runner.failures, runner.tries)


class LogoRunner(doctest.DocTestRunner):
    __module__ = __name__

    def __init__(self, interpreter, *args, **kw):
        doctest.DocTestRunner.__init__(self, *args, **kw)
        self.interpreter = interpreter

    def _DocTestRunner__run(self, test, compileflags, out):
        (failures, tries) = self._run(test, compileflags, out)
        self._DocTestRunner__record_outcome(test, failures, tries)
        return (failures, tries)

    def _DocTestRunner__run(self, test, compileflags, out):
        """
        Run the examples in `test`.  Write the outcome of each example
        with one of the `DocTestRunner.report_*` methods, using the
        writer function `out`.  `compileflags` is the set of compiler
        flags that should be used to execute examples.  Return a tuple
        `(f, t)`, where `t` is the number of examples tried, and `f`
        is the number of examples that failed.  The examples are run
        in the namespace `test.globs`.
        """
        failures = tries = 0
        original_optionflags = self.optionflags
        (SUCCESS, FAILURE, BOOM) = range(3)
        check = self._checker.check_output
        for (examplenum, example) in enumerate(test.examples):
            quiet = self.optionflags & doctest.REPORT_ONLY_FIRST_FAILURE and failures > 0
            self.optionflags = original_optionflags
            if example.options:
                for (optionflag, val) in example.options.items():
                    if val:
                        self.optionflags |= optionflag
                    else:
                        self.optionflags &= ~optionflag

            tries += 1
            if not quiet:
                self.report_start(out, test, example)
            filename = '<doctest %s[%d]>' % (test.name, examplenum)
            try:
                self.run_example(example.source, filename, compileflags, test.globs)
                self.debugger.set_continue()
                exception = None
            except KeyboardInterrupt:
                raise
            except:
                exception = sys.exc_info()
                self.debugger.set_continue()

            got = self._fakeout.getvalue()
            self._fakeout.truncate(0)
            outcome = FAILURE
            if exception is None:
                if check(example.want, got, self.optionflags):
                    outcome = SUCCESS
            else:
                exc_info = sys.exc_info()
                exc_msg = traceback.format_exception_only(*exc_info[:2])[(-1)]
                if not quiet:
                    got += doctest._exception_traceback(exc_info)
                if example.exc_msg is None:
                    outcome = BOOM
                elif check(example.exc_msg, exc_msg, self.optionflags):
                    outcome = SUCCESS
                elif self.optionflags & doctest.IGNORE_EXCEPTION_DETAIL:
                    m1 = re.match('[^:]*:', example.exc_msg)
                    m2 = re.match('[^:]*:', exc_msg)
                    if m1 and m2 and check(m1.group(0), m2.group(0), self.optionflags):
                        outcome = SUCCESS
            if outcome is SUCCESS:
                if not quiet:
                    self.report_success(out, test, example, got)
            elif outcome is FAILURE:
                if not quiet:
                    self.report_failure(out, test, example, got)
                failures += 1
            elif outcome is BOOM:
                if not quiet:
                    self.report_unexpected_exception(out, test, example, exc_info)
                failures += 1
            else:
                assert False, ('unknown outcome', outcome)

        self.optionflags = original_optionflags
        self._DocTestRunner__record_outcome(test, failures, tries)
        return (failures, tries)

    prompts = {None: '', 'to': '', '[': '', '(': '', 'func': ''}

    def run_example(self, source, filename, compileflags, globs):
        input = StringIO(source)
        input = reader.TrackingStream(input, name=filename)
        tokenizer = reader.FileTokenizer(input, prompt=self.prompts)
        interp = self.interpreter
        interp.push_tokenizer(tokenizer)
        try:
            v = interp.expr_top()
            if v is not None:
                print builtins.logo_repr(v)
        finally:
            interp.pop_tokenizer()
        return


if __name__ == '__main__':
    filenames = sys.argv[1:]
    for filename in filenames:
        if filename.startswith('-'):
            continue
        print 'testing', filename
        testfile(filename)