# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.6-intel-2.7/P4.py
# Compiled at: 2017-12-20 11:27:20
from __future__ import print_function
import sys, datetime, re, shutil
from contextlib import contextmanager
import uuid, tempfile, os, os.path, platform, subprocess

class P4Exception(Exception):
    """Exception thrown by P4 in case of Perforce errors or warnings"""

    def __init__(self, value):
        Exception.__init__(self)
        if isinstance(value, (list, tuple)) and len(value) > 2:
            self.value = value[0]
            self.errors = value[1]
            self.warnings = value[2]
        else:
            self.value = value

    def __str__(self):
        return str(self.value)


class Spec(dict):
    """Subclass of dict, representing the fields of a spec definition.
        
        Attributes can be accessed either with the conventional dict format,
        spec['attribute'] or with shorthand spec._attribute.
        
        Instances of this class will preventing any unknown keys.
        """

    def __init__(self, fieldmap=None):
        self.__dict__['_Spec__fields'] = fieldmap

    def permitted_fields(self):
        return self.__fields

    def __setitem__(self, key, value):
        if not isinstance(value, str) and not isinstance(value, list):
            raise P4Exception('Illegal value of type %s, must be string or list' % value.__class__)
        if key in self or self.__fields == None:
            dict.__setitem__(self, key, value)
        elif str(key).lower() in self.__fields:
            dict.__setitem__(self, self.__fields[key.lower()], value)
        else:
            raise P4Exception("Illegal field '%s'" % str(key))
        return

    def __getattr__(self, attr):
        key = str(attr).lower()
        if key[0] != '_':
            raise AttributeError(attr)
        key = key[1:]
        if key in self:
            return self[key]
        if key in self.__fields:
            return self[self.__fields[key]]

    def __setattr__(self, attr, value):
        if attr == 'comment':
            self.__dict__[attr] = value
        else:
            key = str(attr).lower()
            if key[0] != '_':
                raise AttributeError(attr)
            key = key[1:]
            self[key] = value


class Integration():

    def __init__(self, how, file, srev, erev):
        self.how = how
        self.file = file
        self.srev = srev
        self.erev = erev

    def __repr__(self):
        return 'Integration (how = %s file = %s srev = %s erev = %s)' % (
         self.how, self.file, self.srev, self.erev)


class Revision():

    def __init__(self, depotFile):
        self.depotFile = depotFile
        self.integrations = []
        self.rev = None
        self.change = None
        self.action = None
        self.type = None
        self.time = None
        self.user = None
        self.client = None
        self.desc = None
        self.digest = None
        self.fileSize = None
        return

    def integration(self, how, file, srev, erev):
        rec = Integration(how, file, srev, erev)
        self.integrations.append(rec)
        return rec

    def each_integration(self):
        for i in self.integrations:
            yield i

    def __repr__(self):
        return 'Revision (depotFile = %s rev = %s change = %s action = %s type = %s time = %s user = %s client = %s)' % (
         self.depotFile, self.rev, self.change, self.action, self.type, self.time, self.user, self.client)


class DepotFile():

    def __init__(self, name):
        self.depotFile = name
        self.revisions = []

    def new_revision(self):
        r = Revision(self.depotFile)
        self.revisions.append(r)
        return r

    def each_revision(self):
        for r in self.revisions:
            yield r

    def str_revision(self, rev, revFormat, changeFormat):
        result = ("... #{rev:<{rf}} change {change:{cf}} {action:9} on {date}  by {user}@{client} ({type}) '{desc}'").format(rev=rev.rev, rf=revFormat, change=rev.change, cf=changeFormat, action=rev.action, date=rev.time, user=rev.user, client=rev.client, type=rev.type, desc=rev.desc)
        return result

    def str_integration(self, integ):
        result = ('... ... {how} {file}#{srev},{erev}').format(how=integ.how, file=integ.file, srev=integ.srev, erev=integ.erev)
        return result

    def __str__(self):
        result = ('{}').format(self.depotFile)
        revFormat = len(str(self.revisions[0].rev))
        changeFormat = len(str(self.revisions[0].change))
        for rev in self.revisions:
            result += ('\n{}').format(self.str_revision(rev, revFormat, changeFormat))
            for integ in rev.integrations:
                result += ('\n{}').format(self.str_integration(integ))

        return result

    def __repr__(self):
        return 'DepotFile (depotFile = %s, %s revisions)' % (self.depotFile, len(self.revisions))


