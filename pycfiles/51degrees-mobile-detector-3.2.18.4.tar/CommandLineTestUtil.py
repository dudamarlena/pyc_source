# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\CommandLine\CommandLineTestUtil.py
# Compiled at: 2005-04-13 18:41:04
__doc__ = '\nCommand-line script related extensions to the test suite framework\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import os, Ft

class TestRun:
    __module__ = __name__

    def __init__(self, name, options, args, expectedOut=None, validationFunc=None, input=None, outFile=None, skipOutputTest=False, compareFunc=cmp):
        self.name = name
        self.expectedOut = expectedOut
        self.validationFunc = validationFunc
        self.input = input
        self.output = outFile
        self.skipOutputTest = skipOutputTest
        self.compareFunc = compareFunc
        self.argv = self.makeCommandLine(options, args)
        return

    def makeCommandLine(self, options, args):
        argv = []
        for (name, value) in options.items():
            if value:
                if ' ' in str(value):
                    value = '"%s"' % value
                option = '--%s=%s' % (name, value)
            else:
                option = '--%s' % name
            argv.append(option)

        for arg in args:
            if ' ' in str(arg):
                arg = '"%s"' % arg
            argv.append(arg)

        return (' ').join(argv)

    def test(self, tester, script):
        title = script + ' ' + self.argv
        script = os.path.join(Ft.GetConfigVar('BINDIR'), script)
        command = script + ' ' + self.argv
        tester.startGroup(self.name)
        tester.startTest(title)
        if self.skipOutputTest:
            if self.input:
                pipe = os.popen(command, 'w')
                pipe.write(self.input)
                status = pipe.close()
            pipe = os.popen(command, 'r')
            result = pipe.read()
            try:
                status = pipe.close()
            except IOError, e:
                status = -1
            else:
                if status is not None:
                    (input, output) = os.popen4(command)
                    input.close()
                    error = output.read()
                    try:
                        output.close()
                    except IOError:
                        pass
                    else:
                        tester.error("Error executing '%s':\n%s" % (script, error))
        else:
            (input, output) = os.popen4(command)
            if self.input:
                input.write(self.input)
            input.close()
            result = output.read()
            try:
                output.close()
            except IOError:
                pass

            if self.output:
                f = open(self.output)
                result = f.read()
                f.close()
                os.remove(self.output)
            if result:
                if not self.expectedOut:
                    tester.warning('Unexpected output:\n%r' % result)
                else:
                    tester.compare(self.expectedOut, result, func=self.compareFunc, diff=1)
            elif self.expectedOut:
                tester.error('Missing expected output:\n%r' % self.expectedOut)
        if self.validationFunc and not self.validationFunc(tester):
            tester.error('Validation Failed')
        tester.testDone()
        tester.groupDone()
        return
        return


class Test:
    __module__ = __name__

    def __init__(self, commandName, runs):
        self.commandName = commandName
        self.runs = runs
        return

    def test(self, tester):
        tester.startGroup('Command-line %r' % self.commandName)
        for run in self.runs:
            run.test(tester, self.commandName)

        tester.groupDone()