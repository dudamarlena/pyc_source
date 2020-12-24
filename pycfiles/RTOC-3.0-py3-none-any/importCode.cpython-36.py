# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\importCode.py
# Compiled at: 2019-04-23 10:35:13
# Size of source mod 2**32: 1360 bytes


def importCode(code, name, add_to_sys_modules=0):
    """
    Import dynamically generated code as a module. code is the
    object containing the code (a string, a file handle or an
    actual compiled code object, same types as accepted by an
    exec statement). The name is the name to give to the module,
    and the final argument says wheter to add it to sys.modules
    or not. If it is added, a subsequent import statement using
    name will return this module. If it is not added to sys.modules
    import will try to load it in the normal fashion.

    import foo

    is equivalent to

    foofile = open("/path/to/foo.py")
    foo = importCode(foofile,"foo",1)

    Returns a newly generated module.
    """
    import sys, imp
    module = imp.new_module(name)
    exec(code, module.__dict__)
    if add_to_sys_modules:
        sys.modules[name] = module
    return module


if __name__ == '__main__':
    code = '\n    def testFunc():\n        print "spam!"\n\n    class testClass:\n        def testMethod(self):\n            print "eggs!"\n    '
    m = importCode(code, 'test')
    m.testFunc()
    o = m.testClass()
    o.testMethod()