class Resolver():

    def __init__(self):
        pass

    def resolve(self, mergeInfo):
        if mergeInfo.merge_hint == 'e':
            print('Standard resolver encountered merge conflict, skipping resolve')
            return 's'
        else:
            return mergeInfo.merge_hint

    def actionResolve(self, mergeInfo):
        return mergeInfo.merge_hint


class OutputHandler():
    REPORT = 0
    HANDLED = 1
    CANCEL = 2

    def __init__(self):
        pass

    def outputText(self, s):
        return OutputHandler.REPORT

    def outputBinary(self, b):
        return OutputHandler.REPORT

    def outputStat(self, h):
        return OutputHandler.REPORT

    def outputInfo(self, i):
        return OutputHandler.REPORT

    def outputMessage(self, e):
        return OutputHandler.REPORT


class ReportHandler(OutputHandler):

    def __init__(self):
        OutputHandler.__init__(self)

    def outputText(self, s):
        print('text: ', s)
        return OutputHandler.HANDLED

    def outputBinary(self, b):
        print('binary: ', b)
        return OutputHandler.HANDLED

    def outputStat(self, h):
        print('stat:', h)
        return OutputHandler.HANDLED

    def outputInfo(self, i):
        print('info: ', i)
        return OutputHandler.HANDLED

    def outputMessage(self, e):
        print('error:', e)
        return OutputHandler.HANDLED


class Progress():
    TYPE_SENDFILE = 1
    TYPE_RECEIVEFILE = 2
    TYPE_TRANSFER = 3
    TYPE_COMPUTATION = 4
    UNIT_PERCENT = 1
    UNIT_FILES = 2
    UNIT_KBYTES = 3
    UNIT_MBYTES = 4

    def __init__(self):
        pass

    def init(self, type):
        self.type = type

    def setDescription(self, description, units):
        self.description = description
        self.units = units

    def setTotal(self, total):
        self.total = total

    def update(self, position):
        self.position = position

    def done(self, fail):
        pass


class TextProgress(Progress):
    TYPES = [
     'Unknown', 'Submit', 'Sync', 'Clone']
    UNITS = ['Unknown', 'Percent', 'Files', 'KBytes', 'MBytes']

    def __init__(self):
        Progress.__init__(self)

    def init(self, type):
        Progress.init(self, type)
        print("Progress.init with '%s'" % self.TYPES[type])

    def setDescription(self, description, units):
        Progress.setDescription(self, description, units)
        print("Progress.setDescription with '%s' and units '%s'" % (description, self.UNITS[units]))

    def setTotal(self, total):
        Progress.setTotal(self, total)
        print("Progress.setTotal with '%s' " % total)

    def update(self, position):
        Progress.update(self, position)
        print("Progress.update with '%s'" % position)

    def done(self, fail):
        Progress.done(self, fail)
        print("Progress.done with '%s" % fail)


def processFilelog(h):
    if 'depotFile' in h:
        df = DepotFile(h['depotFile'])
        for n, rev in enumerate(h['rev']):
            r = df.new_revision()
            r.rev = int(rev)
            r.change = int(h['change'][n])
            r.action = h['action'][n]
            r.type = h['type'][n]
            r.time = datetime.datetime.utcfromtimestamp(int(h['time'][n]))
            r.user = h['user'][n]
            r.client = h['client'][n]
            r.desc = h['desc'][n]
            if 'digest' in h and n < len(h['digest']):
                r.digest = h['digest'][n]
            if 'fileSize' in h and n < len(h['fileSize']):
                r.fileSize = h['fileSize'][n]
            if 'how' not in h or n >= len(h['how']) or h['how'][n] == None:
                continue
            else:
                for m, how in enumerate(h['how'][n]):
                    file = h['file'][n][m]
                    srev = h['srev'][n][m].lstrip('#')
                    erev = h['erev'][n][m].lstrip('#')
                    if srev == 'none':
                        srev = 0
                    else:
                        srev = int(srev)
                    if erev == 'none':
                        erev = 0
                    else:
                        erev = int(erev)
                    r.integration(how, file, srev, erev)

        return df
    else:
        raise Exception('Not a filelog object: ' + h)
        return


class FilelogOutputHandler(OutputHandler):

    def __init__(self):
        OutputHandler.__init__(self)

    def outputStat(self, h):
        df = processFilelog(h)
        return self.outputFilelog(df)

    def outputFilelog(self, f):
        return OutputHandler.REPORT


