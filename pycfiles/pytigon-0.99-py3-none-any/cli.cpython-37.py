# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/cli.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 7031 bytes
from .std import tqdm, TqdmTypeError, TqdmKeyError
from ._version import __version__
import sys, re, logging
__all__ = [
 'main']

def cast(val, typ):
    log = logging.getLogger(__name__)
    log.debug((val, typ))
    if ' or ' in typ:
        for t in typ.split(' or '):
            try:
                return cast(val, t)
            except TqdmTypeError:
                pass

        raise TqdmTypeError(val + ' : ' + typ)
    if typ == 'bool':
        if val == 'True' or val == '':
            return True
        if val == 'False':
            return False
        raise TqdmTypeError(val + ' : ' + typ)
    try:
        return eval(typ + '("' + val + '")')
    except:
        if typ == 'chr':
            return chr(ord(eval('"' + val + '"')))
        raise TqdmTypeError(val + ' : ' + typ)


def posix_pipe(fin, fout, delim='\n', buf_size=256, callback=lambda int: None):
    """
    Params
    ------
    fin  : file with `read(buf_size : int)` method
    fout  : file with `write` (and optionally `flush`) methods.
    callback  : function(int), e.g.: `tqdm.update`
    """
    fp_write = fout.write
    if not delim:
        while 1:
            tmp = fin.read(buf_size)
            if not tmp:
                getattr(fout, 'flush', lambda : None)()
                return
                fp_write(tmp)
                callback(len(tmp))

    buf = ''
    while 1:
        tmp = fin.read(buf_size)
        if not tmp:
            if buf:
                fp_write(buf)
                callback(1 + buf.count(delim))
            getattr(fout, 'flush', lambda : None)()
            return
            while True:
                try:
                    i = tmp.index(delim)
                except ValueError:
                    buf += tmp
                    break
                else:
                    fp_write(buf + tmp[:i + len(delim)])
                    callback(1)
                    buf = ''
                    tmp = tmp[i + len(delim):]


RE_OPTS = re.compile('\\n {8}(\\S+)\\s{2,}:\\s*([^,]+)')
RE_SHLEX = re.compile('\\s*(?<!\\S)--?([^\\s=]+)(\\s+|=|$)')
UNSUPPORTED_OPTS = ('iterable', 'gui', 'out', 'file')
CLI_EXTRA_DOC = "\n        Extra CLI Options\n        -----------------\n        name  : type, optional\n            TODO: find out why this is needed.\n        delim  : chr, optional\n            Delimiting character [default: '\\n']. Use '\\0' for null.\n            N.B.: on Windows systems, Python converts '\\n' to '\\r\\n'.\n        buf_size  : int, optional\n            String buffer size in bytes [default: 256]\n            used when `delim` is specified.\n        bytes  : bool, optional\n            If true, will count bytes, ignore `delim`, and default\n            `unit_scale` to True, `unit_divisor` to 1024, and `unit` to 'B'.\n        manpath  : str, optional\n            Directory in which to install tqdm man pages.\n        log  : str, optional\n            CRITICAL|FATAL|ERROR|WARN(ING)|[default: 'INFO']|DEBUG|NOTSET.\n"

def main(fp=sys.stderr, argv=None):
    """
    Parameters (internal use only)
    ---------
    fp  : file-like object for tqdm
    argv  : list (default: sys.argv[1:])
    """
    if argv is None:
        argv = sys.argv[1:]
    try:
        log = argv.index('--log')
    except ValueError:
        for i in argv:
            if i.startswith('--log='):
                logLevel = i[len('--log='):]
                break
        else:
            logLevel = 'INFO'

    else:
        logLevel = argv[(log + 1)]
    logging.basicConfig(level=(getattr(logging, logLevel)),
      format='%(levelname)s:%(module)s:%(lineno)d:%(message)s')
    log = logging.getLogger(__name__)
    d = tqdm.__init__.__doc__ + CLI_EXTRA_DOC
    opt_types = dict(RE_OPTS.findall(d))
    for o in UNSUPPORTED_OPTS:
        opt_types.pop(o)

    log.debug(sorted(opt_types.items()))
    split = RE_OPTS.split(d)
    opt_types_desc = zip(split[1::3], split[2::3], split[3::3])
    d = ''.join((('\n  --{0}=<{0}>  : {1}{2}'.format)(*otd) for otd in opt_types_desc if otd[0] not in UNSUPPORTED_OPTS))
    d = 'Usage:\n  tqdm [--help | options]\n\nOptions:\n  -h, --help     Print this help and exit\n  -v, --version  Print version and exit\n\n' + d.strip('\n') + '\n'
    if any((v in argv for v in ('-v', '--version'))):
        sys.stdout.write(__version__ + '\n')
        sys.exit(0)
    else:
        if any((v in argv for v in ('-h', '--help'))):
            sys.stdout.write(d + '\n')
            sys.exit(0)
        argv = RE_SHLEX.split(' '.join(['tqdm'] + argv))
        opts = dict(zip(argv[1::3], argv[3::3]))
        log.debug(opts)
        opts.pop('log', True)
        tqdm_args = {'file': fp}
        try:
            for o, v in opts.items():
                try:
                    tqdm_args[o] = cast(v, opt_types[o])
                except KeyError as e:
                    try:
                        raise TqdmKeyError(str(e))
                    finally:
                        e = None
                        del e

            log.debug('args:' + str(tqdm_args))
        except:
            fp.write('\nError:\nUsage:\n  tqdm [--help | options]\n')
            for i in sys.stdin:
                sys.stdout.write(i)

            raise
        else:
            buf_size = tqdm_args.pop('buf_size', 256)
            delim = tqdm_args.pop('delim', '\n')
            delim_per_char = tqdm_args.pop('bytes', False)
            manpath = tqdm_args.pop('manpath', None)
            stdin = getattr(sys.stdin, 'buffer', sys.stdin)
            stdout = getattr(sys.stdout, 'buffer', sys.stdout)
            if manpath is not None:
                from os import path
                from shutil import copyfile
                from pkg_resources import resource_filename, Requirement
                fi = resource_filename(Requirement.parse('tqdm'), 'tqdm/tqdm.1')
                fo = path.join(manpath, 'tqdm.1')
                copyfile(fi, fo)
                log.info('written:' + fo)
                sys.exit(0)
            elif delim_per_char:
                tqdm_args.setdefault('unit', 'B')
                tqdm_args.setdefault('unit_scale', True)
                tqdm_args.setdefault('unit_divisor', 1024)
                log.debug(tqdm_args)
                with tqdm(**tqdm_args) as (t):
                    posix_pipe(stdin, stdout, '', buf_size, t.update)
            else:
                if delim == '\n':
                    log.debug(tqdm_args)
                    for i in tqdm(stdin, **tqdm_args):
                        stdout.write(i)

                else:
                    log.debug(tqdm_args)
                    with tqdm(**tqdm_args) as (t):
                        posix_pipe(stdin, stdout, delim, buf_size, t.update)