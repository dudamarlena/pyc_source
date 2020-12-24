# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/MixIn.py
# Compiled at: 2006-10-22 17:01:01
from types import MethodType
import sys
if hasattr(sys, 'version_info') and sys.version_info[0] >= 2:

    def MixIn(pyClass, mixInClass, makeAncestor=0, mixInSuperMethods=0):
        """
                Mixes in the attributes of the mixInClass into the pyClass. These attributes are typically methods (but don't have to be). Note that private attributes, denoted by a double underscore, are not mixed in. Collisions are resolved by the mixInClass' attribute overwriting the pyClass'. This gives mix-ins the power to override the behavior of the pyClass.

                After using MixIn(), instances of the pyClass will respond to the messages of the mixInClass.

                An assertion fails if you try to mix in a class with itself.

                The pyClass will be given a new attribute mixInsForCLASSNAME which is a list of all mixInClass' that have ever been installed, in the order they were installed. You may find this useful for inspection and debugging.

                You are advised to install your mix-ins at the start up of your program, prior to the creation of any objects. This approach will result in less headaches. But like most things in Python, you're free to do whatever you're willing to live with.  :-)

                There is a bitchin' article in the Linux Journal, April 2001, "Using Mix-ins with Python" by Chuck Esterbrook which gives a thorough treatment of this topic.

                An example, that resides in Webware, is MiddleKit.Core.ModelUser.py, which install mix-ins for SQL adapters. Search for "MixIn(".

                If makeAncestor is 1, then a different technique is employed: the mixInClass is made the first base class of the pyClass. You probably don't need to use this and if you do, be aware that your mix-in can no longer override attributes/methods in pyClass.

                If mixInSuperMethods is 1, then support will be enabled for you to be able to call the original or 
                "parent" method from the mixed-in method.  This is done like so:

                    class MyMixInClass:
                        def foo(self):
                            MyMixInClass.mixInSuperFoo(self)    # call the original method
                            # now do whatever you want

                This function only exists if you are using Python 2.0 or later. Python 1.5.2 has a problem where functions (as in aMethod.im_func) are tied to their class, when in fact, they should be totally generic with only the methods being tied to their class. Apparently this was fixed in Py 2.0.
                """
        assert mixInClass is not pyClass, 'mixInClass = %r, pyClass = %r' % (mixInClass, pyClass)
        if makeAncestor:
            if mixInClass not in pyClass.__bases__:
                pyClass.__bases__ = (
                 mixInClass,) + pyClass.__bases__
        else:
            baseClasses = list(mixInClass.__bases__)
            baseClasses.reverse()
            for baseClass in baseClasses:
                MixIn(pyClass, baseClass)

        attrName = 'mixInsFor' + pyClass.__name__
        mixIns = getattr(pyClass, attrName, None)
        if mixIns is None:
            mixIns = []
            setattr(pyClass, attrName, mixIns)
        mixIns.append(mixInClass)
        for name in dir(mixInClass):
            if not name.startswith('__'):
                member = getattr(mixInClass, name)
                if type(member) is MethodType and mixInSuperMethods:
                    if hasattr(pyClass, name):
                        origmember = getattr(pyClass, name)
                        setattr(mixInClass, 'mixInSuper' + name[0].upper() + name[1:], origmember)
                if type(member) is MethodType:
                    member = member.im_func
                setattr(pyClass, name, member)

        return