import P4API

class P4(P4API.P4Adapter):
    """Use this class to communicate with a Perforce server
        
        Instances of P4 will use the environment settings (including P4CONFIG)
        to determine the connection parameters such as P4CLIENT and P4PORT.
        
        This attributes can also be set separately before connecting.
        
        To run any Perforce commands, users of this class first need to run
        the connect() method.
        
        It is good practice to disconnect() after the program is complete.
        """
    RAISE_ALL = 2
    RAISE_ERROR = 1
    RAISE_ERRORS = 1
    RAISE_NONE = 0
    EV_NONE = 0
    EV_USAGE = 1
    EV_UNKNOWN = 2
    EV_CONTEXT = 3
    EV_ILLEGAL = 4
    EV_NOTYET = 5
    EV_PROTECT = 6
    EV_EMPTY = 17
    EV_FAULT = 33
    EV_CLIENT = 34
    EV_ADMIN = 35
    EV_CONFIG = 36
    EV_UPGRADE = 37
    EV_COMM = 38
    EV_TOOBIG = 39
    E_EMPTY = 0
    E_INFO = 1
    E_WARN = 2
    E_FAILED = 3
    E_FATAL = 4
    specfields = {'clients': ('client', 'client'), 
       'labels': ('label', 'label'), 
       'branches': ('branch', 'branch'), 
       'changes': ('change', 'change'), 
       'streams': ('stream', 'Stream'), 
       'jobs': ('job', 'Job'), 
       'users': ('user', 'User'), 
       'groups': ('group', 'group'), 
       'depots': ('depot', 'name'), 
       'servers': ('server', 'Name')}

    def __init__(self, *args, **kwlist):
        P4API.P4Adapter.__init__(self, *args, **kwlist)

    def __del__(self):
        if self.debug > 3:
            print('P4.__del__()', file=sys.stderr)

    def __getattr__(self, name):
        if name.startswith('run_'):
            cmd = name[len('run_'):]
            return lambda *args, **kargs: self.run(cmd, *args, **kargs)
        if name.startswith('delete_'):
            cmd = name[len('delete_'):]
            return lambda *args, **kargs: self.run(cmd, '-d', *args, **kargs)
        if name.startswith('fetch_'):
            cmd = name[len('fetch_'):]
            return lambda *args, **kargs: self.__fetch(cmd, *args, **kargs)
        if name.startswith('save_'):
            cmd = name[len('save_'):]
            return lambda *args, **kargs: self.__save(cmd, *args, **kargs)
        if name.startswith('parse_'):
            cmd = name[len('parse_'):]
            return lambda *args, **kargs: self.__parse_spec(cmd, *args, **kargs)
        if name.startswith('format_'):
            cmd = name[len('format_'):]
            return lambda *args, **kargs: self.__format_spec(cmd, *args, **kargs)
        if name.startswith('iterate_'):
            cmd = name[len('iterate_'):]
            return lambda *args, **kargs: self.__iterate(cmd, *args, **kargs)
        raise AttributeError(name)

    def __save(self, cmd, *args, **kargs):
        self.input = args[0]
        return self.run(cmd, '-i', args[1:], **kargs)

    def __parse_spec(self, cmd, *args, **kargs):
        form = args[0]
        comments = ('\n').join([ x for x in form.split('\n') if x.startswith('#') ]) + '\n'
        spec = self.parse_spec(cmd, *args, **kargs)
        spec.__dict__['comment'] = comments
        return spec

    def __format_spec(self, cmd, *args, **kargs):
        spec = args[0]
        form = self.format_spec(cmd, *args, **kargs)
        if 'comment' in spec.__dict__:
            form = spec.__dict__['comment'] + '\n' + form
        return form

    def __fetch(self, cmd, *args, **kargs):
        result = self.run(cmd, '-o', *args, **kargs)
        for r in result:
            if isinstance(r, tuple) or isinstance(r, dict):
                return r

        return result[0]

    def __iterate(self, cmd, *args, **kargs):
        if cmd in self.specfields:
            specs = self.run(cmd, *args, **kargs)
            spec = self.specfields[cmd][0]
            field = self.specfields[cmd][1]
            return (self.run(spec, '-o', x[field])[0] for x in specs)
        raise Exception('Unknown spec list command: %s', cmd)

    def __repr__(self):
        state = 'disconnected'
        if self.connected():
            state = 'connected'
        return 'P4 [%s@%s %s] %s' % (
         self.user, self.client, self.port, state)

    def identify(cls):
        return P4API.identify()

    identify = classmethod(identify)

    def log_messages(self):
        for message in self.messages:
            if message.severity == 3:
                self.logger.error(message)
            elif message.severity == 2:
                self.logger.warning(message)
            elif message.severity == 1:
                self.logger.info(message)

    def run(self, *args, **kargs):
        """Generic run method"""
        context = {}
        resultLogging = True
        if 'resultLogging' in kargs:
            resultLogging = False
            del kargs['resultLogging']
        for k, v in list(kargs.items()):
            context[k] = getattr(self, k)
            setattr(self, k, v)

        flatArgs = self.__flatten(args)
        if hasattr(self, 'encoding') and self.encoding and not self.encoding == 'raw':
            result = []
            for s in flatArgs:
                result.append(s.encode(self.encoding))

            flatArgs = result
        if self.logger:
            self.logger.info('p4 ' + (' ').join(flatArgs))
        try:
            result = P4API.P4Adapter.run(self, *flatArgs)
        except P4Exception as e:
            if self.logger:
                self.log_messages()
            for k, v in list(context.items()):
                setattr(self, k, v)

            raise e

        if self.logger:
            self.log_messages()
        if resultLogging and self.logger:
            self.logger.debug(result)
        for k, v in list(context.items()):
            setattr(self, k, v)

        return result

    def run_submit(self, *args, **kargs):
        """Simplified submit - if any arguments is a dict, assume it to be the changeform"""
        nargs = list(args)
        form = None
        for n, arg in enumerate(nargs):
            if isinstance(arg, dict):
                self.input = arg
                nargs.pop(n)
                nargs.append('-i')
                break

        return self.run('submit', *nargs, **kargs)

    def run_shelve(self, *args, **kargs):
        """Simplified shelve - if any arguments is a dict, assume it to be the changeform"""
        nargs = list(args)
        form = None
        for n, arg in enumerate(nargs):
            if isinstance(arg, dict):
                self.input = arg
                nargs.pop(n)
                nargs.append('-i')
                break

        return self.run('shelve', *nargs, **kargs)

    def delete_shelve(self, *args, **kargs):
        """Simplified deletion of shelves - if no -c is passed in, add it to the args"""
        nargs = list(args)
        if '-c' not in nargs:
            nargs = [
             '-c'] + nargs
        nargs = [
         '-d'] + nargs
        return self.run('shelve', *nargs, **kargs)

    def run_login(self, *args, **kargs):
        """Simple interface to make login easier"""
        if 'password' in kargs:
            password = kargs['password']
            self.input = password
            del kargs['password']
        else:
            self.input = self.password
        return self.run('login', *args, **kargs)

    def run_password(self, oldpass, newpass, *args, **kargs):
        """Simple interface to allow setting of the password"""
        if oldpass and len(oldpass) > 0:
            self.input = [
             oldpass, newpass, newpass]
        else:
            self.input = [
             newpass, newpass]
        try:
            return self.run('password', *args, **kargs)
        except P4Exception as e:
            if self.errors and self.errors[0] == "Passwords don't match.":
                raise P4Exception('Password invalid.')

    def run_filelog(self, *args, **kargs):
        kargs['resultLogging'] = False
        raw = self.run('filelog', args, **kargs)
        if not self.tagged or not raw:
            return raw
        result = []
        for h in raw:
            df = None
            if isinstance(h, dict):
                df = processFilelog(h)
            else:
                df = h
            result.append(df)

        logger = self.logger
        if 'logger' in kargs:
            logger = kargs['logger']
        if logger:
            output = ('\n\n').join([ str(x) for x in result ])
            logger.debug(output)
        return result

    def run_print(self, *args, **kargs):
        kargs['resultLogging'] = False
        raw = self.run('print', args, **kargs)
        logger = self.logger
        if 'logger' in kargs:
            logger = kargs['logger']
        result = []
        if raw:
            debugResult = []
            for line in raw:
                if isinstance(line, dict):
                    result.append(line)
                    if logger:
                        debugResult.append(line)
                    result.append('')
                else:
                    try:
                        result[(-1)] += line
                    except TypeError:
                        if type(line) == bytes and type(result[(-1)]) == str and result[(-1)] == '':
                            result[-1] = line
                        else:
                            raise

            if logger:
                logger.debug(debugResult)
            return result
        return []

    def run_resolve(self, *args, **kargs):
        if self.resolver:
            myResolver = self.resolver
        else:
            myResolver = Resolver()
        if 'resolver' in kargs:
            myResolver = kargs['resolver']
        savedResolver = self.resolver
        self.resolver = myResolver
        result = self.run('resolve', args)
        self.resolver = savedResolver
        return result

    def run_tickets(self, *args):
        fname = self.ticket_file
        with open(fname) as (f):
            tickets_raw = f.readlines()
        pattern = re.compile('([^=]*)=(.*):([^:]*)\n')
        tickets = [ pattern.match(x).groups() for x in tickets_raw ]
        keys = ['Host', 'User', 'Ticket']
        result = [ dict(zip(keys, x)) for x in tickets ]
        return result

    def run_init(self, *args, **kargs):
        raise Exception('Please run P4.init() instead')

    def run_clone(self, *args, **kargs):
        raise Exception('Please run P4.clone) instead')

    def __flatten(self, args):
        result = []
        if isinstance(args, tuple) or isinstance(args, list):
            for i in args:
                result.extend(self.__flatten(i))

        else:
            result.append(args)
        return tuple(result)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected():
            self.disconnect()
        return False

    def connect(self):
        P4API.P4Adapter.connect(self)
        return self

    def is_ignored(self, path):
        return P4API.P4Adapter.is_ignored(self, os.path.abspath(path))

    @contextmanager
    def while_tagged(self, t):
        old = self.tagged
        self.tagged = t
        try:
            yield
        finally:
            self.tagged = old

    @contextmanager
    def at_exception_level(self, e):
        old = self.exception_level
        self.exception_level = e
        try:
            yield
        finally:
            self.exception_level = old

    @contextmanager
    def using_handler(self, c):
        old = self.handler
        self.handler = c
        try:
            yield
        finally:
            self.handler = old

    @contextmanager
    def saved_context(self, **kargs):
        """Saves the context of this p4 object and restores it again at the end of the block"""
        saved_context = {}
        for attr in self.__members__:
            saved_context[attr] = getattr(self, attr)

        for k, v in list(kargs.items()):
            setattr(self, k, v)

        try:
            yield
        finally:
            for k, v in list(saved_context.items()):
                if k not in ('port', 'track'):
                    try:
                        setattr(self, k, v)
                    except AttributeError:
                        pass

    @contextmanager
    def temp_client(self, prefix, template):
        """Creates a temporary workspace with a temporary root. 
            To be used with the "with" statement. Will clean up the temporary root and client
            workspace after the block has finished.
            The prefix is prepended to the workspace name and should be used in conjunction with
            the SpecMap of a spec depot to avoid creating entries there.
        """
        name = ('{prefix}_{id}').format(prefix=prefix, id=str(uuid.uuid1()))
        ws = self.fetch_client('-t', template, name)
        try:
            root = tempfile.mkdtemp(prefix=prefix)
            ws._root = root
            self.save_client(ws)
            oldName = self.client
            self.client = name
            oldCwd = self.cwd
            self.cwd = root
            yield ws
            self.cwd = oldCwd
            self.client = oldName
        finally:
            self.delete_client(name)
            shutil.rmtree(root)


