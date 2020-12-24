# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\selftest.py
# Compiled at: 2009-11-09 10:54:08
import mod2doctest
from mod2doctest import m2d_print

def fix_output(input):
    return ('\n+ ').join(input.replace('>>', '|>').replace('..', '|.').split('\n'))


file = '\nimport sys\nimport os\nprint "Current dir is \'%s\'" % os.getcwd()\n\n'
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
file = '\nclass MyClass(object):\n    pass\n\nprint MyClass\nprint MyClass()\n\n'
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
file = '\nimport os\nimport pickle\nprint pickle.dumps(os)\n\n'
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
file = '\n#===============================================================================\n# Header\n#===============================================================================\n# Comment Level 1\n## Double Comments\n### Triple Comments\n\n'
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
file = "\nprint 'Only one line break'\n\nprint 'Two line breaks'\n\n\nprint 'Six line breaks'\n\n\n\n\n\nprint 'DONE!'\n"
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
file = "\nfrom mod2doctest import m2d_print\n#===============================================================================\nm2d_print.h1('HEADER 1')\n#===============================================================================\n\n\nm2d_print.h2('HEADER 2')\n#-------------------------------------------------------------------------------\n\n"
print fix_output(mod2doctest.convert(src=file, target=None, run_doctest=False, add_testmod=False))
if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(src=None, target='selftest_test.py', run_doctest=True, add_testmod=True)