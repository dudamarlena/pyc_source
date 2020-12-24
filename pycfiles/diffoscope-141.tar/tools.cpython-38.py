# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lamby/git/debian/reproducible-builds/diffoscope/tests/utils/tools.py
# Compiled at: 2020-04-15 14:13:01
# Size of source mod 2**32: 6683 bytes
import os, pytest, functools, importlib.util, subprocess
from distutils.spawn import find_executable
from distutils.version import LooseVersion
from diffoscope.tools import get_package_provider

def file_version():
    return subprocess.check_output(('file', '-v')).decode('utf-8').splitlines()[0].split('-')[(-1)]


def tools_missing(*required):
    return not required or any((find_executable(x) is None for x in required))


def skipif(*args, **kwargs):
    """
    Call `pytest.mark.skipif` with the specified arguments.

    If `check_env_for_missing_tools=True` is passed and the
    `DIFFOSCOPE_TESTS_FAIL_ON_MISSING_TOOLS` environment variable is exported,
    this alters the behaviour such that a tool listed within this variable is
    treated as a failed test instead of being skipped.

    For more information on the rationale here, see issue #35.
    """
    if not kwargs.get('check_env_for_missing_tools', False):
        return (pytest.mark.skipif)(*args, **kwargs)
    key = 'DIFFOSCOPE_FAIL_TESTS_ON_MISSING_TOOLS'
    val = os.environ.get(key)
    if val is None:
        return (pytest.mark.skipif)(*args, **kwargs)
    tools_required = kwargs.get('tools', ())
    missing_tools = val.split() + ['/missing']
    if not tools_required or any((x for x in tools_required if x in missing_tools)):
        return (pytest.mark.skipif)(*args, **kwargs)
    msg = '{} ({}={!r})'.format(kwargs['reason'], key, val)

    def outer(*args1, **kwargs1):

        def inner(*args2, **kwargs2):
            if args[0]:
                return pytest.fail(msg)

        return inner

    return outer


def skip_unless_tools_exist(*required):
    return skipif(tools_missing(*required),
      reason=reason(*required),
      tools=required,
      check_env_for_missing_tools=True)


def skip_if_tool_version_is(tool, actual_ver, target_ver, vcls=LooseVersion):
    if tools_missing(tool):
        return skipif(True, reason=(reason(tool)), tools=(tool,))
    if callable(actual_ver):
        actual_ver = actual_ver()
    return skipif((vcls(str(actual_ver)) == vcls(str(target_ver))),
      reason=('requires {} != {} ({} detected)'.format(tool, target_ver, actual_ver)),
      tools=(
     tool,))


def skip_unless_tool_is_at_least(tool, actual_ver, min_ver, vcls=LooseVersion):
    if tools_missing(tool):
        if module_is_not_importable(tool):
            return skipif(True, reason=(reason(tool)), tools=(tool,))
    if callable(actual_ver):
        actual_ver = actual_ver()
    return skipif((vcls(str(actual_ver)) < vcls(str(min_ver))),
      reason=('{} >= {} ({} detected)'.format(reason(tool), min_ver, actual_ver)),
      tools=(
     tool,))


def skip_unless_tool_is_at_most(tool, actual_ver, max_ver, vcls=LooseVersion):
    if tools_missing(tool):
        if module_is_not_importable(tool):
            return skipif(True, reason=(reason(tool)), tools=(tool,))
    if callable(actual_ver):
        actual_ver = actual_ver()
    return skipif((vcls(str(actual_ver)) > vcls(str(max_ver))),
      reason=('{} <= {} ({} detected)'.format(reason(tool), max_ver, actual_ver)),
      tools=(
     tool,))


def skip_unless_tool_is_between(tool, actual_ver, min_ver, max_ver, vcls=LooseVersion):
    if tools_missing(tool):
        return skipif(True, reason=(reason(tool)), tools=(tool,))
    if callable(actual_ver):
        actual_ver = actual_ver()
    return skipif((vcls(str(actual_ver)) < vcls(str(min_ver)) or vcls(str(actual_ver)) > vcls(str(max_ver))),
      reason=('{} min {} >= {} ({} detected)'.format(reason(tool), min_ver, max_ver, actual_ver)),
      tools=(
     tool,))


def skip_if_binutils_does_not_support_x86():
    if tools_missing('objdump'):
        return skip_unless_tools_exist('objdump')
    return skipif(('elf64-x86-64' not in get_supported_elf_formats()),
      reason='requires a binutils capable of reading x86-64 binaries',
      tools=('objdump', ))


@functools.lru_cache()
def get_supported_elf_formats():
    return set(subprocess.check_output(('objdump', '--info')).decode('utf-8').splitlines())


def module_is_not_importable--- This code section failed: ---

 L. 180         0  SETUP_FINALLY        38  'to 38'

 L. 181         2  LOAD_GLOBAL              importlib
                4  LOAD_ATTR                util
                6  LOAD_METHOD              find_spec
                8  LOAD_FAST                'x'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 182        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L. 187        24  LOAD_GLOBAL              importlib
               26  LOAD_METHOD              import_module
               28  LOAD_FAST                'x'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_FORWARD         60  'to 60'
             38_0  COME_FROM_FINALLY     0  '0'

 L. 188        38  DUP_TOP          
               40  LOAD_GLOBAL              ImportError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 191        52  POP_EXCEPT       
               54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'
               58  END_FINALLY      
             60_0  COME_FROM            36  '36'

 L. 193        60  LOAD_CONST               False
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 20


def skip_unless_module_exists(name):
    return skipif((module_is_not_importable(name)),
      reason=('requires {} Python module'.format(name)),
      tools=('{}_module'.format(name)))


def skip_unless_file_version_is_at_least(version):
    return skip_unless_tool_is_at_least('file', file_version, version)


def reason(*tools):
    xs = []
    for x in tools:
        provider = get_package_provider(x)
        if provider is None:
            xs.append(x)
        else:
            xs.append('{} (try installing {})'.format(x, provider))
    else:
        return 'requires {}'.format(' and '.join(xs))