class Map(P4API.P4Map):

    def __init__(self, *args):
        P4API.P4Map.__init__(self, *args)
        if len(args) > 0:
            self.insert(*args)

    LEFT2RIGHT = True
    RIGHT2LEFT = False

    def __str__(self):
        result = ''
        for a in self.as_array():
            result += a + '\n'

        return result

    def is_empty(self):
        """Returns True if this map has no entries yet, otherwise False"""
        return self.count() == 0

    def includes(self, *args):
        return self.translate(*args) != None

    def reverse(self):
        return Map(P4API.P4Map.reverse(self).as_array())

    def insert(self, *args):
        """Insert an argument to the map. The argument can be:
            
            A String,
            Either of the form "[+-]//lhs/... //rhs/..." or "[+-]//lhs/..."
            for label style maps.
            A List:
            This is a list of strings of one of the single string formats
            described above.
            A pair of Strings:
            P4.Map.insert(lhs, rhs)
            """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                P4API.P4Map.insert(self, arg)
            elif isinstance(arg, list):
                for s in arg:
                    P4API.P4Map.insert(self, s)

        else:
            left = args[0].strip()
            right = args[1].strip()
            P4API.P4Map.insert(self, left, right)


def init(*args, **kargs):
    keywords = ('user', 'client', 'directory', 'port', 'casesensitive', 'unicode')
    new_kargs = dict((x, kargs[x]) for x in kargs if x in keywords)
    result = P4API.dvcs_init(*args, **new_kargs)
    return __dvcs_post_process(result, *args, **kargs)


