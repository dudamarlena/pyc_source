# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/parsing.py
# Compiled at: 2009-10-07 18:08:46


class ArgumentsError(Exception):
    __module__ = __name__


def require_modules(option, *modules):
    assert len(modules) > 0
    missing_modules = []
    for modulename in modules:
        try:
            __import__(modulename)
        except ImportError:
            missing_modules.append(modulename)

    if missing_modules:
        raise ArgumentsError("option '%(option)s' requires missing modules %(missing_modules)s" % vars())


def require_posix(option):
    try:
        import posix
    except ImportError:
        raise ArgumentsError("option '%s' requires a POSIX environment" % option)


def _parser():
    usage = "%prog [options] [test1 [test2 [...]]]\n\nexamples:\n  %prog                          - run default set of tests\n  %prog MyTestSuite              - run suite 'MyTestSuite'\n  %prog MyTestCase.testSomething - run MyTestCase.testSomething\n  %prog MyTestCase               - run all 'test*' test methods in MyTestCase"
    try:
        import optparse
    except ImportError:
        from testoob.compatibility import optparse

    formatter = optparse.TitledHelpFormatter(max_help_position=30)
    from testoob import __version__ as version
    return optparse.OptionParser(usage=usage, formatter=formatter, version='Testoob %s' % version)


parser = _parser()
option_processors = []