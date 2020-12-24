# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/static/AJS/AJS_minify.py
# Compiled at: 2006-12-26 17:18:07
import re, sys
from sets import Set
DOM_SHORTCUTS = [
 'ul', 'li', 'td', 'tr', 'th', 'tbody', 'table', 'input', 'span', 'b', 'a', 'div', 'img', 'button', 'h1', 'h2', 'h3', 'br', 'textarea', 'form', 'p', 'select', 'option', 'iframe', 'script', 'center', 'dl', 'dt', 'dd', 'small', 'pre', 'tn']
FN_SHORTCUTS = {'$': 'getElement', '$$': 'getElements', '$f': 'getFormElement', '$b': 'bind', '$A': 'createArray', 'DI': 'documentInsert', 'ACN': 'appendChildNodes', 'RCN': 'replaceChildNodes', 'AEV': 'addEventListener', 'REV': 'removeEventListener', '$bytc': 'getElementsByTagAndClassName'}
AJS_TEMPLATE = '//AJS JavaScript library (minify\'ed version)\n//Copyright (c) 2006 Amir Salihefendic. All rights reserved.\n//Copyright (c) 2005 Bob Ippolito. All rights reserved.\n//License: http://www.opensource.org/licenses/mit-license.php\n//Visit http://orangoo.com/AmiNation/AJS for full version.\nAJS = {\nBASE_URL: "",\ndrag_obj: null,\ndrag_elm: null,\n_drop_zones: [],\n_cur_pos: null,\n\n%(functions)s\n}\n\nAJS.$ = AJS.getElement;\nAJS.$$ = AJS.getElements;\nAJS.$f = AJS.getFormElement;\nAJS.$b = AJS.bind;\nAJS.$A = AJS.createArray;\nAJS.DI = AJS.documentInsert;\nAJS.ACN = AJS.appendChildNodes;\nAJS.RCN = AJS.replaceChildNodes;\nAJS.AEV = AJS.addEventListener;\nAJS.REV = AJS.removeEventListener;\nAJS.$bytc = AJS.getElementsByTagAndClassName;\n\nAJS.addEventListener(window, \'unload\', AJS._unloadListeners);\nAJS._createDomShortcuts()\n\n%(AJSDeferred)s'
AJS_SRC = 'AJS.js'
AJS_MINI_SRC = 'AJS_mini.js'

def getAjsCode():
    return open(AJS_SRC).read()


def writeAjsMini(code):
    open(AJS_MINI_SRC, 'w').write(code)


class AjsAnalyzer:
    __module__ = __name__

    def __init__(self):
        self.code = getAjsCode()
        self.ajs_fns = {}
        self.ajs_deps = {}
        self._parseAJS()
        self._findDeps()

    def _parseAJS(self):
        ajs_code = re.search('AJS =(.|\n)*\n}\n', self.code).group(0)
        fns = re.findall('\\s+((\\w*?):(.|\n)*?\n\\s*}),\n', ajs_code)
        for f in fns:
            self.ajs_fns[f[1]] = f[0]

    def getFnCode(self, fn_name):
        """
        Returns the code of function and it's dependencies as a list
        """
        fn_name = self._unfoldFn(fn_name)
        r = []
        if self.ajs_fns.get(fn_name):
            r.append(self.ajs_fns[fn_name])
            for dep_fn in self.ajs_deps[fn_name]:
                if fn_name != dep_fn:
                    r.extend(self.getFnCode(dep_fn))

        return r

    def getAjsDeferredCode(self):
        return re.search('AJSDeferred =(.|\n)*\n}\n', self.code).group(0)

    def _findDeps(self):
        """
        Parses AJS and for every function it finds dependencies for the other functions.
        """
        for (fn_name, fn_code) in self.ajs_fns.items():
            self.ajs_deps[fn_name] = self._findFns(fn_code)

    def _findFns(self, inner):
        """
        Searches after AJS.fnX( in inner and returns all the fnX in a Set.
        """
        s = re.findall('AJS\\.([\\w_$]*?)(?:\\(|,)', inner)
        s = list(Set(s))
        return self._unfoldFns(s)

    def _unfoldFns(self, list):
        """
        Unfolds:
          AJS.B, AJS.H1 etc. to _createDomShortcuts
          AJS.$ to AJS.getElement etc.
        """
        return [ self._unfoldFn(n) for n in list ]

    def _unfoldFn(self, fn_name):
        if fn_name.lower() in DOM_SHORTCUTS:
            return '_createDomShortcuts'
        elif FN_SHORTCUTS.get(fn_name):
            return FN_SHORTCUTS[fn_name]
        else:
            return fn_name


class ExternalCodeAnalyzer:
    __module__ = __name__

    def __init__(self, files):
        self.found_ajs_fns = []
        self.files = files

    def findFunctions(self):
        for f in self.files:
            self.found_ajs_fns.extend(self._parseFile(f))

        return list(Set(self.found_ajs_fns))

    def _parseFile(self, f):
        """
        Parses the file, looks for AJS functions and returns all the found functions.
        """
        code = open(f).read()
        return re.findall('AJS\\.([\\w_$]*?)\\(', code)


class AjsComposer:
    __module__ = __name__

    def __init__(self, fn_list):
        self.code = getAjsCode()
        self.analyzer = AjsAnalyzer()
        self.fn_list = fn_list
        self.fn_list.extend(['_unloadListeners', 'createDOM', '_createDomShortcuts'])
        in_list = lambda x: x in self.fn_list
        if in_list('getRequest') or in_list('loadJSONDoc'):
            self.deferred = self._minify(self.analyzer.getAjsDeferredCode())
            self.fn_list.append('isObject')
        else:
            self.deferred = ''

    def writeToOutput(self):
        fns = self._getFns()
        d = {}
        d['functions'] = (',\n').join(fns)
        d['AJSDeferred'] = self.deferred
        mini_code = AJS_TEMPLATE % d
        writeAjsMini(mini_code)

    def _minify(self, code):
        new_lines = []
        for l in code.split('\n'):
            if l not in ['\n', '']:
                new_lines.append(l.lstrip())

        return ('\n').join(new_lines)

    def _getFns(self):
        r = []
        for fn in self.fn_list:
            r.extend(self.analyzer.getFnCode(fn))

        r = list(Set(r))
        return [ self._minify(fn) for fn in r ]


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print "Usage is:\n      python AJS_minify.py ajs_file js_file.js html_using_ajs.html ...\n    Example usage:\n      Using relative paths:\n        python AJS_minify.py AJS.js test.js index.html\n      Using absolute paths:\n        python AJS_minify.py ~/Desktop/AJS/AJS.js ~/Desktop/GreyBox_v3_42/greybox/greybox.js\n    This will create a new file called '%s' that has the needed AJS functions." % AJS_MINI_SRC
        sys.exit(0)
    FILES = sys.argv[2:]
    print 'Parsing through:\n  %s' % ('\n  ').join(FILES)
    code_analyzer = ExternalCodeAnalyzer(FILES)
    found_fns = code_analyzer.findFunctions()
    print 'Found following AJS functions:\n  %s' % ('\n  ').join(found_fns)
    composer = AjsComposer(found_fns)
    composer.writeToOutput()
    print "Written the minified code to '%s'" % AJS_MINI_SRC