def clone(*args, **kargs):
    keywords = ('user', 'client', 'directory', 'depth', 'verbose', 'port', 'remote',
                'file', 'noarchive', 'progress')
    new_kargs = dict((x, kargs[x]) for x in kargs if x in keywords)
    result = P4API.dvcs_clone(*args, **new_kargs)
    return __dvcs_post_process(result, *args, **kargs)


def __dvcs_post_process(result, *args, **kargs):
    excluded = ('directory', 'unicode', 'casesensitive', 'depth', 'verbose', 'port',
                'remote', 'file', 'noarchive', 'progress')
    new_kargs = dict((x, kargs[x]) for x in kargs if x not in excluded)
    new_kargs['cwd'] = os.getcwd()
    p4 = P4(**new_kargs)
    p4.messages.extend(result)
    return p4


def __run_dvcs(cmd, *args, **kargs):
    __check_paths()
    options = []

    def add_option(options, name, opt):
        if name in kargs:
            options += [opt, kargs[name]]

    add_option(options, 'client', '-c')
    add_option(options, 'directory', '-d')
    add_option(options, 'user', '-u')
    named_args = []
    if 'unicode' in kargs:
        unicode = kargs['unicode']
        del kargs['unicode']
        if unicode:
            named_args.append('-xi')
        else:
            named_args.append('-n')
    if 'casesensitive' in kargs:
        casesensitive = kargs['casesensitive']
        del kargs['casesensitive']
        if casesensitive:
            named_args.append('-C1')
        else:
            named_args.append('-C0')
    arguments = [
     'p4']
    arguments += options
    arguments += [cmd]
    arguments += named_args
    for a in args:
        arguments += a

    p = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout, serr = p.stdout, p.stderr
    results = sout.read()
    errors = serr.read()
    sout.close()
    serr.close()
    if errors:
        if type(errors) == bytes:
            errors = errors.decode('UTF-8')
        errors = errors.strip()
        raise Exception(("Cmd '{}' raised\n{}").format((' ').join(arguments), errors))
    if type(results) == bytes:
        results = results.decode('UTF-8')
    results = results.strip()
    if 'directory' in kargs:
        path = os.path.abspath(kargs['directory'])
        os.chdir(path)
        os.environ['PWD'] = path
    new_kargs = dict((x, kargs[x]) for x in kargs if x not in ('directory', 'unicode',
                                                               'casesensitive'))
    return P4(**new_kargs)


