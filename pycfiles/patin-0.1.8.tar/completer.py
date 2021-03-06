# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugoruscitti/proyectos/patin/patin/simplegui/console/completer.py
# Compiled at: 2011-11-16 18:48:43
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QListWidget
import sys, types, inspect, StringIO, os
_HELPOUT = StringIO.StringIO
_STDOUT = sys.stdout
try:
    x = set
except NameError:
    from sets import Set as set
else:
    del x

COLWIDTH = 20

def complete(s, fname=None, imports=None, debug=False):
    """Display completion in Emacs window"""
    if not s:
        return ''
    if fname:
        os.chdir(os.path.dirname(fname))
    completions = get_all_completions(s, imports)
    completions.sort(key=lambda x: len(x), reverse=True)
    dots = s.split('.')
    result = os.path.commonprefix([ k[len(dots[(-1)]):] for k in completions ])
    if result == '' or result not in completions:
        if completions:
            width = 80
            column = width / COLWIDTH
            white = ' ' * COLWIDTH
            msg = ''
            counter = 0
            for completion in completions:
                if len(completion) < COLWIDTH:
                    msg += completion + white[len(completion):]
                    counter += 1
                else:
                    msg += completion + white[len(completion) - COLWIDTH:]
                    counter += 2
                if counter >= column:
                    counter = 0
                    msg += '\n'

        else:
            msg = 'no completions!'
        if debug:
            return set(completions)
    return result


def get_signature(s, fname=None):
    """Return info about function parameters"""
    if not s:
        return ''
    else:
        if fname:
            os.chdir(os.path.dirname(fname))
        obj = None
        sig = ''
        try:
            obj = _load_symbol(s, globals(), locals())
        except Exception as ex:
            return '%s' % ex

        if type(obj) in (types.ClassType, types.TypeType):
            obj = _find_constructor(obj)
        elif type(obj) == types.MethodType:
            obj = obj.im_func
        if type(obj) in [types.FunctionType, types.LambdaType]:
            args, varargs, varkw, defaults = inspect.getargspec(obj)
            sig = '%s: %s' % (obj.__name__,
             inspect.formatargspec(args, varargs, varkw, defaults))
        doc = getattr(obj, '__doc__', '')
        if doc and not sig:
            doc = doc.lstrip()
            pos = doc.find('\n')
            if pos < 0 or pos > 70:
                pos = 70
            sig = doc[:pos]
        return sig


def _load_symbol(s, dglobals, dlocals):
    sym = None
    dots = s.split('.')
    if not s or len(dots) == 1:
        sym = eval(s, dglobals, dlocals)
    else:
        for i in range(1, len(dots) + 1):
            s = ('.').join(dots[:i])
            if not s:
                continue
            try:
                sym = eval(s, dglobals, dlocals)
            except NameError:
                try:
                    sym = __import__(s, dglobals, dlocals, [])
                    dglobals[s] = sym
                except ImportError:
                    pass

            except AttributeError:
                try:
                    sym = __import__(s, dglobals, dlocals, [])
                except ImportError:
                    pass

    return sym


def _import_modules(imports, dglobals):
    """If given, execute import statements"""
    if imports is not None:
        for stmt in imports:
            try:
                exec stmt in dglobals
            except TypeError:
                raise TypeError('invalid type: %s' % stmt)
            except Exception:
                continue

    return


def get_all_completions(s, imports=None):
    """Return contextual completion of s (string of >= zero chars)"""
    dlocals = {}
    _import_modules(imports, globals())
    dots = s.rsplit('.', 1)
    if not s or len(dots) == 1:
        keys = set()
        keys.update(globals().keys())
        keys.update(dlocals.keys())
        import __builtin__
        keys.update(dir(__builtin__))
        keys = list(keys)
        keys.sort()
        if s:
            return [ k for k in keys if k.startswith(s) ]
        return keys
    sym = None
    for i in range(1, len(dots)):
        s = ('.').join(dots[:i])
        if not s:
            continue
        try:
            s = unicode(s)
            sym = eval(s, globals(), dlocals)
        except NameError:
            try:
                sym = __import__(s, globals(), dlocals, [])
            except ImportError:
                return []
            except AttributeError:
                try:
                    sym = __import__(s, globals(), dlocals, [])
                except ImportError:
                    pass

    if sym is not None:
        s = dots[(-1)]
        return [ k for k in dir(sym) if k.startswith(s) and not k.startswith('__') and not k.endswith('__')
               ]
    else:
        return


def _find_constructor(class_ob):
    try:
        return class_ob.__init__.im_func
    except AttributeError:
        for base in class_ob.__bases__:
            rc = _find_constructor(base)
            if rc is not None:
                return rc

    return


class CompleterWidget(QCompleter):

    def __init__(self, editor):
        QCompleter.__init__(self)
        self.setWidget(editor)
        self.popupView = QListWidget()
        self.popupView.setAlternatingRowColors(True)
        self.popupView.setWordWrap(False)
        self.setPopup(self.popupView)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def insert_completion(self):
        insert = self.popupView.currentItem().text()
        extra = insert.length() - self.completionPrefix().length()
        self.widget().textCursor().insertText(insert.right(extra))
        self.popup().hide()

    def complete(self, cr, results):
        results = [ x for x in results if not x.startswith('get_') and not x.startswith('obtener_') and not x.startswith('set_') and not x.startswith('_') and not x.startswith('definir_')
                  ]
        self.popupView.clear()
        model = self.obtain_model_items(results)
        self.setModel(model)
        self.popup().setCurrentIndex(model.index(0, 0))
        cr.setWidth(self.popup().sizeHintForColumn(0) + self.popup().verticalScrollBar().sizeHint().width() + 10)
        self.popupView.updateGeometries()
        QCompleter.complete(self, cr)

    def obtain_model_items(self, proposals):
        proposals.sort()
        for p in proposals:
            self.popupView.addItem(QListWidgetItem(p))

        return self.popupView.model()