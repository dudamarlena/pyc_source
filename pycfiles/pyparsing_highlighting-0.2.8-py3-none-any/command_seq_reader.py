# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/command_seq_reader.py
# Compiled at: 2009-01-14 14:04:57
__doc__ = '\nlast_assignment_or_evaluatable should return the last value assigned or otherwise\nreferred to in a stack of Python commands.\n\n>>> last_assignment_or_evaluatable(\'a=1\')\n1\n>>> last_assignment_or_evaluatable(\'a = 1\\nb = 2\')\n2\n>>> last_assignment_or_evaluatable(\'beast = "cow"\\nx = 22\\nbeast\')\n\'cow\'\n>>> last_assignment_or_evaluatable(\'f=4.0\\ni=7\\ntarget=f\')\n4.0\n>>> last_assignment_or_evaluatable(\'f=4.0\\ni=7\\ntarget=f\', types_of_interest=(int,))\n7\n'
import unittest, doctest, re
commandUnfinished = re.compile('unexpected EOF while parsing|EOL while scanning|unexpected character after line continuation character|invalid syntax')

def items_of_interest(dct, types_of_interest):
    return [ (k, v) for (k, v) in dct.items() if isinstance(v, types_of_interest) ]


def recordingexec(arg, types_of_interest=(
 int, basestring)):
    cmdbuf = []
    lastcmd = ''
    commandInProgress = []
    lastlocals = []
    for line in arg.strip().splitlines():
        cmdbuf.append(line)
        commandInProgress.append(line)
        try:
            oldlocals = items_of_interest(locals(), types_of_interest)
            exec ('\n').join(cmdbuf)
            newlocals = [ itm for itm in items_of_interest(locals(), types_of_interest) if itm not in oldlocals
                        ]
            if newlocals:
                lastlocals = newlocals
            lastcmd = ('\n').join(commandInProgress)
            commandInProgress = []
        except IndentationError:
            pass
        except SyntaxError, e:
            if not commandUnfinished.search(str(e)):
                raise
        except Exception, e:
            raise Exception, '%s:\n%s' % (e, line)

    return (
     lastcmd, dict(lastlocals))


def last_assignment_or_evaluatable(s, types_of_interest=(
 basestring, int, float)):
    s = s.strip()
    if not s:
        return
    exec s
    (lastcmd, lastlocals) = recordingexec(s, types_of_interest)
    try:
        return eval(lastcmd)
    except SyntaxError, e:
        if 'invalid syntax' not in str(e):
            raise

    if len(lastlocals) > 1:
        raise ValueError, "Multiple assignments - couldn't determine which one"
    return eval(lastlocals.keys()[0])


class RecordingExecTestSuite(unittest.TestCase):

    def testSimpleAssignments(self):
        (lastcmd, lastlocals) = recordingexec('\na = 1\nb = "cow"\nc = 3')
        self.assertEqual(lastcmd, 'c = 3')
        self.assertEqual(lastlocals, {'c': 3})

    def testIgnoreObj(self):
        (lastcmd, lastlocals) = recordingexec('\na = 1\nb = 2\nuts = unittest.TestSuite()\n', unittest.TestSuite)
        self.assertEqual(lastcmd, 'uts = unittest.TestSuite()')
        self.assertEqual(lastlocals.keys(), ['uts'])

    def testExecutableLastLine(self):
        (lastcmd, lastlocals) = recordingexec('\na = 1\nprint "hi mom"')
        self.assertEqual(lastcmd, 'print "hi mom"')
        self.assertEqual(lastlocals, {'a': 1})

    def testEvalLastLine(self):
        (lastcmd, lastlocals) = recordingexec('\na = 1\na')
        self.assertEqual(lastcmd, 'a')
        self.assertEqual(lastlocals, {'a': 1})


class last_assignment_or_evaluatableTestSuite(unittest.TestCase):

    def testSimpleAssignments(self):
        lv = last_assignment_or_evaluatable('\na = 1\nb = "cow"\nc = 3')
        self.assertEqual(lv, 3)

    def testSimpleAssignments(self):
        lv = last_assignment_or_evaluatable('\na = 1\nb = "cow"\nc = 3\nb')
        self.assertEqual(lv, 'cow')

    def testMultiAssignFail(self):
        self.assertRaises(ValueError, last_assignment_or_evaluatable, '\na = 1\n(b, c) = (2, 3)')

    def testEmpty(self):
        lv = last_assignment_or_evaluatable('')
        self.assertEqual(lv, None)
        return


if __name__ == '__main__':
    doctest.testmod()