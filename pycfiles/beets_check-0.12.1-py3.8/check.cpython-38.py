# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beetsplug/check.py
# Compiled at: 2020-04-19 05:08:36
# Size of source mod 2**32: 17585 bytes
import re, os, sys
from subprocess import Popen, PIPE, STDOUT, check_call
from hashlib import sha256
from optparse import OptionParser
from concurrent import futures
import beets
from beets import importer, config, logging
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs, colorize, input_yn, UserError
from beets.library import ReadError
from beets.util import cpu_count, displayable_path, syspath
log = logging.getLogger('beets.check')

def set_checksum(item):
    item['checksum'] = compute_checksum(item)
    item.store()


def compute_checksum(item):
    hash = sha256()
    with open(syspath(item.path), 'rb') as (file):
        hash.update(file.read())
    return hash.hexdigest()


def verify_checksum(item):
    if item['checksum'] != compute_checksum(item):
        raise ChecksumError(item.path, 'checksum did not match value in library.')


def verify_integrity(item):
    for checker in IntegrityChecker.allAvailable():
        checker.check(item)


class ChecksumError(ReadError):
    pass


class CheckPlugin(BeetsPlugin):

    def __init__(self):
        super(CheckPlugin, self).__init__()
        self.config.add({'import':True, 
         'write-check':True, 
         'write-update':True, 
         'integrity':True, 
         'convert-update':True, 
         'threads':cpu_count(), 
         'external':{'mp3val':{'cmdline':'mp3val {0}', 
           'formats':'MP3', 
           'error':'^WARNING: .* \\(offset 0x[0-9a-f]+\\): (.*)$', 
           'fix':'mp3val -nb -f {0}'}, 
          'flac':{'cmdline':'flac --test --silent {0}', 
           'formats':'FLAC', 
           'error':'^.*: ERROR,? (.*)$'}, 
          'oggz-validate':{'cmdline':'oggz-validate {0}', 
           'formats':'OGG'}}})
        if self.config['import']:
            self.register_listener('item_imported', self.item_imported)
            self.import_stages = [self.copy_original_checksum]
            self.register_listener('album_imported', self.album_imported)
        if self.config['write-check']:
            self.register_listener('write', self.item_before_write)
        if self.config['write-update']:
            self.register_listener('after_write', self.item_after_write)
        if self.config['convert-update']:
            self.register_listener('after_convert', self.after_convert)
        if self.config['integrity']:
            self.register_listener('import_task_choice', self.verify_import_integrity)

    def commands(self):
        return [CheckCommand(self.config)]

    def album_imported(self, lib, album):
        for item in album.items():
            if not item.get('checksum', None):
                set_checksum(item)

    def item_imported(self, lib, item):
        if not item.get('checksum', None):
            set_checksum(item)

    def item_before_write(self, item, path, **kwargs):
        if path != item.path:
            return
        if item.get('checksum', None):
            verify_checksum(item)

    def item_after_write(self, item, path, **kwargs):
        if path != item.path:
            return
        set_checksum(item)

    def after_convert(self, item, dest, keepnew):
        if keepnew:
            set_checksum(item)

    def copy_original_checksum--- This code section failed: ---

 L. 132         0  LOAD_FAST                'task'
                2  LOAD_METHOD              imported_items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM            80  '80'
                8  FOR_ITER            100  'to 100'
               10  STORE_FAST               'item'

 L. 133        12  LOAD_CONST               None
               14  STORE_FAST               'checksum'

 L. 134        16  LOAD_FAST                'task'
               18  LOAD_ATTR                replaced_items
               20  LOAD_FAST                'item'
               22  BINARY_SUBSCR    
               24  GET_ITER         
             26_0  COME_FROM            70  '70'
               26  FOR_ITER             78  'to 78'
               28  STORE_FAST               'replaced'

 L. 135        30  SETUP_FINALLY        44  'to 44'

 L. 136        32  LOAD_FAST                'replaced'
               34  LOAD_STR                 'checksum'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'checksum'
               40  POP_BLOCK        
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 137        44  DUP_TOP          
               46  LOAD_GLOBAL              KeyError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    66  'to 66'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 138        58  POP_EXCEPT       
               60  JUMP_BACK            26  'to 26'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            50  '50'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            42  '42'

 L. 139        68  LOAD_FAST                'checksum'
               70  POP_JUMP_IF_FALSE    26  'to 26'

 L. 140        72  POP_TOP          
               74  BREAK_LOOP           78  'to 78'
               76  JUMP_BACK            26  'to 26'

 L. 141        78  LOAD_FAST                'checksum'
               80  POP_JUMP_IF_FALSE     8  'to 8'

 L. 142        82  LOAD_FAST                'checksum'
               84  LOAD_FAST                'item'
               86  LOAD_STR                 'checksum'
               88  STORE_SUBSCR     

 L. 143        90  LOAD_FAST                'item'
               92  LOAD_METHOD              store
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          
               98  JUMP_BACK             8  'to 8'

