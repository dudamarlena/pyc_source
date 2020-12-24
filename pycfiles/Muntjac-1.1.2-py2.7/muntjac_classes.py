# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/muntjac_classes.py
# Compiled at: 2013-04-04 15:36:37
import sys, traceback
from os import listdir
from os.path import exists, dirname, join, isdir, basename
import muntjac
from muntjac.ui.component import IComponent
from muntjac.ui.component_container import IComponentContainer
from muntjac.api import PopupView, CustomComponent, LoginForm, SplitPanel, VerticalSplitPanel, HorizontalSplitPanel, Window
from muntjac.ui.drag_and_drop_wrapper import DragAndDropWrapper
from muntjac.util import clsname, loadClass

class MuntjacClasses(object):

    @classmethod
    def main(cls, args):
        print 'ComponentContainers'
        print '==================='
        for c in cls.getComponentContainers():
            print clsname(c)

        print
        print 'Components'
        print '=========='
        for c in cls.getComponents():
            print clsname(c)

        print
        print 'Server side classes'
        print '==================='
        for c in cls.getAllServerSideClasses():
            print clsname(c)

    @classmethod
    def getComponents(cls):
        try:
            return cls.findClasses(IComponent, 'muntjac.ui')
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()

    @classmethod
    def getAllServerSideClasses(cls):
        try:
            return cls.findClassesNoTests(object, 'muntjac', [
             'muntjac.tests', 'muntjac.terminal.gwt.client'])
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()

    @classmethod
    def getComponentContainers(cls):
        try:
            return cls.findClasses(IComponentContainer, 'muntjac.ui')
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()

    @classmethod
    def getComponentContainersSupportingAddRemoveComponent(cls):
        classes = cls.getComponentContainers()
        classes.remove(PopupView)
        classes.remove(CustomComponent)
        classes.remove(DragAndDropWrapper)
        classes.remove(LoginForm)
        return classes

    @classmethod
    def getComponentContainersSupportingUnlimitedNumberOfComponents(cls):
        classes = cls.getComponentContainersSupportingAddRemoveComponent()
        classes.remove(SplitPanel)
        classes.remove(VerticalSplitPanel)
        classes.remove(HorizontalSplitPanel)
        classes.remove(Window)
        return classes

    @classmethod
    def findClasses(cls, baseClass, basePackage, ignoredPackages=None):
        if ignoredPackages == None:
            ignoredPackages = []
        classes = list()
        basePackageDirName = '/' + basePackage.replace('.', '/')
        location = cls.getResource(basePackageDirName)
        if not exists(location):
            raise IOError('Directory ' + location + ' does not exist')
        cls.findPackages(location, basePackage, baseClass, classes, ignoredPackages)
        classes.sort(key=lambda klass: clsname(klass))
        return classes

    @classmethod
    def findClassesNoTests(cls, baseClass, basePackage, ignoredPackages):
        classes = cls.findClasses(baseClass, basePackage, ignoredPackages)
        classesNoTests = list()
        for clazz in classes:
            if 'Test' not in clsname(clazz):
                testPresent = False
                if not testPresent:
                    classesNoTests.append(clazz)

        return classesNoTests

    @classmethod
    def findPackages(cls, parent, package, baseClass, result, ignoredPackages):
        exceptions = [
         '__init__.py', 'util.py', 'api.py']
        for ignoredPackage in ignoredPackages:
            if package == ignoredPackage:
                return

        for f in listdir(parent):
            if isdir(f):
                cls.findPackages(file, package + '.' + basename(f), baseClass, result, ignoredPackages)
            elif f.endswith('.py') and basename(f) not in exceptions:
                fullyQualifiedClassName = cls.fullyQualifiedName(package, f)
                cls.addClassIfMatches(result, fullyQualifiedClassName, baseClass)

    @classmethod
    def addClassIfMatches(cls, result, fullyQualifiedClassName, baseClass):
        try:
            c = loadClass(fullyQualifiedClassName)
            if issubclass(c, baseClass) and not cls.isAbstract(c):
                result.append(c)
        except AttributeError:
            pos = fullyQualifiedClassName.rfind('.')
            fullyQualifiedClassName = fullyQualifiedClassName[:pos + 1] + 'I' + fullyQualifiedClassName[pos + 1:]
            try:
                c = loadClass(fullyQualifiedClassName)
            except Exception:
                traceback.print_exc(file=sys.stdout)

        except Exception:
            traceback.print_exc(file=sys.stdout)

    @classmethod
    def getResource(cls, path):
        if path[0] == '/':
            path = path[1:]
        root = join(dirname(muntjac.__file__), '..')
        return join(root, path)

    @classmethod
    def isAbstract(self, klass):
        name = klass.__name__
        if name.startswith('_') or name.lower().startswith('abstract'):
            return True
        return False

    @classmethod
    def fullyQualifiedName(cls, package, filename):
        name = basename(filename).replace('.py', '')
        if '_' in name or name.lower() == name:
            clsname = cls.toCamel(name)
        else:
            clsname = name
        return package + '.' + name + '.' + clsname

    @classmethod
    def toCamel(cls, name):
        camel = ''
        lastWasUnderScore = False
        for i, c in enumerate(name):
            if i == 0:
                camel += c.upper()
            elif lastWasUnderScore:
                camel += c.upper()
                lastWasUnderScore = False
            elif c == '_':
                lastWasUnderScore = True
            else:
                camel += c

        return camel


if __name__ == '__main__':
    MuntjacClasses.main(sys.argv)