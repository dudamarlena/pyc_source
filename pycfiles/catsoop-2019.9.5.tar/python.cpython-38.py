# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/python.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4956 bytes
import os, ast, sys, time, uuid, fcntl, shutil, hashlib, logging, tempfile, resource, subprocess
LOGGER = logging.getLogger('cs')
_resource_mapper = {'CPUTIME':(
  resource.RLIMIT_CPU, lambda x: (x, x + 1)), 
 'MEMORY':(
  resource.RLIMIT_AS, lambda x: (x, x)), 
 'FILESIZE':(
  resource.RLIMIT_FSIZE, lambda x: (x, x))}

def run_code(context, code, options, count_opcodes=False, opcode_limit=None, result_as_string=False):
    if options.get('do_rlimits', True):
        rlimits = [
         (
          resource.RLIMIT_NPROC, (0, 0))]
        for key, val in _resource_mapper.items():
            if key == 'MEMORY' and options[key] <= 0:
                pass
            else:
                rlimits.append((val[0], val[1](options[key])))

    else:
        rlimits = []

    def limiter():
        os.setsid()
        for i in rlimits:
            (resource.setrlimit)(*i)
        else:
            context['csm_process'].set_pdeathsig()()

    tmpdir = context.get('csq_sandbox_dir', '/tmp/sandbox')
    this_one = '_%s' % uuid.uuid4().hex
    tmpdir = os.path.join(tmpdir, this_one)
    with open(os.path.join(context['cs_fs_root'], '__QTYPES__', 'pythoncode', '__SANDBOXES__', '_template.py')) as (f):
        template = f.read()
    template %= {'enable_opcode_count':count_opcodes, 
     'result_as_string':result_as_string, 
     'test_module':this_one, 
     'opcode_limit':opcode_limit or float('inf')}
    os.makedirs(tmpdir, 511)
    with open(os.path.join(tmpdir, 'run_catsoop_test.py'), 'w') as (f):
        f.write(template)
    for f in options['FILES']:
        typ = f[0].strip().lower()
        if typ == 'copy':
            shutil.copyfile(f[1], os.path.join(tmpdir, f[2]))
        else:
            if typ == 'string':
                with open(os.path.join(tmpdir, f[1]), 'w') as (fileobj):
                    fileobj.write(f[2])
            fname = '%s.py' % this_one
            with open(os.path.join(tmpdir, fname), 'w') as (fileobj):
                fileobj.write(code.replace('\r\n', '\n'))
            LOGGER.debug('[pythoncode.sandbox.python] context cs_version=%s, cs_python_interpreter=%s' % (
             context.get('cs_version'), context.get('cs_python_interpreter')))
            interp = context.get('csq_python_interpreter', context.get('cs_python_interpreter', 'python3'))

    try:
        p = subprocess.Popen([
         interp, '-E', '-B', 'run_catsoop_test.py'],
          cwd=tmpdir,
          preexec_fn=limiter,
          bufsize=0,
          stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
    except Exception as err:
        try:
            LOGGER.error('[pythoncode.sandbox.python] error executing subprocess, interp=%s, fname=%s, tmpdir=%s, preexec_fn=%s' % (
             interp, fname, tmpdir, limiter))
            raise Exception('[cs.qtypes.pythoncode.python] Failed to execute subprocess interp=%s (need to set csq_python_interpreter?), err=%s' % (
             interp, err))
        finally:
            err = None
            del err

    else:
        out = ''
        err = ''
        try:
            out, err = p.communicate((options['STDIN'] or ''), timeout=(options['CLOCKTIME']))
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            out, err = p.communicate()
        else:
            out = out.decode()
            err = err.decode()
            shutil.rmtree(tmpdir, True)
            n = out.rsplit('---', 1)
            log = {}
            if len(n) == 2:
                out, log = n
                try:
                    log = context['csm_util'].literal_eval(log)
                except:
                    log = {}

            elif log == {} or log.get('opcode_limit_reached', False):
                if err.strip() == '':
                    err = 'Your code did not run to completion, but no error message was returned.\nThis normally means that your code contains an infinite loop or otherwise took too long to run.'
            if len(n) > 2:
                out = ''
                log = {}
                err = 'BAD CODE - this will be logged'
            return {'fname':fname,  'out':out,  'err':err,  'info':log}