# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/finbull/__init__.py
# Compiled at: 2019-08-01 22:18:30
# Size of source mod 2**32: 14529 bytes
import ast, importlib, inspect, os, sys, traceback, finbull.error
__version__ = '1.0.2'

def _get_app_path():
    """
    get the app path from traceback
    """
    t = traceback.extract_stack()
    for i, k in zip(t, t[1:]):
        if k[0] == os.path.abspath(__file__) or k[0] + 'c' == os.path.abspath(__file__) or k[0] + 'o' == os.path.abspath(__file__):
            return os.path.abspath(os.path.dirname(i[0]))


def _get_decorators(cls):
    """
    get the all decorators of the class
    :param cls:
    :return:
    """
    target = cls
    decorators = {}

    def visit(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def _check_decorators(cls_name, cls, func_name, decorator_names):
    """
    check the method decorated with the decorator.
    """
    all_decorators = _get_decorators(cls)
    if func_name not in all_decorators:
        return True
    exist = bool([d for d in all_decorators[func_name] if d in decorator_names])
    if exist is False:
        raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
          errmsg=('this module[%s] function[%s] must decorate with[%s].' % (
         cls_name, func_name, decorator_names)))
    return exist


def _load_all_classes(dirname, module_list, extends):
    """
    load all class into memory
    """
    if not dirname is None:
        if not os.path.isdir(dirname):
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='load all class failed. dirname is None or error.')
        if module_list is None or len(module_list) < 1:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='load all class failed. module is None or error.')
        modules = [cls[:cls.rfind('.')] for cls in module_list]
        modules = sorted(['.'.join(reversed(m.split('.'))) for m in modules])
        for i, m in enumerate(modules):
            if i == 0 or m.find('.') == -1 or modules[(i - 1)].find('.') == -1:
                continue
            if m == modules[(i - 1)]:
                continue
            if m[:m.find('.')] == modules[(i - 1)][:modules[(i - 1)].find('.')]:
                raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                  errmsg=('finbull do not support the module that has the same name[%s:%s]' % (
                 '.'.join(reversed(m.split('.'))),
                 '.'.join(reversed(modules[(i - 1)].split('.'))))))

        classes = [cls[cls.rfind('.'):] for cls in module_list]
        same_classes = [x for x in classes if classes.count(x) > 1]
        if len(same_classes) > 0:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg=('finbull do not support the class that has the same name[%s]' % same_classes))
    else:
        sys.path.insert(0, dirname)
        try:
            for m in module_list:
                if m.count('.') >= 2:
                    tmp_module = m[:m.rfind('.', 0, m.rfind('.'))]
                    tmp_path = dirname + '/' + tmp_module.replace('.', '/')
                    sys.path.insert(0, tmp_path)
                    cur_module = m[len(tmp_module) + 1:m.rfind('.')]
                    importlib.import_module(cur_module)
                    sys.path.remove(tmp_path)
                else:
                    importlib.import_module(m[:m.rfind('.')])

        except ImportError as e:
            try:
                raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                  errmsg=('import module failed: %s. module[%s]' % (e, m)))
            finally:
                e = None
                del e

    sys.path.remove(dirname)
    all_classes = {}
    for cls in extends.__subclasses__():
        for m in module_list:
            cls_name = m[m.rfind('.') + 1:]
            if cls.__name__ == cls_name:
                all_classes[m] = cls

    return all_classes