Parse error at or near `POP_EXCEPT' instruction at offset 62

    def verify_import_integrity(self, session, task):
        integrity_errors = []
        if not task.items:
            return
        for item in task.items:
            try:
                verify_integrity(item)
            except IntegrityError as ex:
                try:
                    integrity_errors.append(ex)
                finally:
                    ex = None
                    del ex

        else:
            if integrity_errors:
                log.warning('Warning: failed to verify integrity')
                for error in integrity_errors:
                    log.warning('  {}: {}'.format(displayable_path(item.path), error))
                else:
                    if beets.config['import']['quiet'] or input_yn('Do you want to skip this album (Y/n)'):
                        log.info('Skipping.')
                        task.choice_flag = importer.action.SKIP


class CheckCommand(Subcommand):

    def __init__(self, config):
        self.threads = config['threads'].get(int)
        self.check_integrity = config['integrity'].get(bool)
        parser = OptionParser(usage='%prog [options] [QUERY...]')
        parser.add_option('-e',
          '--external', action='store_true',
          dest='external',
          default=False,
          help='run external tools')
        parser.add_option('-a',
          '--add', action='store_true',
          dest='add',
          default=False,
          help='add checksum for all files that do not already have one')
        parser.add_option('-u',
          '--update', action='store_true',
          dest='update',
          default=False,
          help='compute new checksums and add the to the database')
        parser.add_option('-f',
          '--force', action='store_true',
          dest='force',
          default=False,
          help='force updating the whole library or fixing all files')
        parser.add_option('--export',
          action='store_true',
          dest='export',
          default=False,
          help='print paths and corresponding checksum')
        parser.add_option('-x',
          '--fix', action='store_true',
          dest='fix',
          default=False,
          help='fix errors with external tools')
        parser.add_option('-l',
          '--list-tools', action='store_true',
          dest='list_tools',
          default=False,
          help='list available third-party used to check integrity')
        parser.add_option('-q',
          '--quiet', action='store_true',
          dest='quiet',
          default=False,
          help='only show errors')
        super(CheckCommand, self).__init__(parser=parser,
          name='check',
          help='compute and verify checksums')

    def func(self, lib, options, arguments):
        self.quiet = options.quiet
        self.lib = lib
        arguments = decargs(arguments)
        self.query = arguments
        self.force_update = options.force
        if options.add:
            self.add()
        else:
            if options.update:
                self.update()
            else:
                if options.export:
                    self.export()
                else:
                    if options.fix:
                        self.fix(ask=(not options.force))
                    else:
                        if options.list_tools:
                            self.list_tools()
                        else:
                            self.check(options.external)

    def add(self):
        self.log('Looking for files without checksums...')
        items = [i for i in self.lib.items(self.query) if not i.get('checksum', None)]

        def add(item):
            log.debug('adding checksum for {0}'.format(displayable_path(item.path)))
            set_checksum(item)
            if self.check_integrity:
                try:
                    verify_integrity(item)
                except IntegrityError as ex:
                    try:
                        log.warning('{} {}: {}'.format(colorize('yellow', 'WARNING'), ex.reason, displayable_path(item.path)))
                    finally:
                        ex = None
                        del ex

        self.execute_with_progress(add, items, msg='Adding missing checksums')

    def check(self, external):
        if external:
            if not IntegrityChecker.allAvailable():
                no_checkers_warning = "No integrity checkers found. Run 'beet check --list-tools'"
                raise UserError(no_checkers_warning)
        if external:
            progs = list(map(lambda c: c.name, IntegrityChecker.allAvailable()))
            plural = 's' if len(progs) > 1 else ''
            self.log('Using integrity checker{} {}'.format(plural, ', '.join(progs)))
        else:
            items = list(self.lib.items(self.query))
            failures = [0]

            def check(item):
                try:
                    if external:
                        verify_integrity(item)
                    else:
                        if item.get('checksum', None):
                            verify_checksum(item)
                    log.debug('{}: {}'.format(colorize('green', 'OK'), displayable_path(item.path)))
                except ChecksumError:
                    log.error('{}: {}'.format(colorize('red', 'FAILED'), displayable_path(item.path)))
                    failures[0] += 1
                except IntegrityError as ex:
                    try:
                        log.warning('{} {}: {}'.format(colorize('yellow', 'WARNING'), ex.reason, displayable_path(item.path)))
                        failures[0] += 1
                    finally:
                        ex = None
                        del ex

                except IOError as exc:
                    try:
                        log.error('{} {}'.format(colorize('red', 'ERROR'), exc))
                        failures[0] += 1
                    finally:
                        exc = None
                        del exc

            if external:
                msg = 'Running external tests'
            else:
                msg = 'Verifying checksums'
            self.execute_with_progress(check, items, msg)
            failures = failures[0]
            if external:
                if failures:
                    self.log('Found {} integrity error(s)'.format(failures))
                    sys.exit(15)
                else:
                    self.log('Integrity successfully verified')
            else:
                if failures:
                    self.log('Failed to verify checksum of {} file(s)'.format(failures))
                    sys.exit(15)
                else:
                    self.log('All checksums successfully verified')

    def update(self):
        if not self.query:
            if not self.force_update:
                if not input_yn('Do you want to overwrite all checksums in your database? (y/n)', require=True):
                    return
        items = self.lib.items(self.query)

        def update(item):
            log.debug('updating checksum: {}'.format(displayable_path(item.path)))
            try:
                set_checksum(item)
            except IOError as exc:
                try:
                    log.error('{} {}'.format(colorize('red', 'ERROR'), exc))
                finally:
                    exc = None
                    del exc

        self.execute_with_progress(update, items, msg='Updating checksums')

    def export(self):
        for item in self.lib.items(self.query):
            if item.get('checksum', None):
                print('{} *{}'.format(item.checksum, displayable_path(item.path)))

    def fix(self, ask=True):
        items = list(self.lib.items(self.query))
        failed = []

        def check(item):
            try:
                if 'checksum' in item:
                    verify_checksum(item)
                fixer = IntegrityChecker.fixer(item)
                if fixer:
                    fixer.check(item)
                    log.debug('{}: {}'.format(colorize('green', 'OK'), displayable_path(item.path)))
            except IntegrityError:
                failed.append(item)
            except ChecksumError:
                log.error('{}: {}'.format(colorize('red', 'FAILED checksum'), displayable_path(item.path)))
            except IOError as exc:
                try:
                    log.error('{} {}'.format(colorize('red', 'ERROR'), exc))
                finally:
                    exc = None
                    del exc

        self.execute_with_progress(check, items, msg='Verifying integrity')
        if not failed:
            self.log('No MP3 files to fix')
            return None
        for item in failed:
            log.info(displayable_path(item.path))
        else:
            if ask:
                if not input_yn('Do you want to fix these files? {} (y/n)', require=True):
                    return

            def fix(item):
                fixer = IntegrityChecker.fixer(item)
                if fixer:
                    fixer.fix(item)
                    log.debug('{}: {}'.format(colorize('green', 'FIXED'), displayable_path(item.path)))
                    set_checksum(item)

            self.execute_with_progress(fix, failed, msg='Fixing files')

    def list_tools(self):
        checkers = [(checker.name, checker.available()) for checker in IntegrityChecker.all()]
        prog_length = max(map(lambda c: len(c[0]), checkers)) + 3
        for name, available in checkers:
            msg = name + (prog_length - len(name)) * ' '
            if available:
                msg += colorize('green', 'found')
            else:
                msg += colorize('red', 'not found')
            print(msg)

    def log(self, msg):
        if not self.quiet:
            print(msg)

    def log_progress(self, msg, index, total):
        if not self.quiet:
            return sys.stdout.isatty() or None
        else:
            msg = '{}: {}/{} [{}%]'.format(msg, index, total, index * 100 / total)
            sys.stdout.write(msg + '\r')
            sys.stdout.flush()
            if index == total:
                sys.stdout.write('\n')
            else:
                sys.stdout.write(len(msg) * ' ' + '\r')

    def execute_with_progress(self, func, args, msg=None):
        """Run `func` for each value in the iterator `args` in a thread pool.

        When the function has finished it logs the progress and the `msg`.
        """
        total = len(args)
        finished = 0
        with futures.ThreadPoolExecutor(max_workers=(self.threads)) as (e):
            for _ in e.map(func, args):
                finished += 1
                self.log_progress(msg, finished, total)


class IntegrityError(ReadError):
    pass


class IntegrityChecker(object):

    @classmethod
    def all(cls):
        if hasattr(cls, '_all'):
            return cls._all
        cls._all = []
        for name, tool in config['check']['external'].items():
            cls._all.append(cls(name, tool))
        else:
            return cls._all

    @classmethod
    def allAvailable(cls):
        if not hasattr(cls, '_all_available'):
            cls._all_available = [c for c in cls.all() if c.available()]
        return cls._all_available

    def __init__(self, name, config):
        self.name = name
        self.cmdline = config['cmdline'].get(str)
        if config['formats'].exists():
            self.formats = config['formats'].as_str_seq()
        else:
            self.formats = True
        if config['error'].exists():
            self.error_match = re.compile(config['error'].get(str), re.M)
        else:
            self.error_match = False
        if config['fix'].exists():
            self.fixcmd = config['fix'].get(str)
        else:
            self.fixcmd = False

    def available(self):
        try:
            with open(os.devnull, 'wb') as (devnull):
                check_call([self.cmdline.split(' ')[0], '-v'], stdout=devnull,
                  stderr=devnull)
        except OSError:
            return False
        else:
            return True

    @classmethod
    def fixer(cls, item):
        """Return an `IntegrityChecker` instance that can fix this item.
        """
        for checker in cls.allAvailable():
            if checker.can_fix(item):
                return checker

    def can_check(self, item):
        return self.formats is True or item.format in self.formats

    def check(self, item):
        if not self.can_check(item):
            return
        else:
            process = Popen((self.cmdline.format(self.shellquote(syspath(item.path).decode('utf-8')))),
              shell=True,
              stdin=PIPE,
              stdout=PIPE,
              stderr=STDOUT)
            stdout = process.communicate()[0]
            if self.error_match:
                match = self.error_match.search(stdout.decode('utf-8'))
            else:
                match = False
            if match:
                raise IntegrityError(item.path, match.group(1))
            else:
                if process.returncode:
                    raise IntegrityError(item.path, 'non-zero exit code for {}'.format(self.name))

    def can_fix(self, item):
        return self.can_check(item) and self.fixcmd

    def fix(self, item):
        check_call((self.fixcmd.format(self.shellquote(syspath(item.path).decode('utf-8')))), shell=True,
          stdin=PIPE,
          stdout=PIPE,
          stderr=STDOUT)

    def shellquote(self, s):
        return "'" + s.replace("'", "'\\''") + "'"