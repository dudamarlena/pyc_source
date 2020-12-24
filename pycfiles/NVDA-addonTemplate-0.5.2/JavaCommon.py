# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\JavaCommon.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.JavaCommon

Stuff for processing Java.

"""
__revision__ = 'src/engine/SCons/Tool/JavaCommon.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, os.path, re
java_parsing = 1
default_java_version = '1.4'
if java_parsing:
    _reToken = re.compile('(\\n|\\\\\\\\|//|\\\\[\\\'"]|[\\\'"\\{\\}\\;\\.\\(\\)]|' + '\\d*\\.\\d*|[A-Za-z_][\\w\\$\\.]*|<[A-Za-z_]\\w+>|' + '/\\*|\\*/|\\[\\])')

    class OuterState(object):
        """The initial state for parsing a Java file for classes,
        interfaces, and anonymous inner classes."""

        def __init__(self, version=default_java_version):
            if version not in ('1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8',
                               '5', '6'):
                msg = 'Java version %s not supported' % version
                raise NotImplementedError(msg)
            self.version = version
            self.listClasses = []
            self.listOutputs = []
            self.stackBrackets = []
            self.brackets = 0
            self.nextAnon = 1
            self.localClasses = []
            self.stackAnonClassBrackets = []
            self.anonStacksStack = [[0]]
            self.package = None
            return

        def trace(self):
            pass

        def __getClassState(self):
            try:
                return self.classState
            except AttributeError:
                ret = ClassState(self)
                self.classState = ret
                return ret

        def __getPackageState(self):
            try:
                return self.packageState
            except AttributeError:
                ret = PackageState(self)
                self.packageState = ret
                return ret

        def __getAnonClassState(self):
            try:
                return self.anonState
            except AttributeError:
                self.outer_state = self
                ret = SkipState(1, AnonClassState(self))
                self.anonState = ret
                return ret

        def __getSkipState(self):
            try:
                return self.skipState
            except AttributeError:
                ret = SkipState(1, self)
                self.skipState = ret
                return ret

        def __getAnonStack(self):
            return self.anonStacksStack[(-1)]

        def openBracket(self):
            self.brackets = self.brackets + 1

        def closeBracket(self):
            self.brackets = self.brackets - 1
            if len(self.stackBrackets) and self.brackets == self.stackBrackets[(-1)]:
                self.listOutputs.append(('$').join(self.listClasses))
                self.localClasses.pop()
                self.listClasses.pop()
                self.anonStacksStack.pop()
                self.stackBrackets.pop()
            if len(self.stackAnonClassBrackets) and self.brackets == self.stackAnonClassBrackets[(-1)]:
                self.__getAnonStack().pop()
                self.stackAnonClassBrackets.pop()

        def parseToken(self, token):
            if token[:2] == '//':
                return IgnoreState('\n', self)
            if token == '/*':
                return IgnoreState('*/', self)
            if token == '{':
                self.openBracket()
            elif token == '}':
                self.closeBracket()
            else:
                if token in ('"', "'"):
                    return IgnoreState(token, self)
                if token == 'new':
                    if len(self.listClasses) > 0:
                        return self.__getAnonClassState()
                    return self.__getSkipState()
                if token in ('class', 'interface', 'enum'):
                    if len(self.listClasses) == 0:
                        self.nextAnon = 1
                    self.stackBrackets.append(self.brackets)
                    return self.__getClassState()
                if token == 'package':
                    return self.__getPackageState()
                if token == '.':
                    return self.__getSkipState()
            return self

        def addAnonClass(self):
            """Add an anonymous inner class"""
            if self.version in ('1.1', '1.2', '1.3', '1.4'):
                clazz = self.listClasses[0]
                self.listOutputs.append('%s$%d' % (clazz, self.nextAnon))
            elif self.version in ('1.5', '1.6', '1.7', '1.8', '5', '6'):
                self.stackAnonClassBrackets.append(self.brackets)
                className = []
                className.extend(self.listClasses)
                self.__getAnonStack()[-1] = self.__getAnonStack()[(-1)] + 1
                for anon in self.__getAnonStack():
                    className.append(str(anon))

                self.listOutputs.append(('$').join(className))
            self.nextAnon = self.nextAnon + 1
            self.__getAnonStack().append(0)

        def setPackage(self, package):
            self.package = package


    class AnonClassState(object):
        """A state that looks for anonymous inner classes."""

        def __init__(self, old_state):
            self.outer_state = old_state.outer_state
            self.old_state = old_state
            self.brace_level = 0

        def parseToken(self, token):
            if token[:2] == '//':
                return IgnoreState('\n', self)
            if token == '/*':
                return IgnoreState('*/', self)
            if token == '\n':
                return self
            if token[0] == '<' and token[(-1)] == '>':
                return self
            if token == '(':
                self.brace_level = self.brace_level + 1
                return self
            if self.brace_level > 0:
                if token == 'new':
                    return SkipState(1, AnonClassState(self))
                if token in ('"', "'"):
                    return IgnoreState(token, self)
                if token == ')':
                    self.brace_level = self.brace_level - 1
                return self
            if token == '{':
                self.outer_state.addAnonClass()
            return self.old_state.parseToken(token)


    class SkipState(object):
        """A state that will skip a specified number of tokens before
        reverting to the previous state."""

        def __init__(self, tokens_to_skip, old_state):
            self.tokens_to_skip = tokens_to_skip
            self.old_state = old_state

        def parseToken(self, token):
            self.tokens_to_skip = self.tokens_to_skip - 1
            if self.tokens_to_skip < 1:
                return self.old_state
            return self


    class ClassState(object):
        """A state we go into when we hit a class or interface keyword."""

        def __init__(self, outer_state):
            self.outer_state = outer_state

        def parseToken(self, token):
            if token == '\n':
                return self
            if self.outer_state.localClasses and self.outer_state.stackBrackets[(-1)] > self.outer_state.stackBrackets[(-2)] + 1:
                locals = self.outer_state.localClasses[(-1)]
                try:
                    idx = locals[token]
                    locals[token] = locals[token] + 1
                except KeyError:
                    locals[token] = 1

                token = str(locals[token]) + token
            self.outer_state.localClasses.append({})
            self.outer_state.listClasses.append(token)
            self.outer_state.anonStacksStack.append([0])
            return self.outer_state


    class IgnoreState(object):
        """A state that will ignore all tokens until it gets to a
        specified token."""

        def __init__(self, ignore_until, old_state):
            self.ignore_until = ignore_until
            self.old_state = old_state

        def parseToken(self, token):
            if self.ignore_until == token:
                return self.old_state
            return self


    class PackageState(object):
        """The state we enter when we encounter the package keyword.
        We assume the next token will be the package name."""

        def __init__(self, outer_state):
            self.outer_state = outer_state

        def parseToken(self, token):
            self.outer_state.setPackage(token)
            return self.outer_state


    def parse_java_file(fn, version=default_java_version):
        return parse_java(open(fn, 'r').read(), version)


    def parse_java(contents, version=default_java_version, trace=None):
        """Parse a .java file and return a double of package directory,
        plus a list of .class files that compiling that .java file will
        produce"""
        package = None
        initial = OuterState(version)
        currstate = initial
        for token in _reToken.findall(contents):
            currstate = currstate.parseToken(token)
            if trace:
                trace(token, currstate)

        if initial.package:
            package = initial.package.replace('.', os.sep)
        return (
         package, initial.listOutputs)


else:

    def parse_java_file(fn):
        """ "Parse" a .java file.

        This actually just splits the file name, so the assumption here
        is that the file name matches the public class name, and that
        the path to the file is the same as the package name.
        """
        return os.path.split(file)