# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpcspy/mpcspy.py
# Compiled at: 2020-01-09 00:54:46
# Size of source mod 2**32: 6420 bytes
import ast, sys, types, importlib, site

def check(node_or_string, allowed_modules={}, allowed_functions=[]):
    aliases = {}
    if isinstance(node_or_string, str):
        node_or_string = ast.parse(node_or_string, mode='exec')
    if isinstance(node_or_string, ast.Module):
        node_or_string = node_or_string.body

    def check_package(name):
        lib_path = importlib.find_loader(name).path
        local_site = site.getusersitepackages()
        local_site = '/'.join(local_site.split('/')[:-1])
        global_sites = site.getsitepackages()
        for global_site in global_sites:
            global_site = '/'.join(global_site.split('/')[:-1])
            if global_site in lib_path:
                return True
            if local_site in lib_path:
                return True
            return False

    def _check(node):
        if hasattr(node, 'values'):
            for value in node.values:
                _check(value)
            else:
                if hasattr(node, 'elts'):
                    for value in node.elts:
                        _check(value)
                    else:
                        if hasattr(node, 'body'):
                            for exp in node.body:
                                _check(exp)
                            else:
                                if isinstance(node, ast.Expr):
                                    _check(node.value)
                                    return
                                    if isinstance(node, ast.Constant):
                                        return
                                    if isinstance(node, (ast.Str, ast.Bytes)):
                                        return
                                    if isinstance(node, ast.Num):
                                        return
                                    if isinstance(node, ast.Tuple):
                                        return
                                    if isinstance(node, ast.List):
                                        return
                                    if isinstance(node, ast.Set):
                                        return
                                    if isinstance(node, ast.Dict):
                                        return
                                    if isinstance(node, ast.NameConstant):
                                        return
                                    if isinstance(node, ast.BinOp):
                                        _check(node.right)
                                        _check(node.left)
                                        return None
                                    if isinstance(node, ast.For):
                                        _check(node.iter)
                                        return None
                                    if isinstance(node, ast.While):
                                        _check(node.test)
                                        return None
                                    if isinstance(node, ast.Compare):
                                        for exp in node.comparators:
                                            _check(exp)
                                        else:
                                            _check(node.left)
                                            return None

                                    if isinstance(node, ast.FunctionDef):
                                        for arg in node.args.defaults:
                                            _check(arg)
                                        else:
                                            return

                                    if isinstance(node, ast.Return):
                                        _check(node.value)
                                        return None
                                    if isinstance(node, ast.Pass):
                                        return
                                    if isinstance(node, ast.ClassDef):
                                        for base in node.bases:
                                            _check(base)
                                        else:
                                            return

                                    if isinstance(node, ast.AnnAssign):
                                        _check(node.target)
                                        _check(node.value)
                                        return None
                                    if isinstance(node, ast.Assign):
                                        for target in node.targets:
                                            _check(target)
                                        else:
                                            _check(node.value)
                                            return None

                                    if isinstance(node, ast.Name):
                                        if node.id in aliases.keys():
                                            raise ValueError('Assigning modules is not allowed')
                                        return
                                elif isinstance(node, ast.Import):
                                    for alias in node.names:
                                        if alias.name not in allowed_modules:
                                            raise ValueError(f"{alias.name} is not allowed.")
                                        if alias.asname is not None:
                                            aliases[alias.asname] = alias.name

                                else:
                                    aliases[alias.name] = alias.name
                                if check_package(alias.name):
                                    return None
                                raise ValueError(f"{alias.name} is not allowed.")

                        else:
                            pass

                    if isinstance(node, ast.ImportFrom):
                        if node.module not in allowed_modules:
                            raise ValueError(f"{node.module} is not allowed.")
                else:
                    for alias in node.names:
                        if alias.name in allowed_modules[node.module]:
                            if alias.asname is not None:
                                aliases[alias.asname] = alias.name
                            else:
                                aliases[alias.name] = alias.name
                        else:
                            raise ValueError(f"{alias.name} from {node.module} is not allowed.")

                if check_package(node.module):
                    return
                raise ValueError(f"{node.module} is not allowed.")

        else:
            if isinstance(node, ast.Attribute):
                if hasattr(node.value, 'value'):
                    _check(node.value)
                    if isinstance(node.value, ast.Constant):
                        return
                    if node.value.attr in allowed_modules.keys() and node.attr in allowed_modules[node.value.attr]:
                        return
                elif hasattr(node, 'id'):
                    if node.id in allowed_functions:
                        return
                elif node.value.id in aliases.keys():
                    funcs = allowed_modules[aliases[node.value.id]]
                    if funcs == '':
                        return
                    if node.attr in funcs:
                        return
                elif node.attr in allowed_functions:
                    return
                if node.attr in allowed_modules[node.value.id]:
                    return
                raise ValueError(f"{node.attr} is not allowed.")
            else:
                if isinstance(node, ast.Call):
                    for arg in node.args:
                        _check(arg)
                    else:
                        if isinstance(node.func, ast.Attribute):
                            _check(node.func)
                        else:
                            if node.func.id not in allowed_functions:
                                raise ValueError(f"{node.func.id} is not allowed.")
                            return

                if isinstance(node, ast.FormattedValue):
                    _check(node.value)
                    return
                raise ValueError(f"malformed node or string: {node}")

    return [_check(node) for node in node_or_string]


def read_config(config_file, allowed_modules={}, allowed_functions=[], verbose=False):
    if not verbose:
        sys.tracebacklimit = 0
    config = types.ModuleType('config', 'Config')
    with open(config_file) as (f):
        code = f.read()
        check(code, allowed_modules=allowed_modules, allowed_functions=allowed_functions)
        code = compile(code, 'config', 'exec')
        exec(code, config.__dict__)
    sys.tracebacklimit = 1000
    return config