def __check_paths():
    if not __exec_exists('p4'):
        raise Exception('P4 executable not in path')
    if not __exec_exists('p4d'):
        raise Exception('P4D executable not in path')


def __exec_exists(name):
    execName = name
    if platform.system() == 'Windows':
        execName += '.exe'
    for p in os.environ['PATH'].split(os.pathsep):
        pathToFile = os.path.join(p, execName)
        if os.path.exists(pathToFile) and os.access(pathToFile, os.X_OK):
            return __check_version(pathToFile)

    return False


def __check_version(pathToFile):
    p = subprocess.Popen([pathToFile, '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout, serr = p.stdout, p.stderr
    output = sout.read()
    error = serr.read()
    sout.close()
    serr.close()
    if type(output) == bytes:
        output = output.decode('UTF-8')
    chunks = output.split(os.linesep)
    pattern = re.compile('Rev. (?P<Program>.+)/(?P<Platform>.+)/(?P<Release>.+)/(?P<Patch>\\d+) \\((\\d+/\\d+/\\d+)\\).')
    for c in chunks:
        match = pattern.match(c)
        if match:
            version = match.group('Release')
            year = int(version.split('.')[0])
            if year >= 2015:
                return True
            program = match.group('Program')
            raise Exception(('{} must be at least 2015.1, not {}').format(program, version))

    raise Exception(('Unknown P4 output : {}').format(output))


if __name__ == '__main__':
    p4 = P4()
    p4.connect()
    try:
        ret = p4.run(sys.argv[1:])
        for line in ret:
            if isinstance(line, dict):
                print('-----')
                for k in list(line.keys()):
                    print(k, '=', line[k])

            else:
                print(line)

    except:
        for e in p4.errors:
            print(e)