# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_import_module.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1933 bytes
__all__ = ['import_module']

def import_module(module):
    """This will try to import the passed module. This will return
       the module if it was imported, or will return 'None' if
       it should not be imported.

       Parameters
       ----------
       module: str
         The name of the module to import
    """
    try:
        import importlib
        m = importlib.import_module(module)
    except SyntaxError as e:
        try:
            print(f"\nSyntax error when importing {module}")
            print(f"{e.__class__.__name__}:{e}")
            print(f"Line {e.lineno}.{e.offset}:{(e.offset - 1) * ' '} |")
            print(f"Line {e.lineno}.{e.offset}:{(e.offset - 1) * ' '}\\|/")
            print(f"Line {e.lineno}.{e.offset}: {e.text}\n")
            m = None
        finally:
            e = None
            del e

    except Exception:
        m = None

    if m is None:
        try:
            import importlib.util, os
            if os.path.exists(module):
                pyfile = module
            else:
                if os.path.exists(f"{module}.py"):
                    pyfile = f"{module}.py"
                else:
                    if os.path.exists(f"{module}.pyx"):
                        pyfile = f"{module}.pyx"
                    else:
                        pyfile = None
            if pyfile:
                spec = importlib.util.spec_from_file_location(module, pyfile)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                print(f"Loaded {module} from {pyfile}")
        except SyntaxError as e:
            try:
                print(f"\nSyntax error when reading {pyfile}")
                print(f"{e.__class__.__name__}:{e}")
                print(f"Line {e.lineno}.{e.offset}:{(e.offset - 1) * ' '} |")
                print(f"Line {e.lineno}.{e.offset}:{(e.offset - 1) * ' '}\\|/")
                print(f"Line {e.lineno}.{e.offset}: {e.text}\n")
            finally:
                e = None
                del e

        except Exception:
            pass

    return m