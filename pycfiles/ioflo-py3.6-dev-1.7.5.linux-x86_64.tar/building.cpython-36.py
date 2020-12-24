# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/building.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 179701 bytes
"""building.py build frameworks from mission files

"""
from __future__ import division
import time, re, importlib, os
from collections import deque
try:
    from itertools import izip
except ImportError:
    izip = zip

from ..aid.sixing import *
from ..aid.odicting import odict
from .globaling import *
from . import excepting
from . import registering
from . import storing
from . import housing
from . import acting
from . import poking
from . import needing
from . import goaling
from . import doing
from . import traiting
from . import fiating
from . import wanting
from . import completing
from . import tasking
from . import framing
from . import logging
from . import serving
from .. import trim
from ..aid.consoling import getConsole
console = getConsole()
from ..trim import exterior

def Convert2Num(text):
    """converts text to python type in order
       Int, hex, Float, Complex
       ValueError if can't
    """
    try:
        value = int(text, 10)
        return value
    except ValueError as ex:
        pass

    try:
        value = int(text, 16)
        return value
    except ValueError as ex:
        pass

    try:
        value = float(text)
        return value
    except ValueError as ex:
        pass

    try:
        value = complex(text)
        return value
    except ValueError as ex:
        pass

    raise ValueError("Expected Number got '{0}'".format(text))


def Convert2CoordNum(text):
    """converts text to python type in order
       FracDeg, Int, hex, Float, Complex
       ValueError if can't
    """
    dm = REO_LatLonNE.findall(text)
    if dm:
        deg = float(dm[0][0])
        min_ = float(dm[0][1])
        return deg + min_ / 60.0
    dm = REO_LatLonSW.findall(text)
    if dm:
        deg = float(dm[0][0])
        min_ = float(dm[0][1])
        return -(deg + min_ / 60.0)
    try:
        return Convert2Num(text)
    except ValueError:
        raise ValueError("Expected CoordPointNum got '{0}'".format(text))


def Convert2BoolCoordNum(text):
    """converts text to python type in order
       None, Boolean, Int, Float, Complex
       ValueError if can't
    """
    if text.lower() == 'none':
        return
    else:
        if text.lower() in ('true', 'yes'):
            return True
        if text.lower() in ('false', 'no'):
            return False
        try:
            return Convert2CoordNum(text)
        except ValueError:
            raise ValueError("Expected BoolCoordPointNum got '{0}'".format(text))


def Convert2StrBoolCoordNum(text):
    """converts text to python type in order
       Boolean, Int, Float, complex or double quoted string
       ValueError if can't

       Need goal wants unitary type not path or point
    """
    if REO_Quoted.match(text):
        return text.strip('"')
    else:
        if REO_QuotedSingle.match(text):
            return text.strip("'")
        try:
            return Convert2BoolCoordNum(text)
        except ValueError:
            raise ValueError("Expected StrBoolCoordNum got '{0}'".format(text))


def Convert2PointNum(text):
    """
    Converts text to python type in order
       Pxy, Pne,Pfs,Pxyz,Pned,Pfsb, Int, hex, Float, Complex
       ValueError if can't
    """
    match = REO_PointXY.findall(text)
    if match:
        x, y = match[0]
        return Pxy(x=(float(x)), y=(float(y)))
    match = REO_PointNE.findall(text)
    if match:
        n, e = match[0]
        return Pne(n=(float(n)), e=(float(e)))
    match = REO_PointFS.findall(text)
    if match:
        f, s = match[0]
        return Pfs(f=(float(f)), s=(float(s)))
    match = REO_PointXYZ.findall(text)
    if match:
        x, y, z = match[0]
        return Pxyz(x=(float(x)), y=(float(y)), z=(float(z)))
    match = REO_PointNED.findall(text)
    if match:
        n, e, d = match[0]
        return Pned(n=(float(n)), e=(float(e)), d=(float(d)))
    match = REO_PointFSB.findall(text)
    if match:
        f, s, b = match[0]
        return Pfsb(f=(float(f)), s=(float(s)), b=(float(b)))
    try:
        return Convert2Num(text)
    except ValueError:
        raise ValueError("Expected PointNum got '{0}'".format(text))


def Convert2CoordPointNum(text):
    """converts text to python type in order
       FracDeg, Int, hex, Float, Complex
       ValueError if can't
    """
    dm = REO_LatLonNE.findall(text)
    if dm:
        deg = float(dm[0][0])
        min_ = float(dm[0][1])
        return deg + min_ / 60.0
    dm = REO_LatLonSW.findall(text)
    if dm:
        deg = float(dm[0][0])
        min_ = float(dm[0][1])
        return -(deg + min_ / 60.0)
    try:
        return Convert2PointNum(text)
    except ValueError:
        raise ValueError("Expected CoordPointNum got '{0}'".format(text))


def Convert2BoolCoordPointNum(text):
    """converts text to python type in order
       None, Boolean, Int, Float, Complex
       ValueError if can't
    """
    if text.lower() == 'none':
        return
    else:
        if text.lower() in ('true', 'yes'):
            return True
        if text.lower() in ('false', 'no'):
            return False
        try:
            return Convert2CoordPointNum(text)
        except ValueError:
            raise ValueError("Expected BoolCoordPointNum got '{0}'".format(text))


def Convert2PathCoordPointNum(text):
    """converts text to python type in order
       Boolean, Int, Float, Complex
       ValueError if can't
    """
    if REO_PathNode.match(text):
        return text
    try:
        return Convert2CoordPointNum(text)
    except ValueError:
        raise ValueError("Expected PathCoordPointNum got '{0}'".format(text))


def Convert2BoolPathCoordPointNum(text):
    """converts text to python type in order
       Boolean, Int, Float, Complex
       ValueError if can't
    """
    if text.lower() == 'none':
        return
    else:
        if text.lower() in ('true', 'yes'):
            return True
        if text.lower() in ('false', 'no'):
            return False
        try:
            return Convert2PathCoordPointNum(text)
        except ValueError:
            raise ValueError("Expected PathBoolCoordPointNum got '{0}'".format(text))


def Convert2StrBoolPathCoordPointNum(text):
    """converts text to python type in order
       Boolean, Int, Float, complex or double quoted string
       ValueError if can't
    """
    if REO_Quoted.match(text):
        return text.strip('"')
    else:
        if REO_QuotedSingle.match(text):
            return text.strip("'")
        try:
            return Convert2BoolPathCoordPointNum(text)
        except ValueError:
            raise ValueError("Expected StrBoolPathCoordPointNum got '{0}'".format(text))


def StripQuotes(text):
    """
    Returns text with leading and following quotes (singe or double) stripped
    off if any Otherwise return as is
    """
    if REO_Quoted.match(text):
        return text.strip('"')
    else:
        if REO_QuotedSingle.match(text):
            return text.strip("'")
        return text


VerbList = ['load', 'house', 'init',
 'server',
 'logger', 'log', 'loggee',
 'framer', 'first',
 'frame', 'over', 'under', 'next', 'done', 'timeout', 'repeat',
 'native', 'benter', 'enter', 'recur', 'exit', 'precur', 'renter', 'rexit',
 'print', 'put', 'inc', 'copy', 'set',
 'aux', 'rear', 'raze',
 'go', 'let',
 'do',
 'bid', 'ready', 'start', 'stop', 'run', 'abort',
 'use', 'flo', 'give', 'take']
Comparisons = [
 '==', '<', '<=', '>=', '>', '!=']
Connectives = ['to', 'by', 'with', 'from', 'per', 'for', 'cum', 'qua', 'via',
 'as', 'at', 'in', 'of', 'on', 're', 'is',
 'if', 'be', 'into', 'and', 'not', '+-']
Reserved = Connectives + Comparisons
ReservedFrameNames = ['next', 'prev']

class Builder(object):
    __doc__ = '\n\n    '

    def __init__(self, fileName='', mode=None, metas=None, preloads=None, behaviors=None):
        """

        """
        self.fileName = fileName
        self.mode = mode or []
        self.metas = metas or []
        self.preloads = preloads or []
        self.behaviors = behaviors or []
        self.files = []
        self.counts = []
        self.houses = []
        self.currentFile = None
        self.currentCount = 0
        self.currentHuman = ''
        self.currentMode = None
        self.currentHouse = None
        self.currentStore = None
        self.currentLogger = None
        self.currentLog = None
        self.currentFramer = None
        self.currentFrame = None
        self.currentContext = NATIVE

    def tokenize(self, line):
        """
        Parse line and read and parse continuation lines if any and return tokens list.
        """
        saveLines = []
        saveLineViews = []
        while line.endswith('\\\n'):
            line = line.rstrip()
            saveLineViews.append('%04d %s' % (self.currentCount, line))
            saveLines.append(line.rstrip('\\').strip())
            line = self.currentFile.readline()
            self.currentCount += 1

        line = line.rstrip()
        saveLineViews.append('%04d %s' % (self.currentCount, line))
        saveLines.append(line)
        lineView = '\n'.join(saveLineViews)
        line = ' '.join(saveLines)
        console.concise(lineView + '\n')
        line = line.strip()
        chunks = REO_Chunks.findall(line)
        tokens = []
        for chunk in chunks:
            if chunk[0] == '#':
                break
            else:
                tokens.append(chunk)

        return tokens

    def build(self, fileName='', mode=None, metas=None, preloads=None, behaviors=None):
        """
           Allows building from multiple files. Essentially files list is stack of files
           fileName is name of first file. Load commands in any files push (append) file onto files
           until file completed loaded and then popped off

           Each house's store is inited with the meta data in metas
        """
        if fileName:
            self.fileName = fileName
        else:
            if mode:
                self.mode.extend[mode]
            else:
                if metas:
                    self.metas.extend[metas]
                if preloads:
                    self.preloads.extend[preloads]
                if behaviors:
                    self.behaviors.extend[behaviors]
            if self.behaviors:
                for behavior in self.behaviors:
                    mod = importlib.import_module(behavior)

        housing.House.Clear()
        housing.ClearRegistries()
        try:
            try:
                self.fileName = os.path.abspath(self.fileName)
                self.currentFile = open(self.fileName, 'r')
                self.currentCount = 0
                try:
                    while self.currentFile:
                        line = self.currentFile.readline()
                        self.currentCount += 1
                        nextTokens = []
                        while line:
                            if nextTokens:
                                tokens = nextTokens
                                nextTokens = []
                            else:
                                tokens = self.tokenize(line)
                            if not tokens:
                                line = self.currentFile.readline()
                                self.currentCount += 1
                            else:
                                if tokens[0] not in 'load':
                                    while 1:
                                        line = self.currentFile.readline()
                                        self.currentCount += 1
                                        if not line:
                                            break
                                        nextTokens = self.tokenize(line)
                                        if nextTokens:
                                            if nextTokens[0] not in Reserved:
                                                break
                                            if nextTokens:
                                                tokens.extend(nextTokens)
                                                nextTokens = []

                                self.currentHuman = ' '.join(tokens)
                                try:
                                    if not self.dispatch(tokens):
                                        console.terse('Script Parsing stopped at line {0} in file {1}\n'.format(self.currentCount, self.currentFile.name))
                                        console.terse(self.currentHuman + '\n')
                                        return False
                                except excepting.ParseError as ex:
                                    console.terse('\n{0}\n\n'.format(ex))
                                    console.terse('Script line {0} in file {1}\n'.format(self.currentCount, self.currentFile.name))
                                    console.terse(self.currentHuman + '\n')
                                    raise

                                if not nextTokens:
                                    line = self.currentFile.readline()
                                    self.currentCount += 1

                        self.currentFile.close()
                        if self.files:
                            self.currentFile = self.files.pop()
                            self.currentCount = self.counts.pop()
                            console.terse('Resume loading from file {0}.\n'.format(self.currentFile.name))
                        else:
                            self.currentFile = None

                    for house in self.houses:
                        house.orderTaskables()
                        house.resolve()
                        if console._verbosity >= console.Wordage.concise:
                            house.showAllTaskers()
                            for framer in house.framers:
                                framer.showHierarchy()

                            console.concise('\nData Store for {0}\n'.format(house.name))
                            house.store.expose(valued=(console._verbosity >= console.Wordage.terse))

                    return True
                except excepting.ResolveError as ex:
                    console.terse('{0}\n'.format(ex))
                    return False

            except IOError as ex:
                console.terse('Error opening mission file  {0}\n'.format(ex))
                return False

        finally:
            for f in self.files:
                if not f.closed:
                    f.close()

    def dispatch(self, tokens):
        """
        Converts declaration verb into build method name  and calls it
        """
        verb = tokens[0]
        index = 1
        if verb not in VerbList:
            msg = 'ParseError: Building {0}. Unknown verb {1}, index = {2} tokens = {3}'.format(verb, verb, index, tokens)
            raise excepting.ParseError(msg, tokens, index)
        verbMethod = 'build' + verb.capitalize()
        if hasattr(self, verbMethod):
            return getattr(self, verbMethod)(verb, tokens, index)
        else:
            return self.buildGeneric(verb, tokens, index)

    def buildGeneric(self, verb, tokens, index):
        """
        Called when no build method exists for a verb
        """
        msg = 'ParseError: No build method for verb {0}.'.format(verb)
        raise excepting.ParseError(msg, tokens, index)

    def buildLoad(self, command, tokens, index):
        """
           load filepathname
        """
        try:
            name = tokens[index]
            index += 1
            self.files.append(self.currentFile)
            self.counts.append(self.currentCount)
            cwd = os.getcwd()
            os.chdir(os.path.split(self.currentFile.name)[0])
            name = os.path.abspath(os.path.expanduser(name))
            os.chdir(cwd)
            self.currentFile = open(name, 'r')
            self.currentCount = 0
            console.terse('Loading from file {0}.\n'.format(self.currentFile.name))
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildHouse(self, command, tokens, index):
        """Create a new house and make it the current one

           house dreams
        """
        try:
            name = tokens[index]
            index += 1
            self.verifyName(name, command, tokens, index)
            self.currentHouse = housing.House(name=name)
            self.houses.append(self.currentHouse)
            self.currentStore = self.currentHouse.store
            console.terse("   Created House '{0}'. Assigning registries and creating instances ...\n".format(name))
            self.currentHouse.assignRegistries()
            console.profuse('     Clearing current Framer, Frame, Log etc.\n')
            self.currentFramer = None
            self.currentFrame = None
            self.currentLogger = None
            self.currentLog = None
            for name, path, data in self.metas:
                self.currentHouse.metas[name] = self.initPathToData(path, data)

            self.currentHouse.metas['house'] = self.initPathToData('.meta.house', odict(value=(self.currentHouse.name)))
            for path, data in self.preloads:
                self.initPathToData(path, data)

        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        msg = "   Built House '{0}' with meta:\n".format(self.currentHouse.name)
        for name, share in self.currentHouse.metas.items():
            msg += '       {0}: {1!r}\n'.format(name, share)

        console.terse(msg)
        msg = "   Built House '{0}' with preload:\n".format(self.currentHouse.name)
        for path, data in self.preloads:
            share = self.currentHouse.store.fetch(path)
            msg += '       {0}: {1!r}\n'.format(path, share)

        console.terse(msg)
        return True

    def initPathToData(self, path, data):
        """Convenience support function to preload meta data.
           Initialize share given by path with data.
           Assumes self.currentStore is valid
           path is share path string
           data is ordered dict of data
        """
        share = self.currentStore.create(path)
        self.verifyShareFields(share, data.keys(), None, None)
        share.update(data)
        return share

    def buildInit(self, command, tokens, index):
        """Initialize share in current store

           init destination with data
           init indirect from source

           destination:
              absolute
              path

           data:
              direct

           indirect:
              [(value, fields) in] absolute
              [(value, fields) in] path

           source:
              [(value, fields) in] absolute
              [(value, fields) in] path

        """
        if not self.currentStore:
            msg = "ParseError: Building verb '%s'. No current store" % command
            raise excepting.ParseError(msg, tokens, index)
        try:
            destinationFields, index = self.parseFields(tokens, index)
            destinationPath, index = self.parsePath(tokens, index)
            if self.currentStore.fetchShare(destinationPath) is None:
                console.terse('     Warning: Init of non-preexistent share {0} ... creating anyway\n'.format(destinationPath))
            destination = self.currentStore.create(destinationPath)
            connective = tokens[index]
            index += 1
            if connective in ('with', 'to'):
                if connective == 'to':
                    console.terse("Warning: Connective 'to' in 'init' verb depricated. Use 'with' instead.\n")
                if destinationFields:
                    msg = "ParseError: Building verb '%s'. Unexpected fields '%s in' clause " % (
                     command, destinationFields)
                    raise excepting.ParseError(msg, tokens, index)
                data, index = self.parseDirect(tokens, index)
                self.verifyShareFields(destination, data.keys(), tokens, index)
                destination.update(data)
                console.profuse('     Inited share {0} to data = {1}\n'.format(destination.name, data))
            else:
                if connective in ('from', ):
                    sourceFields, index = self.parseFields(tokens, index)
                    sourcePath, index = self.parsePath(tokens, index)
                    source = self.currentStore.fetchShare(sourcePath)
                    if source is None:
                        msg = "ParseError: Building verb '%s'. Nonexistent source share '%s'" % (
                         command, sourcePath)
                        raise excepting.ParseError(msg, tokens, index)
                    sourceFields, destinationFields = self.prepareSrcDstFields(source, sourceFields, destination, destinationFields, tokens, index)
                    data = odict()
                    for sf, df in izip(sourceFields, destinationFields):
                        data[df] = source[sf]

                    destination.update(data)
                    msg = '     Inited share {0} from source {1} with data = {2}\n'.format(destination.name, source.name, data)
                    console.profuse(msg)
                else:
                    msg = "ParseError: Building verb '%s'. Unexpected connective '%s'" % (
                     command, connective)
                    raise excepting.ParseError(msg, tokens, index)
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildServer(self, command, tokens, index):
        """create server tasker in current house
           server has to have name so can  ask stop

           server name [at period] [be scheduled]
           [rx shost:sport] [tx dhost:dport] [in order] [to prefix] [per data]
           [for source]

           scheduled: (active, inactive, slave)

           rx:
              (host:port, :port, host:, host, :)

           tx:
              (host:port, :port, host:, host, :)

           order:
              (front, mid, back)

           prefix
              filepath

           data:
              direct

           source:
              [(value, fields) in] indirect

        """
        if not self.currentHouse:
            msg = "ParseError: Building verb '%s'. No current house" % command
            raise excepting.ParseError(msg, tokens, index)
        elif not self.currentStore:
            msg = "ParseError: Building verb '%s'. No current store" % command
            raise excepting.ParseError(msg, tokens, index)
        else:
            try:
                parms = {}
                init = {}
                name = ''
                connective = None
                period = 0.0
                prefix = './'
                schedule = ACTIVE
                order = MID
                rxa = ''
                txa = ''
                sha = ('', 54321)
                dha = ('localhost', 54321)
                name = tokens[index]
                index += 1
                while index < len(tokens):
                    connective = tokens[index]
                    index += 1
                    if connective == 'at':
                        period = abs(Convert2Num(tokens[index]))
                        index += 1
                    elif connective == 'to':
                        prefix = tokens[index]
                        index += 1
                    elif connective == 'be':
                        option = tokens[index]
                        index += 1
                        if option not in ('active', 'inactive', 'slave'):
                            msg = "ParseError: Building verb '%s'. Bad server scheduled option got %s" % (
                             command, option)
                            raise excepting.ParseError(msg, tokens, index)
                        schedule = ScheduleValues[option]
                    elif connective == 'in':
                        order = tokens[index]
                        index += 1
                        if order not in OrderValues:
                            msg = "ParseError: Building verb '%s'. Bad order option got %s" % (
                             command, order)
                            raise excepting.ParseError(msg, tokens, index)
                        order = OrderValues[order]
                    elif connective == 'rx':
                        rxa = tokens[index]
                        index += 1
                    elif connective == 'tx':
                        txa = tokens[index]
                        index += 1
                    elif connective == 'per':
                        data, index = self.parseDirect(tokens, index)
                        init.update(data)
                    elif connective == 'for':
                        srcFields, index = self.parseFields(tokens, index)
                        srcPath, index = self.parsePath(tokens, index)
                        if self.currentStore.fetchShare(srcPath) is None:
                            console.terse("     Warning: Init 'with' non-existent share {0} ... creating anyway".format(srcPath))
                        src = self.currentStore.create(srcPath)
                        for field in srcFields:
                            init[field] = src[field]

                    else:
                        msg = "ParseError: Building verb '%s'. Bad connective got %s" % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)

            except IndexError:
                msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
                raise excepting.ParseError(msg, tokens, index)

            if index != len(tokens):
                msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
                raise excepting.ParseError(msg, tokens, index)
            prefix += '/' + self.currentHouse.name
            if rxa:
                if ':' in rxa:
                    host, port = rxa.split(':')
                    sha = (host, int(port))
                else:
                    sha = (
                     rxa, sha[1])
            if txa:
                if ':' in txa:
                    host, port = txa.split(':')
                    dha = (host, int(port))
                else:
                    dha = (
                     txa, dha[1])
            server = serving.Server(name=name, store=(self.currentStore))
            kw = dict(period=period, schedule=schedule, sha=sha, dha=dha, prefix=prefix)
            kw.update(init)
            (server.reinit)(**kw)
            self.currentHouse.taskers.append(server)
            if schedule == SLAVE:
                self.currentHouse.slaves.append(server)
            else:
                if order == FRONT:
                    self.currentHouse.fronts.append(server)
                else:
                    if order == BACK:
                        self.currentHouse.backs.append(server)
                    else:
                        self.currentHouse.mids.append(server)
        msg = '     Created server named {0} at period {2:0.4f} be {3}\n'.format(server.name, name, server.period, ScheduleNames[server.schedule])
        console.profuse(msg)
        return True

    def buildLogger(self, command, tokens, index):
        """
        Create logger in current house

        logger logname [to prefix] [at period] [be scheduled]
                       [flush interval]  [keep copies] [cycle term] [size bytes]
        scheduled: (active, inactive, slave)
        period seconds
        interval seconds
        term seconds
        copies integer
        bytes bytes

        logger basic at 0.125
        logger basic

        """
        if not self.currentHouse:
            msg = "ParseError: Building verb '{0}'. No current house.".format(command, index, tokens)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentStore:
                msg = "ParseError: Building verb '{0}'. No current store.".format(command, index, tokens)
                raise excepting.ParseError(msg, tokens, index)
            try:
                name = tokens[index]
                index += 1
                period = 0.0
                schedule = ACTIVE
                order = MID
                interval = 30.0
                prefix = './'
                keep = 0
                term = 3600.0
                size = 1024
                reuse = False
                while index < len(tokens):
                    connective = tokens[index]
                    index += 1
                    if connective == 'at':
                        period = abs(Convert2Num(tokens[index]))
                        index += 1
                    elif connective == 'to':
                        prefix = tokens[index]
                        index += 1
                    elif connective == 'be':
                        option = tokens[index]
                        index += 1
                        if option not in ('active', 'inactive', 'slave'):
                            msg = 'Error building %s. Bad logger scheduled option got %s.' % (
                             command, option)
                            raise excepting.ParseError(msg, tokens, index)
                        schedule = ScheduleValues[option]
                    elif connective == 'in':
                        order = tokens[index]
                        index += 1
                        if order not in OrderValues:
                            msg = 'Error building %s. Bad order got %s.' % (
                             command, order)
                            raise excepting.ParseError(msg, tokens, index)
                        order = OrderValues[order]
                    elif connective == 'flush':
                        interval = max(1.0, abs(Convert2Num(tokens[index])))
                        index += 1
                    elif connective == 'keep':
                        keep = max(0, int(Convert2Num(tokens[index])))
                        index += 1
                    elif connective == 'cycle':
                        term = max(0.0, abs(Convert2Num(tokens[index])))
                        index += 1
                    elif connective == 'size':
                        size = max(0, abs(Convert2Num(tokens[index])))
                        index += 1
                    elif connective == 'reuse':
                        reuse = True
                    else:
                        msg = 'Error building %s. Bad connective got %s.' % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)

                if name in logging.Logger.Names:
                    msg = 'Error building %s. Task %s already exists.' % (
                     command, name)
                    raise excepting.ParseError(msg, tokens, index)
                logger = logging.Logger(name=name, store=(self.currentStore),
                  period=period,
                  flushPeriod=interval,
                  prefix=prefix,
                  keep=keep,
                  cyclePeriod=term,
                  fileSize=size,
                  reuse=reuse)
                logger.schedule = schedule
                self.currentHouse.taskers.append(logger)
                if schedule == SLAVE:
                    self.currentHouse.slaves.append(logger)
                else:
                    if order == FRONT:
                        self.currentHouse.fronts.append(logger)
                    else:
                        if order == BACK:
                            self.currentHouse.backs.append(logger)
                        else:
                            self.currentHouse.mids.append(logger)
                self.currentLogger = logger
                console.profuse('     Created logger named {0} at period {1:0.4f} be {2}\n'.format(logger.name, logger.period, ScheduleNames[logger.schedule]))
            except IndexError:
                msg = 'Error building %s. Not enough tokens.' % (command,)
                raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildLog(self, command, tokens, index):
        """
        Create log in current logger

        log name  [to fileName] [as (text, binary)] [on rule]
        rule: (once, never, always, update, change, streak, deck)
        default fileName is log's name
        default type is text
        default rule  is never

        for manual logging use tout command with rule once or never

        log autopilot text to './logs/' on update
        """
        if not self.currentLogger:
            msg = 'Error building %s. No current logger.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentStore:
                msg = 'Error building %s. No current store.' % (command,)
                raise excepting.ParseError(msg, tokens, index)
            try:
                kind = 'text'
                fileName = ''
                rule = NEVER
                name = tokens[index]
                index += 1
                while index < len(tokens):
                    connective = tokens[index]
                    index += 1
                    if connective == 'as':
                        kind = tokens[index]
                        index += 1
                        if kind not in ('text', 'binary'):
                            msg = 'Error building %s. Bad kind = %s.' % (
                             command, kind)
                            raise excepting.ParseError(msg, tokens, index)
                    elif connective == 'to':
                        fileName = tokens[index]
                        index += 1
                    elif connective == 'on':
                        rule = tokens[index].capitalize()
                        index += 1
                        if rule not in LogRuleValues:
                            msg = 'Error building %s. Bad rule = %s.' % (
                             command, rule)
                            raise excepting.ParseError(msg, tokens, index)
                        rule = LogRuleValues[rule]
                    else:
                        msg = 'Error building %s. Bad connective got %s.' % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)

                if name in logging.Log.Names:
                    msg = 'Error building %s. Log named %s already exists.' % (
                     command, name)
                    raise excepting.ParseError(msg, tokens, index)
                if fileName:
                    for log in self.currentLogger.logs:
                        if fileName == log.baseFilename:
                            msg = 'Error building {0}. Log named {1} file named {2} already exists.'.format(command, name, fileName)
                            raise excepting.ParseError(msg, tokens, index)

                log = logging.Log(name=name, store=(self.currentStore),
                  kind=kind,
                  baseFilename=fileName,
                  rule=rule)
                self.currentLogger.addLog(log)
                self.currentLog = log
                console.profuse('     Created log named {0} kind {1} file {2} rule {3}\n'.format(name, kind, fileName, LogRuleNames[rule]))
            except IndexError:
                msg = 'Error building %s. Not enough tokens.' % (command,)
                raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildLoggee(self, command, tokens, index):
        """
        Add loggee(s) to current log

        Syntax:

        loggee [fields in] path [as tag] [[fields in] path [as tag]] ...

            path: share path
            fields: field list

        If fields not provided use all fields
        If tag not provide use last segment of path as tag

        If log rule is streak then only one loggee per log is allowed and only
        the first field from fields clause is used.

        Syntax:
        log name on streak
          loggee [fields in] path [as tag]

        If log rule is deck then only one loggee per log is allowed and
        fields clause is required.

        Syntax:
        log name on deck
          loggee fields in path [as tag]

        """
        if not self.currentLog:
            msg = 'Error building %s. No current log.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentStore:
                msg = 'Error building %s. No current store.' % (command,)
                raise excepting.ParseError(msg, tokens, index)
            try:
                while index < len(tokens):
                    tag = ''
                    fields, index = self.parseFields(tokens, index)
                    path = tokens[index]
                    index += 1
                    if path in Reserved:
                        msg = "ParseError: Invalid path '{0}' using reserved".format(path)
                        raise excepting.ParseError(msg, tokens, index)
                    if not (REO_DotPath.match(path) or REO_RelPath.match(path)):
                        msg = "ParseError: Invalid path format'{0}'".format(path)
                        raise excepting.ParseError(msg, tokens, index)
                    parts = path.split('.')
                    if 'me' in parts:
                        msg = "ParseError: Invalid path format'{0}', 'me' undefined".format(path)
                        raise excepting.ParseError(msg, tokens, index)
                    if index < len(tokens):
                        connective = tokens[index]
                        if connective == 'as':
                            index += 1
                            tag = tokens[index]
                            if tag in Reserved:
                                msg = "ParseError: Invalid tag '{0}' using reserved".format(tag)
                                raise excepting.ParseError(msg, tokens, index)
                            tag = StripQuotes(tag)
                            index += 1
                    if not tag:
                        tag = parts[(-1)]
                    share = self.currentStore.create(path)
                    if not isinstance(share, storing.Share):
                        msg = 'Error building %s. Loggee path %s not Share.' % (command, path)
                        raise excepting.ParseError(msg, tokens, index)
                    if tag in self.currentLog.loggees:
                        msg = 'Error building %s. Loggee %s already exists in Log %s.' % (
                         command, tag, self.currentLog.name)
                        raise excepting.ParseError(msg, tokens, index)
                    if self.currentLog.rule in (STREAK, DECK):
                        if self.currentLog.loggees:
                            msg = 'Error building {0}. Only one loggee allowed when rule is streak or deck.'.format(command)
                            raise excepting.ParseError(msg, tokens, index)
                    self.currentLog.addLoggee(tag=tag, loggee=share, fields=fields)
                    console.profuse('     Added loggee {0} with tag {1} fields {2}\n'.format(share.name, tag, fields))

            except IndexError:
                msg = 'Error building %s. Not enough tokens.' % (command,)
                raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildFramer(self, command, tokens, index):
        """Create a new framer and make it the current one

           framer framername [be (active, inactive, aux, slave)] [at period]
                                [first frame] [via inode]
           framer framername be active at 0.0
           framer framername
        """
        if not self.currentHouse:
            msg = 'Error building %s. No current house.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentStore:
                msg = 'Error building %s. No current store.' % (command,)
                raise excepting.ParseError(msg, tokens, index)
            try:
                name = tokens[index]
                index += 1
                self.verifyName(name, command, tokens, index)
                schedule = INACTIVE
                order = MID
                period = 0.0
                frame = ''
                inode = ''
                while index < len(tokens):
                    connective = tokens[index]
                    index += 1
                    if connective == 'at':
                        period = max(0.0, Convert2Num(tokens[index]))
                        index += 1
                    elif connective == 'be':
                        option = tokens[index]
                        index += 1
                        if option not in ScheduleValues:
                            msg = 'Error building %s. Bad scheduled option got %s.' % (
                             command, option)
                            raise excepting.ParseError(msg, tokens, index)
                        schedule = ScheduleValues[option]
                    elif connective == 'in':
                        order = tokens[index]
                        index += 1
                        if order not in OrderValues:
                            msg = 'Error building %s. Bad order got %s.' % (
                             command, order)
                            raise excepting.ParseError(msg, tokens, index)
                        order = OrderValues[order]
                    elif connective == 'first':
                        frame = tokens[index]
                        index += 1
                        self.verifyName(frame, command, tokens, index)
                    elif connective == 'via':
                        inode, index = self.parseIndirect(tokens, index, node=True)
                    else:
                        msg = 'Error building %s. Bad connective got %s.' % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)

                if name in framing.Framer.Names:
                    msg = 'Error building %s. Framer or Task %s already exists.' % (
                     command, name)
                    raise excepting.ParseError(msg, tokens, index)
                else:
                    framer = framing.Framer(name=name, store=(self.currentStore),
                      period=period)
                    framer.schedule = schedule
                    framer.first = frame
                    framer.inode = inode
                    self.currentHouse.taskers.append(framer)
                    self.currentHouse.framers.append(framer)
                    if schedule == SLAVE:
                        self.currentHouse.slaves.append(framer)
                    else:
                        if schedule == AUX:
                            self.currentHouse.auxes.append(framer)
                        else:
                            if schedule == MOOT:
                                self.currentHouse.moots.append(framer)
                            else:
                                if order == FRONT:
                                    self.currentHouse.fronts.append(framer)
                                else:
                                    if order == BACK:
                                        self.currentHouse.backs.append(framer)
                                    else:
                                        self.currentHouse.mids.append(framer)
                        self.currentFramer = framer
                        self.currentFramer.assignFrameRegistry()
                        self.currentFrame = None
                        console.profuse("     Created Framer named '{0}' at period {1:0.4f} be {2} first {3}\n".format(framer.name, framer.period, ScheduleNames[framer.schedule], framer.first))
                        console.profuse("     Added Framer '{0}' to House '{1}', Assigned frame registry\n".format(framer.name, self.currentHouse.name))
            except IndexError:
                msg = 'Error building %s. Not enough tokens.' % (command,)
                raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildFirst(self, command, tokens, index):
        """set first (starting) frame for current framer

           first framename
        """
        if not self.currentFramer:
            msg = 'Error building %s. No current framer.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        try:
            name = tokens[index]
            index += 1
            self.verifyName(name, command, tokens, index)
            self.currentFramer.first = name
            console.profuse('     Assigned first frame {0} for framework {1}\n'.format(name, self.currentFramer.name))
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        return True

    def buildFrame(self, command, tokens, index):
        """Create frame and attach to over frame if indicated

           frame framename [in over] [via inode]

           framename cannot be "next" which is reserved

        """
        if not self.currentStore:
            msg = 'Error building %s. No current store.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentFramer:
                msg = 'Error building %s. No current framer.' % (command,)
                raise excepting.ParseError(msg, tokens, index)
            inode = ''
            try:
                name = tokens[index]
                index += 1
                self.verifyName(name, command, tokens, index)
                over = None
                while index < len(tokens):
                    connective = tokens[index]
                    index += 1
                    if connective == 'in':
                        over = tokens[index]
                        index += 1
                    elif connective == 'via':
                        inode, index = self.parseIndirect(tokens, index, node=True)
                    else:
                        msg = 'Error building %s. Bad connective got %s.' % (command, connective)
                        raise excepting.ParseError(msg, tokens, index)

            except IndexError:
                msg = 'Error building %s. Not enough tokens.' % (command,)
                raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        if name in ReservedFrameNames:
            msg = 'Error building %s in Framer %s. Frame name %s reserved.' % (
             command, self.currentFramer.name, name)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if name in framing.Frame.Names:
                msg = 'Error building %s in Framer %s. Frame %s already exists.' % (
                 command, self.currentFramer.name, name)
                raise excepting.ParseError(msg, tokens, index)
            else:
                frame = framing.Frame(name=name, store=(self.currentStore), framer=(self.currentFramer.name),
                  inode=inode)
                if over:
                    frame.over = over
                if self.currentFrame:
                    if not self.currentFrame.next_:
                        self.currentFrame.next_ = frame.name
                if not self.currentFramer.first:
                    self.currentFramer.first = frame.name
                self.currentFrame = frame
                self.currentContext = NATIVE
        console.profuse('     Created frame {0} with over {1}\n'.format(frame.name, over))
        return True

    def buildOver(self, command, tokens, index):
        """Makes frame the over frame of the current frame

           over frame
        """
        self.verifyCurrentContext(tokens, index)
        try:
            over = tokens[index]
            index += 1
            self.verifyName(over, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        self.currentFrame.over = over
        console.profuse('     Assigned over {0} to frame {1}\n'.format(over, self.currentFrame.name))
        return True

    def buildUnder(self, command, tokens, index):
        """Makes frame the primary under frame of the current frame

           under frame
        """
        self.verifyCurrentContext(tokens, index)
        try:
            under = tokens[index]
            index += 1
            self.verifyName(under, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            unders = self.currentFrame.unders
            if not unders:
                unders.append(under)
            elif under != unders[0]:
                while under in unders:
                    unders.remove(under)

                if isinstance(unders[0], framing.Frame):
                    unders.insert(0, under)
                else:
                    unders[0] = under
        console.profuse('     Assigned primary under {0} for frame {1}\n'.format(under, self.currentFrame.name))
        return True

    def buildNext(self, command, tokens, index):
        """Explicitly assign next frame for timeouts and as target of go next

           next frameName
           next

           blank frameName means use lexically next allows override if multiple
           next commands to default of lexical

        """
        self.verifyCurrentContext(tokens, index)
        try:
            if index < len(tokens):
                next_ = tokens[index]
                index += 1
                self.verifyName(next_, command, tokens, index)
            else:
                next_ = None
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        self.currentFrame.next_ = next_
        console.profuse('     Assigned next frame {0} for frame {1}\n'.format(next_, self.currentFrame.name))
        return True

    def buildAux(self, command, tokens, index):
        """Parse 'aux' command  for simple, cloned, or conditional aux of forms

           Simple Auxiliary:
              aux framername

           Cloned Auxiliary:
              aux framername as (mine, clonedauxname) [via (main, mine, inode)]

           Simple Conditional Auxiliary:
              aux framername  if [not] need
              aux framername  if [not] need [and [not] need ...]

           Cloned Conditional Auxiliary:
              aux framername as (mine, clonedauxname) [via inode]
                             if [not] need
              aux framername as (mine, clonedauxname) [via inode]
                             if [not] need [and [not] need ...]

        """
        self.verifyCurrentContext(tokens, index)
        try:
            needs = []
            aux = None
            connective = None
            clone = None
            inode = ''
            insular = False
            aux = tokens[index]
            index += 1
            self.verifyName(aux, command, tokens, index)
            while index < len(tokens):
                connective = tokens[index]
                index += 1
                if connective == 'as':
                    clone = tokens[index]
                    index += 1
                    self.verifyName(clone, command, tokens, index)
                elif connective == 'via':
                    inode, index = self.parseIndirect(tokens, index, node=True)
                elif connective == 'if':
                    while index < len(tokens):
                        act, index = self.makeNeed(tokens, index)
                        if not act:
                            return False
                        needs.append(act)
                        if index < len(tokens):
                            connective = tokens[index]
                            if connective not in ('and', ):
                                msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                                 command, connective)
                                raise excepting.ParseError(msg, tokens, index)
                            index += 1

                else:
                    msg = "Error building {0}. Invalid connective '{1}'.".format(command, connective)
                    raise excepting.ParseError(msg, tokens, index)

        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        else:
            if clone:
                if needs:
                    msg = 'Error building %s. Conditional auxilary may not be clone.' % (command,)
                    raise excepting.ParseError(msg, tokens, index)
            if clone:
                if clone == 'mine':
                    clone = self.currentFramer.newMootTag(base=aux)
                    insular = True
                if clone in self.currentFramer.moots:
                    msg = "Error building {0}. Aux/Clone tag '{1}' already in use.".format(command, clone)
                    raise excepting.ParseError(msg, tokens, index)
                data = odict(original=aux, clone=clone,
                  schedule=AUX,
                  human=(self.currentHuman),
                  count=(self.currentCount),
                  inode=inode,
                  insular=insular)
                self.currentFramer.moots[clone] = data
                aux = odict(tag=clone)
            if needs:
                human = ' '.join(tokens)
                parms = dict(needs=needs, main='me', aux=aux, human=human)
                act = acting.Act(actor='Suspender', registrar=(acting.Actor),
                  parms=parms,
                  human=(self.currentHuman),
                  count=(self.currentCount))
                self.currentFrame.addPreact(act)
                console.profuse("     Added suspender preact,  '{0}', with aux {1} needs:\n".format(command, aux))
                for need in needs:
                    console.profuse('       {0} with parms = {1}\n'.format(need.actor, need.parms))

            else:
                self.currentFrame.addAux(aux)
                console.profuse('     Added aux framer {0}\n'.format(aux))
        return True

    def buildRear(self, command, tokens, index):
        """
        Parse 'rear' verb

        Two Forms: only first form is currently supported

        rear original [as mine] [be aux] in frame framename

                framename cannot be me or in outline of me

        rear original as clonename be schedule

               schedule cannot be aux
               clonename cannot be mine

        """
        self.verifyCurrentContext(tokens, index)
        try:
            original = None
            connective = None
            clone = 'mine'
            schedule = 'aux'
            frame = 'me'
            original = tokens[index]
            index += 1
            self.verifyName(original, command, tokens, index)
            while index < len(tokens):
                connective = tokens[index]
                index += 1
                if connective == 'as':
                    clone = tokens[index]
                    index += 1
                    self.verifyName(clone, command, tokens, index)
                else:
                    if connective == 'be':
                        schedule = tokens[index]
                        index += 1
                    elif connective == 'in':
                        place = tokens[index]
                        index += 1
                        if place != 'frame':
                            msg = "ParseError: Building verb '{0}'. Invalid  '{1}' clause. Expected 'frame' got '{2}'".format(command, connective, place)
                            raise excepting.ParseError(msg, tokens, index)
                    elif index < len(tokens):
                        frame = tokens[index]
                        index += 1
                    else:
                        msg = "Error building {0}. Invalid connective '{1}'.".format(command, connective)
                        raise excepting.ParseError(msg, tokens, index)

        except IndexError:
            msg = 'Error building {0}. Not enough tokens.'.format(command)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building {0}. Unused tokens.'.format(command)
            raise excepting.ParseError(msg, tokens, index)
        if schedule not in ScheduleValues or schedule not in ('aux', ):
            msg = "Error building {0}. Bad scheduled option got '{1}'.".format(command, schedule)
            raise excepting.ParseError(msg, tokens, index)
        schedule = ScheduleValues[schedule]
        if schedule == AUX:
            if clone != 'mine':
                msg = "Error building {0}. Only insular clonename of 'mine' allowed. Got '{1}'.".format(command, clone)
                raise excepting.ParseError(msg, tokens, index)
            if frame == 'me':
                msg = 'Error building {0}. Frame clause required.'.format(command, clone)
                raise excepting.ParseError(msg, tokens, index)
        parms = dict(original=original, clone=clone,
          schedule=schedule,
          frame=frame)
        actorName = 'Rearer'
        if actorName not in acting.Actor.Registry:
            msg = "Error building '{0}'. No actor named '{1}'.".format(command, actorName)
            raise excepting.ParseError(msg, tokens, index)
        act = acting.Act(actor=actorName, registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildRaze(self, command, tokens, index):
        """
        Parse 'raze' verb

        raze (all, last, first) [in frame [(me, framename)]]

        """
        self.verifyCurrentContext(tokens, index)
        try:
            connective = None
            who = None
            frame = 'me'
            who = tokens[index]
            index += 1
            if who not in ('all', 'first', 'last'):
                msg = "ParseError: Building verb '{0}'. Invalid target of raze. Expected one of ['all', 'first', 'last'] but got '{2}'".format(command, connective, who)
                raise excepting.ParseError(msg, tokens, index)
            while index < len(tokens):
                connective = tokens[index]
                index += 1
                if connective == 'in':
                    place = tokens[index]
                    index += 1
                    if place != 'frame':
                        msg = "ParseError: Building verb '{0}'. Invalid  '{1}' clause. Expected 'frame' got '{2}'".format(command, connective, place)
                        raise excepting.ParseError(msg, tokens, index)
                elif index < len(tokens):
                    frame = tokens[index]
                    index += 1
                else:
                    msg = "Error building {0}. Invalid connective '{1}'.".format(command, connective)
                    raise excepting.ParseError(msg, tokens, index)

        except IndexError:
            msg = 'Error building {0}. Not enough tokens.'.format(command)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building {0}. Unused tokens.'.format(command)
            raise excepting.ParseError(msg, tokens, index)
        parms = dict(who=who, frame=frame)
        actorName = 'Razer'
        if actorName not in acting.Actor.Registry:
            msg = "Error building '{0}'. No actor named '{1}'.".format(command, actorName)
            raise excepting.ParseError(msg, tokens, index)
        act = acting.Act(actor=actorName, registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        context = self.currentContext
        if context == NATIVE:
            context = EXIT
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildDone(self, command, tokens, index):
        """
        Creates complete action that indicates tasker(s) completed
        by setting .done state to True

           native context is enter

           done tasker [tasker ...]
           done [me]

           tasker:
              (taskername, me)

        """
        self.verifyCurrentContext(tokens, index)
        try:
            kind = 'Done'
            taskers = []
            while index < len(tokens):
                tasker = tokens[index]
                index += 1
                self.verifyName(tasker, command, tokens, index)
                taskers.append(tasker)

            if not taskers:
                taskers.append('me')
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        actorName = 'Complete' + kind.capitalize()
        if actorName not in completing.Complete.Registry:
            msg = 'Error building complete %s. No actor named %s.' % (
             kind, actorName)
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['taskers'] = taskers
        act = acting.Act(actor=actorName, registrar=(completing.Complete),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse('     Created done complete {0} with {1}\n'.format(act.actor, act.parms))
        return True

    def buildTimeout(self, command, tokens, index):
        """creates implicit transition to next on elapsed >= value

           timeout 5.0
        """
        self.verifyCurrentContext(tokens, index)
        try:
            value = abs(Convert2Num(tokens[index]))
            index += 1
            if isinstance(value, str):
                msg = 'Error building %s. invalid timeout %s.' % (
                 command, value)
                raise excepting.ParseError(msg, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        need = self.makeImplicitDirectFramerNeed(name='elapsed', comparison='>=',
          goal=(float(value)),
          tolerance=0)
        needs = []
        needs.append(need)
        human = ' '.join(tokens)
        far = 'next'
        parms = dict(needs=needs, near='me', far=far, human=human)
        act = acting.Act(actor='Transiter', registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        self.currentFrame.addPreact(act)
        console.profuse("     Added timeout transition preact,  '{0}', with far {1} needs:\n".format(command, far))
        for act in needs:
            console.profuse('       {0} with parms = {1}\n'.format(act.actor, act.parms))

        return True

    def buildRepeat(self, command, tokens, index):
        """creates implicit transition to next on recurred >= value

           repeat 2

           go next if recurred >= 2
        """
        self.verifyCurrentContext(tokens, index)
        try:
            value = abs(Convert2Num(tokens[index]))
            index += 1
            if isinstance(value, str):
                msg = 'Error building %s. invalid repeat %s.' % (
                 command, value)
                raise excepting.ParseError(msg, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        need = self.makeImplicitDirectFramerNeed(name='recurred', comparison='>=',
          goal=(int(value)),
          tolerance=0)
        needs = []
        needs.append(need)
        human = ' '.join(tokens)
        far = 'next'
        parms = dict(needs=needs, near='me', far=far, human=human)
        act = acting.Act(actor='Transiter', registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        self.currentFrame.addPreact(act)
        console.profuse("     Added repeat transition preact,  '{0}', with far {1} needs:\n".format(command, far))
        for act in needs:
            console.profuse('       {0} with parms = {1}\n'.format(act.actor, act.parms))

        return True

    def buildNative(self, command, tokens, index):
        """ sets context for current frame to

           native
        """
        self.currentContext = NATIVE
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildBenter(self, command, tokens, index):
        """ sets context for current frame to

           benter
        """
        self.currentContext = BENTER
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildEnter(self, command, tokens, index):
        """ sets context for current frame to

           enter
        """
        self.currentContext = ENTER
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildRenter(self, command, tokens, index):
        """ sets context for current frame to

           renter
        """
        self.currentContext = RENTER
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildPrecur(self, command, tokens, index):
        """ sets context for current frame to

           precur
        """
        self.currentContext = PRECUR
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildRecur(self, command, tokens, index):
        """ sets context for current frame to

           recur
        """
        self.currentContext = RECUR
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildExit(self, command, tokens, index):
        """ sets context for current frame to

           exit
        """
        self.currentContext = EXIT
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildRexit(self, command, tokens, index):
        """ sets context for current frame to

           rexit
        """
        self.currentContext = REXIT
        console.profuse('     Changed context to {0}\n'.format(ActionContextNames[self.currentContext]))
        return True

    def buildPrint(self, command, tokens, index):
        """prints a string consisting of space separated tokens
           print message

           print hello world

        """
        self.verifyCurrentContext(tokens, index)
        try:
            message = ' '.join(tokens[1:])
        except IndexError:
            message = ''

        parms = dict(message=message)
        act = acting.Act(actor='Printer', registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildPut(self, command, tokens, index):
        """Build put command to put data into share

           put data into destination

           data:
              direct

           destination:
              [(value, fields) in] indirect

        """
        self.verifyCurrentContext(tokens, index)
        try:
            srcData, index = self.parseDirect(tokens, index)
            connective = tokens[index]
            index += 1
            if connective != 'into':
                msg = "ParseError: Building verb '%s'. Unexpected connective '%s'" % (
                 command, connective)
                raise excepting.ParseError(msg, tokens, index)
            dstFields, index = self.parseFields(tokens, index)
            dstPath, index = self.parseIndirect(tokens, index)
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        actorName = 'PokeDirect'
        if actorName not in poking.Poke.Registry:
            msg = "ParseError: Can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['sourceData'] = srcData
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        act = acting.Act(actor=actorName, registrar=(poking.Poke),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: data = {1}  destination = {2} fields = {3} '.format(actorName, srcData, dstPath, dstFields)
        console.profuse(msg)
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildInc(self, command, tokens, index):
        """Build inc command to inc share by data or from source

           inc destination with data
           inc destination from source

           destination:
              [(value, field) in] indirect

           data:
              directone

           source:
              [(value, field) in] indirect

        """
        self.verifyCurrentContext(tokens, index)
        try:
            dstFields, index = self.parseFields(tokens, index)
            dstPath, index = self.parseIndirect(tokens, index)
            connective = tokens[index]
            index += 1
            if connective in ('with', ):
                srcData, index = self.parseDirect(tokens, index)
                for field, value in srcData.items():
                    if isinstance(value, str):
                        msg = "ParseError: Building verb '%s'. " % command
                        msg += "Data value = '%s' in field '%s' not a number" % (
                         value, field)
                        raise excepting.ParseError(msg, tokens, index)

                act = self.makeIncDirect(dstPath, dstFields, srcData)
            else:
                if connective in ('from', ):
                    srcFields, index = self.parseFields(tokens, index)
                    srcPath, index = self.parseIndirect(tokens, index)
                    act = self.makeIncIndirect(dstPath, dstFields, srcPath, srcFields)
                else:
                    msg = "ParseError: Building verb '%s'. Unexpected connective '%s'" % (
                     command, connective)
                    raise excepting.ParseError(msg, tokens, index)
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildCopy(self, command, tokens, index):
        """Build copy command to copy from one share to another

           copy source into destination

           source:
              [(value, fields) in] indirect

           destination:
              [(value, fields) in] indirect

        """
        self.verifyCurrentContext(tokens, index)
        try:
            srcFields, index = self.parseFields(tokens, index)
            srcPath, index = self.parseIndirect(tokens, index)
            connective = tokens[index]
            index += 1
            if connective != 'into':
                msg = "ParseError: Building verb '%s'. Unexpected connective '%s'" % (
                 command, connective)
                raise excepting.ParseError(msg, tokens, index)
            dstFields, index = self.parseFields(tokens, index)
            dstPath, index = self.parseIndirect(tokens, index)
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        actorName = 'PokeIndirect'
        if actorName not in poking.Poke.Registry:
            msg = "ParseError: Can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['source'] = srcPath
        parms['sourceFields'] = srcFields
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        act = acting.Act(actor=actorName, registrar=(poking.Poke),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildSet(self, command, tokens, index):
        """Build set command to generate goal actions

           set goal with data
           set goal from source

           goal:
              elapsed
              recurred
              [(value, fields) in] absolute
              [(value, fields) in] relativegoal

           data:
              direct

           source:
              indirect

        """
        self.verifyCurrentContext(tokens, index)
        try:
            kind = tokens[index]
            if kind in ('elapsed', 'recurred'):
                index += 1
                act, index = self.makeFramerGoal(kind, tokens, index)
            else:
                dstFields, index = self.parseFields(tokens, index)
                dstPath, index = self.parseIndirect(tokens, index)
                connective = tokens[index]
                index += 1
                if connective in ('with', ):
                    srcData, index = self.parseDirect(tokens, index)
                    act = self.makeGoalDirect(dstPath, dstFields, srcData)
                else:
                    if connective in ('from', ):
                        srcFields, index = self.parseFields(tokens, index)
                        srcPath, index = self.parseIndirect(tokens, index)
                        act = self.makeGoalIndirect(dstPath, dstFields, srcPath, srcFields)
                    else:
                        msg = "ParseError: Building verb '%s'. Unexpected connective '%s'" % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)
            if not act:
                return False
        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildGo(self, command, tokens, index):
        """Parse 'go' command  transition  with
           transition conditions of forms

           Transitions:
              go far
              go far if [not] need
              go far if [not] need [and [not] need ...]

           Far:
              next
              me
              frame
        """
        self.verifyCurrentContext(tokens, index)
        try:
            needs = []
            far = None
            connective = None
            far = tokens[index]
            index += 1
            self.verifyName(far, command, tokens, index)
            if index < len(tokens):
                connective = tokens[index]
                if connective not in ('if', ):
                    msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                     command, connective)
                    raise excepting.ParseError(msg, tokens, index)
                index += 1
                while index < len(tokens):
                    act, index = self.makeNeed(tokens, index)
                    if not act:
                        return False
                    needs.append(act)
                    if index < len(tokens):
                        connective = tokens[index]
                        if connective not in ('and', ):
                            msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                             command, connective)
                            raise excepting.ParseError(msg, tokens, index)
                        index += 1

        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        if not needs:
            if connective:
                msg = "ParseError: Building verb '%s'. Connective %s but missing need(s)" % (
                 command, connective)
                raise excepting.ParseError(msg, tokens, index)
        human = ' '.join(tokens)
        parms = dict(needs=needs, near='me', far=far, human=human)
        act = acting.Act(actor='Transiter', registrar=(acting.Actor),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        self.currentFrame.addPreact(act)
        console.profuse("     Added transition preact,  '{0}', with far {1} needs:\n".format(command, far))
        for act in needs:
            console.profuse('       {0} with parms = {1}\n'.format(act.actor, act.parms))

        return True

    def buildLet(self, command, tokens, index):
        """Parse 'let' command  benter action  with entry conditions of forms

           Before Enter:
              let [me] if [not] need
              let [me] if [not] need [and [not] need ...]

           Far:
              next
              me
              frame
        """
        self.verifyCurrentContext(tokens, index)
        try:
            needs = []
            connective = None
            connective = tokens[index]
            if connective not in ('me', 'if'):
                msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                 command, connective)
                raise excepting.ParseError(msg, tokens, index)
            index += 1
            if connective == 'me':
                connective = tokens[index]
                if connective not in ('if', ):
                    msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                     command, connective)
                    raise excepting.ParseError(msg, tokens, index)
                index += 1
            while index < len(tokens):
                act, index = self.makeNeed(tokens, index)
                if not act:
                    return False
                needs.append(act)
                if index < len(tokens):
                    connective = tokens[index]
                    if connective not in ('and', ):
                        msg = "ParseError: Building verb '%s'. Bad connective '%s'" % (
                         command, connective)
                        raise excepting.ParseError(msg, tokens, index)
                    index += 1

        except IndexError:
            msg = "ParseError: Building verb '%s'. Not enough tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = "ParseError: Building verb '%s'. Unused tokens." % (command,)
            raise excepting.ParseError(msg, tokens, index)
        if not needs:
            msg = "ParseError: Building verb '%s'. Missing need(s)" % command
            raise excepting.ParseError(msg, tokens, index)
        for act in needs:
            self.currentFrame.addBeact(act)

        console.profuse("     Added beact,  '{0}', with needs:\n".format(command))
        for act in needs:
            console.profuse('       {0} with {1}\n'.format(act.actor, act.parms))

        return True

    def buildDo(self, command, tokens, index):
        """
        Syntax:

        do kind [part ...] [as name [part ...]] [at context] [via inode]
               [with data]
               [from source]
               [per data]
               [for source]
               [cum data]
               [qua source]

        deed:
            name [part ...]

        kind:
            name [part ...]

        context:
            (native, benter, enter, recur, exit, precur, renter, rexit)

        inode:
            indirect

        data:
            direct

        source:
            [(value, fields) in] indirect

        do controller pid depth   --> controllerPIDDepth
        do arbiter switch heading  --> arbiterSwitchHeading

        do controller pid depth with foobar 1
        do controller pid depth from value in .max.depth

        """
        self.verifyCurrentContext(tokens, index)
        try:
            kind = ''
            name = ''
            inode = None
            parts = []
            parms = odict()
            inits = odict()
            ioinits = odict()
            prerefs = odict([('inits', odict()),
             (
              'ioinits', odict()),
             (
              'parms', odict())])
            connective = None
            context = self.currentContext
            while index < len(tokens):
                if tokens[index] in ('as', 'at', 'via', 'with', 'from', 'per', 'for',
                                     'cum', 'qua'):
                    break
                parts.append(tokens[index])
                index += 1

            if parts:
                kind = ''.join([part.capitalize() for part in parts])
            while index < len(tokens):
                connective = tokens[index]
                index += 1
                if connective in ('as', ):
                    parts = []
                    while index < len(tokens):
                        if tokens[index] in ('as', 'at', 'with', 'fromper', 'for',
                                             'cum', 'qua'):
                            break
                        parts.append(tokens[index])
                        index += 1

                    name = ''.join([part.capitalize() for part in parts])
                    if not name:
                        msg = "ParseError: Building verb '%s'. Missing name for connective 'as'" % command
                        raise excepting.ParseError(msg, tokens, index)
                elif connective in ('at', ):
                    context = tokens[index]
                    index += 1
                    if context not in ActionContextValues:
                        msg = "ParseError: Building verb '{0}'. Invalid context '{1} for connective 'as'".format(command, context)
                        raise excepting.ParseError(msg, tokens, index)
                    context = ActionContextValues[context]
                elif connective in ('via', ):
                    inode, index = self.parseIndirect(tokens, index, node=True)
                elif connective in ('with', ):
                    data, index = self.parseDirect(tokens, index)
                    parms.update(data)
                elif connective in ('from', ):
                    srcFields, index = self.parseFields(tokens, index)
                    srcPath, index = self.parseIndirect(tokens, index)
                    prerefs['parms'][srcPath] = srcFields
                elif connective in ('per', ):
                    data, index = self.parseDirect(tokens, index)
                    ioinits.update(data)
                elif connective in ('for', ):
                    srcFields, index = self.parseFields(tokens, index)
                    srcPath, index = self.parseIndirect(tokens, index)
                    prerefs['ioinits'][srcPath] = srcFields
                elif connective in ('cum', ):
                    data, index = self.parseDirect(tokens, index)
                    inits.update(data)
                elif connective in ('qua', ):
                    srcFields, index = self.parseFields(tokens, index)
                    srcPath, index = self.parseIndirect(tokens, index)
                    prerefs['inits'][srcPath] = srcFields
                else:
                    msg = "Error building {0}. Invalid connective '{1}'.".format(command, connective)
                    raise excepting.ParseError(msg, tokens, index)

        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        if not kind:
            msg = "ParseError: Building verb '%s'. Missing kind for Doer." % command
            raise excepting.ParseError(msg, tokens, index)
        if kind not in doing.Doer.Registry:
            msg = "ParseError: Building verb '%s'. No Deed of kind '%s' in registry" % (
             command, kind)
            raise excepting.ParseError(msg, tokens, index)
        if inode:
            ioinits.update(inode=inode)
        if name:
            inits['name'] = name
        act = acting.Act(actor=kind, registrar=(doing.Doer),
          inits=inits,
          ioinits=ioinits,
          parms=parms,
          prerefs=prerefs,
          human=(self.currentHuman),
          count=(self.currentCount))
        if context == NATIVE:
            context = RECUR
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildBid(self, command, tokens, index):
        """
        bid control tasker [tasker ...] [at period]
        bid control [me] [at period]
        bid control all [at period]

        control:
           (stop, start, run, abort, ready)

        tasker:
           (tasker, me, all)

        period:
            number
            indirectOne

        indirectOne:
            sharepath [of relative]
            (field, value) in sharepath [of relative]

        """
        self.verifyCurrentContext(tokens, index)
        try:
            period = None
            sourcePath = None
            sourceField = None
            parms = odict([('taskers', []), ('period', None), ('sources', odict())])
            control = tokens[index]
            index += 1
            if control not in ('start', 'run', 'stop', 'abort', 'ready'):
                msg = 'Error building {0}. Bad control = {1}.'.format(command, control)
                raise excepting.ParseError(msg, tokens, index)
            taskers = []
            while index < len(tokens):
                if tokens[index] in ('at', ):
                    break
                tasker = tokens[index]
                index += 1
                self.verifyName(tasker, command, tokens, index)
                taskers.append(tasker)

            if not taskers:
                taskers.append('me')
            while index < len(tokens):
                connective = tokens[index]
                index += 1
                if connective in ('at', ):
                    try:
                        period = max(0.0, Convert2Num(tokens[index]))
                        index += 1
                    except ValueError:
                        sourceField, index = self.parseField(tokens, index)
                        sourcePath, index = self.parseIndirect(tokens, index)

                else:
                    msg = "Error building {0}. Invalid connective '{1}'.".format(command, connective)
                    raise excepting.ParseError(msg, tokens, index)

            actorName = 'Want' + control.capitalize()
            if actorName not in wanting.Want.Registry:
                msg = 'Error building  %s. No actor named %s.' % (command, actorName)
                raise excepting.ParseError(msg, tokens, index)
            parms['taskers'] = taskers
            parms['period'] = period
            parms['source'] = sourcePath
            parms['sourceField'] = sourceField
            act = acting.Act(actor=actorName, registrar=(wanting.Want),
              parms=parms,
              human=(self.currentHuman),
              count=(self.currentCount))
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        context = self.currentContext
        if context == NATIVE:
            context = ENTER
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} want '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def buildReady(self, command, tokens, index):
        """
           ready taskName

        """
        self.verifyCurrentContext(tokens, index)
        try:
            tasker = tokens[index]
            index += 1
            self.verifyName(tasker, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        native = BENTER
        self.makeFiat(tasker, 'ready', native, command, tokens, index)
        return True

    def buildStart(self, command, tokens, index):
        """
           start taskName

        """
        self.verifyCurrentContext(tokens, index)
        try:
            tasker = tokens[index]
            index += 1
            self.verifyName(tasker, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        native = ENTER
        self.makeFiat(tasker, 'start', native, command, tokens, index)
        return True

    def buildStop(self, command, tokens, index):
        """
           stop taskName

        """
        self.verifyCurrentContext(tokens, index)
        try:
            tasker = tokens[index]
            index += 1
            self.verifyName(tasker, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        native = EXIT
        self.makeFiat(tasker, 'stop', native, command, tokens, index)
        return True

    def buildRun(self, command, tokens, index):
        """
           run taskName

        """
        self.verifyCurrentContext(tokens, index)
        try:
            tasker = tokens[index]
            index += 1
            self.verifyName(tasker, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        native = RECUR
        self.makeFiat(tasker, 'run', native, command, tokens, index)
        return True

    def buildAbort(self, command, tokens, index):
        """
           abort taskName

        """
        self.verifyCurrentContext(tokens, index)
        try:
            tasker = tokens[index]
            index += 1
            self.verifyName(tasker, command, tokens, index)
        except IndexError:
            msg = 'Error building %s. Not enough tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)

        if index != len(tokens):
            msg = 'Error building %s. Unused tokens.' % (command,)
            raise excepting.ParseError(msg, tokens, index)
        native = ENTER
        self.makeFiat(tasker, 'abort', native, command, tokens, index)
        return True

    def buildUse(self, command, tokens, index):
        """
        Not implemented yet
        """
        msg = ' '.join(tokens)
        console.concise('{0}\n')
        return True

    def buildFlo(self, command, tokens, index):
        """
        Not implemented yet
        """
        msg = ' '.join(tokens)
        console.concise('{0}\n')
        return True

    def buildTake(self, command, tokens, index):
        """
        Not implemented yet
        """
        msg = ' '.join(tokens)
        console.concise('{0}\n')
        return True

    def buildGive(self, command, tokens, index):
        """
        Not implemented yet
        """
        msg = ' '.join(tokens)
        console.concise('{0}\n')
        return True

    def makeIncDirect(self, dstPath, dstFields, srcData):
        """Make IncDirect act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'IncDirect'
        if actorName not in poking.Poke.Registry:
            msg = "ParseError: Can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        parms['sourceData'] = srcData
        act = acting.Act(actor=actorName, registrar=(poking.Poke),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeIncIndirect(self, dstPath, dstFields, srcPath, srcFields):
        """Make IncIndirect act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'IncIndirect'
        if actorName not in poking.Poke.Registry:
            msg = "ParseError: Goal can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        parms['source'] = srcPath
        parms['sourceFields'] = srcFields
        act = acting.Act(actor=actorName, registrar=(poking.Poke),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeFramerGoal(self, name, tokens, index):
        """Goal to set goal name relative to current framer

           method must be wrapped in appropriate try excepts

           goal to data
           goal from source

           goal:
              name

           implied goal is framer.currentframer.goal.name value

           data:
              [value] value
              field value [field value ...]

           source:
              [(value, fields) in] indirect

        """
        dstPath = 'framer.me.goal.' + name
        dstField = 'value'
        dstFields = [dstField]
        connective = tokens[index]
        index += 1
        if connective in ('to', 'with'):
            srcData, index = self.parseDirect(tokens, index)
            act = self.makeGoalDirect(dstPath, dstFields, srcData)
        else:
            if connective in ('by', 'from'):
                srcFields, index = self.parseFields(tokens, index)
                srcPath, index = self.parseIndirect(tokens, index)
                act = self.makeGoalIndirect(dstPath, dstFields, srcPath, srcFields)
            else:
                msg = "ParseError:  Unexpected connective '%s'" % connective
                raise excepting.ParseError(msg, tokens, index)
        return (
         act, index)

    def makeGoalDirect(self, dstPath, dstFields, srcData):
        """Make GoalDirect act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'GoalDirect'
        if actorName not in goaling.Goal.Registry:
            msg = "ParseError: Goal can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        parms['sourceData'] = srcData
        act = acting.Act(actor=actorName, registrar=(goaling.Goal),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeGoalIndirect(self, dstPath, dstFields, srcPath, srcFields):
        """Make GoalIndirect act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'GoalIndirect'
        if actorName not in goaling.Goal.Registry:
            msg = "ParseError: Goal can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['destination'] = dstPath
        parms['destinationFields'] = dstFields
        parms['source'] = srcPath
        parms['sourceFields'] = srcFields
        act = acting.Act(actor=actorName, registrar=(goaling.Goal),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeNeed(self, tokens, index):
        """
        Parse a need

        method must be wrapped in try except indexError
        method assumes already checked for currentStore
        method assumes already checked for currentFramer
        method assumes already checked for currentFrame

        Need forms:

        [not] need

        need:

            basic need:
                if state [comparison goal [+- tolerance]]

            simple need:
                if framerstate [re [(me, framername)]] comparison framergoal [+- tolerance]

                if framerstate re [me] is TBD  # not supported yet

            special need:

                if indirect is updated  [in frame (me, framename)]

                if taskername is (readied, started, running, stopped, aborted)

                if taskername is done

                if (aux auxname, any, all)
                   [in frame [(me, framename)][in framer [(me, framername)]]] is done

                if (aux auxname, any, all)
                   [in framer [(me, framername)]] is done

                if ([aux] auxname, any, all)
                   in frame [(me, framename)][in framer [(me, framername)]] is done

                if ([aux] auxname, any, all)
                   in framer [(me, framername)] is done

        state:
            [(value, field) in] indirect

        goal:
            value
            [(value, field) in] indirect

        indirect:
            path [[of relation] ...]

        comparison:
            (==, !=, <, <=, >=, >)

        tolerance:
            number (the absolute value is used)

        framerstate:
            (elapsed, recurred)

        framergoal:
            goal
            value
            [(value, field) in] indirect

        """
        kind = None
        negate = False
        if tokens[index] == 'not':
            negate = True
            index += 1
        else:
            if 'and' in tokens[index:]:
                back = tokens[index:].index('and') + index + 1
            else:
                back = len(tokens)
        if 'is' in tokens[index:back]:
            place = tokens[index:back].index('is')
            participle = tokens[(index + place + 1)]
            if participle in ('done', ):
                kind = 'done'
                act, index = self.makeDoneNeed(kind, tokens, index)
            else:
                if participle in ('readied', 'started', 'running', 'stopped', 'aborted'):
                    kind = 'status'
                    act, index = self.makeStatusNeed(kind, tokens, index)
                else:
                    if participle in ('updated', 'changed'):
                        kind = participle[:-1]
                        act, index = self.makeMarkerNeed(kind, tokens, index)
                    else:
                        msg = "ParseError: Unexpected 'is' participle '%s' for need" % participle
                        raise excepting.ParseError(msg, tokens, index)
        else:
            state, framer, index = self.parseFramerState(tokens, index)
            if state is not None:
                if state not in ('elapsed', 'recurred'):
                    msg = "ParseError: Unsupported framer state '%s'" % state
                    raise excepting.ParseError(msg, tokens, index)
                kind = state
                act, index = self.makeFramerNeed(kind, tokens, index)
            else:
                simple = False
                stateField, index = self.parseField(tokens, index)
                if stateField is None:
                    state = tokens[index]
                    if state in ('elapsed', 'recurred'):
                        index += 1
                        kind = state
                        simple = True
                        act, index = self.makeFramerNeed(kind, tokens, index)
                if not simple:
                    statePath, index = self.parseIndirect(tokens, index)
                    comparison, index = self.parseComparisonOpt(tokens, index)
                    if not comparison:
                        act = self.makeBoolenNeed(statePath, stateField)
                    else:
                        direct, goal, goalPath, goalField, index = self.parseNeedGoal(statePath, stateField, tokens, index)
                        tolerance, index = self.parseTolerance(tokens, index)
                        if direct:
                            act = self.makeDirectNeed(statePath, stateField, comparison, goal, tolerance)
                        else:
                            act = self.makeIndirectNeed(statePath, stateField, comparison, goalPath, goalField, tolerance)
            if negate:
                act = acting.Nact(actor=(act.actor), registrar=(act.registrar),
                  parms=(act.parms),
                  human=(self.currentHuman),
                  count=(self.currentCount))
            return (act, index)

    def makeDoneNeed(self, kind, tokens, index):
        """
        Need to check if tasker completed by .done truthy
            method must be wrapped in appropriate try excepts

        Syntax:
            if taskername is done

            if (aux auxname, any, all)
                [in frame [(me, framename)][in framer [(me, framername)]]] is done

            if (aux auxname, any, all)
               [in framer [(me, framername)]] is done

            if ([aux] auxname, any, all)
               in frame [(me, framename)][in framer [(me, framername)]] is done

            if ([aux] auxname, any, all)
               in framer [(me, framername)] is done

        """
        frame = ''
        framer = ''
        auxed = False
        tasker = tokens[index]
        if tasker in ('any', 'all'):
            index += 1
            auxed = True
            framer = 'me'
            frame = 'me'
        else:
            if tasker == 'aux':
                index += 1
                auxed = True
                framer = 'me'
                tasker = tokens[index]
                self.verifyName(tasker, kind, tokens, index)
                index += 1
            else:
                self.verifyName(tasker, kind, tokens, index)
                index += 1
        connective = tokens[index]
        if connective == 'in':
            index += 1
            auxed = True
            framer = 'me'
            place = tokens[index]
            index += 1
            if place == 'framer':
                connective = tokens[index]
                if connective not in Reserved:
                    framer = connective
                    self.verifyName(framer, kind, tokens, index)
                    index += 1
                    connective = tokens[index]
            else:
                if place == 'frame':
                    frame = 'me'
                    connective = tokens[index]
                    if connective not in Reserved:
                        frame = connective
                        self.verifyName(frame, kind, tokens, index)
                        index += 1
                        connective = tokens[index]
                    if connective == 'in':
                        index += 1
                        place = tokens[index]
                        index += 1
                        if place != 'framer':
                            msg = "ParseError: Expected 'framer' got '{0}'".format(place)
                            raise excepting.ParseError(msg, tokens, index)
                        connective = tokens[index]
                        if connective not in Reserved:
                            framer = connective
                            self.verifyName(framer, kind, tokens, index)
                            index += 1
                            connective = tokens[index]
                else:
                    msg = "ParseError: Expected 'framer' or frame' got '{0}'".format(place)
                    raise excepting.ParseError(msg, tokens, index)
        if connective not in ('is', ):
            msg = "ParseError: Expected 'is' connective got '{0}'".format(connective)
            raise excepting.ParseError(msg, tokens, index)
        index += 1
        participle = tokens[index]
        index += 1
        if participle not in ('done', ):
            msg = "ParseError: Expected 'done' participle got '{0}'".format(participle)
            raise excepting.ParseError(msg, tokens, index)
        if frame == 'me':
            if not (framer == 'me' or framer == self.currentFramer.name):
                msg = "Error: Frame '{0}' nonsensical given Framer '{1}'.".format(frame, framer)
                raise excepting.ParseError(msg, tokens, index)
        actorName = 'Need' + kind.capitalize()
        if auxed:
            actorName += 'Aux'
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need '%s' can't find actor named '%s'" % (
             kind, actorName)
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['tasker'] = tasker
        parms['framer'] = framer
        parms['frame'] = frame
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        return (
         act, index)

    def makeStatusNeed(self, kind, tokens, index):
        """
        Need to check if tasker named tasker status' is status

        method must be wrapped in appropriate try excepts

        Syntax:
            if taskername is (readied, started, running, stopped, aborted)

        """
        tasker = tokens[index]
        if not REO_IdentPub.match(tasker):
            msg = "ParseError: Invalid format of tasker name '%s'" % tasker
            raise excepting.ParseError(msg, tokens, index)
        index += 1
        connective = tokens[index]
        index += 1
        if connective not in ('is', ):
            msg = "ParseError: Need status invalid connective '%s'" % (
             kind, connective)
            raise excepting.ParseError(msg, tokens, index)
        status = tokens[index]
        index += 1
        if status.capitalize() not in StatusValues:
            msg = "ParseError: Need status invalid status '%s'" % (
             kind, status)
            raise excepting.ParseError(msg, tokens, index)
        status = StatusValues[status.capitalize()]
        actorName = 'Need' + kind.capitalize()
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need '%s' can't find actor named '%s'" % (
             kind, actorName)
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['tasker'] = tasker
        parms['status'] = status
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        return (act, index)

    def makeUpdateNeed(self, kind, tokens, index):
        """
        Need to check if share updated in frame

        method must be wrapped in appropriate try excepts

        Syntax:
            if path [[of relation] ...] is updated [in frame [(me, framename)]]
                    [by marker]

        """
        return self.makeMarkerNeed(kind, tokens, index)

    def makeChangeNeed(self, kind, tokens, index):
        """
        Need to check if share updated in frame

        method must be wrapped in appropriate try excepts

        Syntax:
            if path [[of relation] ...] is changed [in frame [(me, framename)]]
                    [by marker]

        """
        return self.makeMarkerNeed(kind, tokens, index)

    def makeMarkerNeed(self, kind, tokens, index):
        """
        Support method to make either NeedUpdate or NeedChange
            as determined by kind

        Syntax:
            if path [[of relation] ...] is (updated, changed)
                    [in frame [(me, framename)]] [by marker]

            sharepath:
                path [[of relation] ...]

            marker:
                string

        """
        frame = ''
        marker = ''
        sharePath, index = self.parseIndirect(tokens, index)
        connective = tokens[index]
        if connective not in ('is', ):
            msg = "ParseError: Unexpected connective '{0}' not 'is', while building need".format(connective)
            raise excepting.ParseError(msg, tokens, index)
        index += 1
        participle = tokens[index]
        if participle not in ('updated', 'changed'):
            msg = "ParseError: Unexpected 'is' participle '{0}',  not 'updated' or 'changed', while building need".format(participle)
            raise excepting.ParseError(msg, tokens, index)
        index += 1
        if participle[:-1] != kind:
            msg = "ParseError: Mismatching participle. Expected '{0}' got '{1}'".format(kind + 'd', participle)
            raise excepting.ParseError(msg, tokens, index)
        while index < len(tokens):
            connective = tokens[index]
            if connective not in ('in', 'by'):
                break
            index += 1
            if connective == 'in':
                place = tokens[index]
                index += 1
                if place != 'frame':
                    msg = "ParseError: Invalid  '{0}' clause. Expected 'frame' got '{1}'".format(connective, place)
                    raise excepting.ParseError(msg, tokens, index)
                frame = 'me'
                if index < len(tokens):
                    connective = tokens[index]
                    if connective not in Reserved:
                        frame = connective
                        if not REO_IdentPub.match(frame):
                            msg = "ParseError: Invalid format of frame name '%s'" % frame
                            raise excepting.ParseError(msg, tokens, index)
                        index += 1
            elif connective == 'by':
                marker = tokens[index]
                index += 1
                marker = StripQuotes(marker)

        markerKind = 'Marker' + kind.capitalize()
        actorName = 'Need' + kind.capitalize()
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need '%s' can't find actor named '%s'" % (
             kind, actorName)
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['share'] = sharePath
        parms['frame'] = frame
        parms['kind'] = markerKind
        parms['marker'] = marker
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        return (act, index)

    def makeImplicitDirectFramerNeed(self, name, comparison, goal, tolerance):
        """Make implicit need, ie the need is not parsed but implied by the command
           such as timeout

           method must be wrapped in appropriate try excepts

           state comparison goal [+- tolerance]

           goal:
              value (direct number or string)

           state:
              name

           implied state is framer.currentframer.state.name value
        """
        console.profuse('     Making implicit direct framer need {0}\n'.format(name))
        statePath = 'framer.me.state.' + name
        stateField = 'value'
        act = self.makeDirectNeed(statePath, stateField, comparison, goal, tolerance)
        return act

    def makeFramerNeed(self, name, tokens, index):
        """Need that checks if framer state name for current framer satisfies comparison

           method must be wrapped in appropriate try excepts

           state comparison goal [+- tolerance]

           state:
              name

           implied state is framer.currentframer.state.name value

           goal:
              goal
              from path [key]
              value
              dotpath [key]

           elapsed >= 25.0
           elapsed >= goal
           elapsed == goal +- 0.1

        """
        console.profuse('     Making framer need {0}\n'.format(name))
        statePath = 'framer.me.state.' + name
        stateField = 'value'
        comparison, index = self.parseComparisonReq(tokens, index)
        direct, goal, goalPath, goalField, index = self.parseFramerNeedGoal(statePath, stateField, tokens, index)
        tolerance, index = self.parseTolerance(tokens, index)
        if direct:
            act = self.makeDirectNeed(statePath, stateField, comparison, goal, tolerance)
        else:
            act = self.makeIndirectNeed(statePath, stateField, comparison, goalPath, goalField, tolerance)
        return (act, index)

    def makeBoolenNeed(self, statePath, stateField):
        """Make booleanNeed act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'NeedBoolean'
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['state'] = statePath
        parms['stateField'] = stateField
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeDirectNeed(self, statePath, stateField, comparison, goal, tolerance):
        """Make directNeed act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'NeedDirect'
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['state'] = statePath
        parms['stateField'] = stateField
        parms['comparison'] = comparison
        parms['goal'] = goal
        parms['tolerance'] = tolerance
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        return act

    def makeIndirectNeed(self, statePath, stateField, comparison, goalPath, goalField, tolerance):
        """Make indirectNeed act

           method must be wrapped in appropriate try excepts
        """
        actorName = 'NeedIndirect'
        if actorName not in needing.Need.Registry:
            msg = "ParseError: Need can't find actor named '%s'" % actorName
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['state'] = statePath
        parms['stateField'] = stateField
        parms['comparison'] = comparison
        parms['goal'] = goalPath
        parms['goalField'] = goalField
        parms['tolerance'] = tolerance
        msg = '     Created Actor {0} parms: '.format(actorName)
        for key, value in parms.items():
            msg += ' {0} = {1}'.format(key, value)

        console.profuse('{0}\n'.format(msg))
        act = acting.Act(actor=actorName, registrar=(needing.Need),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        return act

    def makeFiat(self, name, kind, native, command, tokens, index):
        """
           Assumes wrapped in currentFrame etc checks

           make a fiat action given the tasker name and fiat kind

        """
        actorName = 'Fiat' + kind.capitalize()
        if actorName not in fiating.Fiat.Registry:
            msg = 'Error building fiat %s. No actor named %s.' % (kind, actorName)
            raise excepting.ParseError(msg, tokens, index)
        parms = {}
        parms['tasker'] = name
        act = acting.Act(actor=actorName, registrar=(fiating.Fiat),
          parms=parms,
          human=(self.currentHuman),
          count=(self.currentCount))
        context = self.currentContext
        if context == NATIVE:
            context = native
        if not self.currentFrame.addByContext(act, context):
            msg = "Error building %s. Bad context '%s'." % (command, context)
            raise excepting.ParseError(msg, tokens, index)
        console.profuse("     Added {0} fiat '{1}' with parms '{2}'\n".format(ActionContextNames[context], act.actor, act.parms))
        return True

    def parseDirect(self, tokens, index):
        """Parse Direct data address
           returns ordered dictionary of fields (keys) and values
           if no field provided then uses default field = 'value'

           parms:
              tokens = list of tokens for command
              index = current index into tokens

           returns:
              data ordered dict
              index

           method must be wrapped in appropriate try excepts

           Syntax:

           data:
              [value] value
              field value [field value ...]

           possible parsing end conditions:
              no more tokens (init,  set)
              token 'into'  (put)

        """
        data = odict()
        if index == len(tokens) - 1:
            value = tokens[index]
            if value in Reserved:
                msg = "ParseError: Encountered reserved '{0}' instead of value." % value
                raise excepting.ParseError(msg, tokens, index)
            index += 1
            field = 'value'
        else:
            field = tokens[index]
            if field in Reserved:
                msg = "ParseError: Encountered reserved '{0}' instead of field." % field
                raise excepting.ParseError(msg, tokens, index)
            index += 1
            value = tokens[index]
            if value in Reserved:
                value = field
                field = 'value'
            else:
                field = StripQuotes(field)
                index += 1
        data[field] = Convert2StrBoolPathCoordPointNum(value)
        while index < len(tokens):
            field = tokens[index]
            if field in Reserved:
                break
            field = StripQuotes(field)
            index += 1
            value = tokens[index]
            if value in Reserved:
                msg = "ParseError: Encountered reserved '{0}' instead of value." % value
                raise excepting.ParseError(msg, tokens, index)
            index += 1
            data[field] = Convert2StrBoolPathCoordPointNum(value)

        if len(data) > 1:
            if 'value' in data:
                msg = "ParseError: Direct data field = 'value' must be only field '%s'" % data.keys
                raise excepting.ParseError(msg, tokens, index)
        for field in data:
            if not REO_IdentPub.match(field):
                msg = "ParseError: Invalid field  = '%s'" % field
                raise excepting.ParseError(msg, tokens, index)

        return (
         data, index)

    def parseFields(self, tokens, index):
        """
        Parse optional field list for Indirect address

        parms:
           tokens = list of tokens for command
           index = current index into tokens

        returns:
           (fields,index)

        method must be wrapped in appropriate try excepts

        Syntax:

        [(value, fields) in] indirect

        fields:
           field [field ...]

        valid fields only when encounter token 'in' after fields
        consumes fields and the 'in' so subsequent parsePath starts with indirect path

        parsing end conditions that signify no fields
        if encounter before 'in':
           no more tokens
           reserved token

        """
        indexSave = index
        fields = []
        found = False
        while index < len(tokens):
            field = tokens[index]
            if field == 'in':
                index += 1
                found = True
                break
            if field in Reserved:
                break
            index += 1
            field = StripQuotes(field)
            fields.append(field)

        if not found:
            index = indexSave
            fields = []
        if len(fields) > 1:
            if 'value' in fields:
                msg = "ParseError: Field = 'value' with multiple fields = '%s'" % fields
                raise excepting.ParseError(msg, tokens, index)
        for i, field in enumerate(fields):
            if not REO_IdentPub.match(field):
                msg = "ParseError: Invalid format of field '%s'" % field
                raise excepting.ParseError(msg, tokens, index)

        return (
         fields, index)

    def parseField(self, tokens, index):
        """
        Parse optional field  for Indirect address

        parms:
           tokens = list of tokens for command
           index = current index into tokens

        returns:
           (field, index)

        method must be wrapped in appropriate try excepts

        Syntax:

        [(value, field) in] indirect

        valid field only when encounter token 'in' after first field
        consumes field and the 'in' so subsequent parsePath starts with indirect path

        parsing end conditions that signify no fields
        if encounter before 'in':
           no more tokens
           reserved token

        """
        indexSave = index
        fields = []
        found = False
        while index < len(tokens):
            field = tokens[index]
            if field == 'in':
                index += 1
                found = True
                break
            if field in Reserved:
                break
            index += 1
            field = StripQuotes(field)
            fields.append(field)

        if not found:
            index = indexSave
            fields = []
        elif len(fields) > 1:
            msg = "ParseError: More than one field = '%s'" % fields
            raise excepting.ParseError(msg, tokens, index)
        else:
            if fields:
                field = fields[0]
                if not REO_IdentPub.match(field):
                    msg = "ParseError: Invalid format of field '%s'" % field
                    raise excepting.ParseError(msg, tokens, index)
            else:
                field = None
        return (
         field, index)

    def parsePath(self, tokens, index):
        """Parse required (path or dotpath) path
           Does not support relative path processing for verbs such as init or
           server which are not inside a framer context
           method must be wrapped in appropriate try excepts
        """
        path = tokens[index]
        index += 1
        if not REO_Path.match(path):
            msg = "ParseError: Invalid path '%s'" % path
            raise excepting.ParseError(msg, tokens, index)
        return (
         path, index)

    def parseIndirect(self, tokens, index, node=False):
        """
        Parse Indirect data address
        If node then allow trailing dot in path

        parms:
           tokens = list of tokens for command
           index = current index into tokens

        returns:
           path
           index

        method must be wrapped in appropriate try excepts

        Syntax:

        indirect:
           absolute
           relative

        absolute:
           dotpath

        relative:
           root
           inode
           framer
           frame
           actor

        root:
           path [of root]

        inode:
           path of me

        framer:
           path of framer [name]

        frame:
           path of frame [name]

        actor:
           path of actor [name]

        """
        if node:
            reoDotPath = REO_DotPathNode
            reoRelPath = REO_RelPathNode
        else:
            reoDotPath = REO_DotPath
            reoRelPath = REO_RelPath
        path = tokens[index]
        index += 1
        if path in Reserved:
            msg = "ParseError: Invalid path '%s' using reserved" % path
            raise excepting.ParseError(msg, tokens, index)
        else:
            if reoDotPath.match(path):
                relation, index = self.parseRelation(tokens, index)
            else:
                if reoRelPath.match(path):
                    relation, index = self.parseRelation(tokens, index)
                    chunks = path.split('.')
                    if relation:
                        if chunks[0] in ('framer', 'frame', 'actor'):
                            if chunks[0] == 'framer' or chunks[0] == 'frame' and '.frame.' in relation or chunks[0] == 'actor' and '.actor.' in relation:
                                msg = "ParseError: Relation conflict in path '{0}' with relation '{1}'".format(path, relation)
                                raise excepting.ParseError(msg, tokens, index)
                            if relation == 'me':
                                msg = "ParseError: Relation conflict in path '{0}' with relation '{1}'".format(path, relation)
                                raise excepting.ParseError(msg, tokens, index)
                    else:
                        if chunks[0] == 'actor':
                            if len(chunks) < 3:
                                msg = "ParseError: Incomplete path '{0}'. Actor name or Share name missing given inline actor relation".format(path)
                                raise excepting.ParseError(msg, tokens, index)
                            relation = 'framer.me.frame.me'
                        else:
                            if chunks[0] == 'frame':
                                if len(chunks) < 3:
                                    msg = "ParseError: Incomplete path '{0}'. Frame name or Share name missing given inline frame relation".format(path)
                                    raise excepting.ParseError(msg, tokens, index)
                                framername = 'me'
                                if chunks[1] == 'main':
                                    framername = 'main'
                                relation = 'framer.' + framername
                    if relation:
                        relation += '.'
                else:
                    msg = "ParseError: Invalid path '{0}'".format(path)
                    raise excepting.ParseError(msg, tokens, index)
        path = relation + path
        return (
         path, index)

    def parseRelation(self, tokens, index, framername=''):
        """
        Parse optional relation clause of relative data address

        parms:
            tokens = list of tokens for command
            index = current index into tokens
            framername = default framer name if not provided such as 'main'

        returns:
            relation
            index

        method must be wrapped in appropriate try excepts

        Syntax:

        relative:
            root
            inode
            framer
            frame
            actor

        root:
            path [of root]

        inode:
            path of me

        framer:
            path of framer [(me, main, name)]

        frame:
            path of frame [(me, main, name)]

        actor:
            path of actor [(me, name)]

        """
        relation = ''
        if index < len(tokens):
            connective = tokens[index]
            if connective == 'of':
                index += 1
                relation = tokens[index]
                index += 1
                if relation not in ('root', 'me', 'framer', 'frame', 'actor'):
                    msg = "ParseError: Invalid relation '%s'" % relation
                    raise excepting.ParseError(msg, tokens, index)
                if relation == 'root':
                    relation = ''
                elif relation == 'me':
                    pass
            if relation in ('framer', ):
                name = ''
                if index < len(tokens):
                    name = tokens[index]
                    if name not in Reserved:
                        index += 1
                        if not REO_IdentPub.match(name):
                            msg = "ParseError: Invalid relation %s name '%s'" % (
                             relation, name)
                            raise excepting.ParseError(msg, tokens, index)
                    else:
                        name = ''
                if not name:
                    name = framername or 'me'
                relation += '.' + name
            if relation in ('frame', ):
                name = ''
                if index < len(tokens):
                    name = tokens[index]
                    if name not in Reserved:
                        index += 1
                        if not REO_IdentPub.match(name):
                            msg = "ParseError: Invalid relation %s name '%s'" % (
                             relation, name)
                            raise excepting.ParseError(msg, tokens, index)
                    else:
                        name = ''
                if not name:
                    name = 'me'
                relation += '.' + name
                framername = ''
                if name == 'main':
                    framername = 'main'
                framerRelation, index = self.parseRelation(tokens, index,
                  framername=framername)
                if framerRelation:
                    if '.frame.' in framerRelation or '.actor.' in framerRelation:
                        msg = "ParseError: Invalid relation '%s' following frame relation" % framerRelation
                        raise excepting.ParseError(msg, tokens, index)
                if framerRelation:
                    relation = framerRelation + '.' + relation
                else:
                    framername = framername or 'me'
                    relation = 'framer.' + framername + '.' + relation
            if relation in ('actor', ):
                name = ''
                if index < len(tokens):
                    name = tokens[index]
                    if name not in Reserved:
                        index += 1
                        if not REO_IdentPub.match(name):
                            msg = "ParseError: Invalid relation %s name '%s'" % (
                             relation, name)
                            raise excepting.ParseError(msg, tokens, index)
                    else:
                        name = ''
                if not name:
                    name = 'me'
                relation += '.' + name
                frameRelation, index = self.parseRelation(tokens, index)
                if frameRelation:
                    if '.actor.' in frameRelation:
                        msg = "ParseError: Invalid relation '%s' following actor relation" % frameRelation
                        raise excepting.ParseError(msg, tokens, index)
                if frameRelation:
                    relation = frameRelation + '.' + relation
                else:
                    relation = 'framer.me.frame.me.' + relation
        return (
         relation, index)

    def parseComparisonOpt(self, tokens, index):
        """Parse a optional comparison

           method must be wrapped in appropriate try excepts
        """
        comparison = None
        if index < len(tokens):
            comparison = tokens[index]
            if comparison in Comparisons:
                index += 1
            else:
                comparison = None
        return (
         comparison, index)

    def parseComparisonReq(self, tokens, index):
        """Parse a required comparison

           method must be wrapped in appropriate try excepts
        """
        comparison = tokens[index]
        index += 1
        if comparison not in Comparisons:
            msg = "ParseError: Need has invalid comparison '%s'" % comparison
            raise excepting.ParseError(msg, tokens, index)
        return (comparison, index)

    def parseFramerState(self, tokens, index):
        """Parse framer state expression

           parms:
              tokens = list of tokens for command
              index = current index into tokens

           returns:
              (state, framer, index)

           method must be wrapped in appropriate try excepts

           Syntax:

           state re [(me, framername)]

           valid state only when encounter token 're' after first state

           parsing end conditions that signify no state
           if encounter before 're':
              no more tokens
              reserved token
              multiple states

        """
        indexSave = index
        states = []
        found = False
        framer = None
        while index < len(tokens):
            connective = tokens[index]
            if connective == 're':
                index += 1
                found = True
                break
            if connective in Reserved:
                break
            index += 1
            state = StripQuotes(connective)
            states.append(state)

        if not found:
            index = indexSave
            states = []
        elif len(states) > 1:
            msg = "ParseError: More than one state = '%s'" % states
            raise excepting.ParseError(msg, tokens, index)
        else:
            if states:
                state = states[0]
                if not REO_IdentPub.match(state):
                    msg = "ParseError: Invalid format of state '%s'" % state
                    raise excepting.ParseError(msg, tokens, index)
            else:
                state = None
        if state is not None:
            framer = 'me'
            while index < len(tokens):
                connective = tokens[index]
                if connective in Reserved:
                    break
                framer = connective
                if not REO_IdentPub.match(framer):
                    msg = "ParseError: Invalid format of framer name '%s'" % framer
                    raise excepting.ParseError(msg, tokens, index)
                if framer != 'me':
                    if framer != self.currentFramer.name:
                        msg = "ParseError: Framer name '%s' for state need not current framer" % framer
                        raise excepting.ParseError(msg, tokens, index)
                index += 1

        return (
         state, framer, index)

    def parseNeedState(self, tokens, index):
        """Parse required need state

           method must be wrapped in appropriate try excepts
        """
        stateField, index = self.parseField(tokens, index)
        statePath, index = self.parseIndirect(tokens, index)
        return (statePath, stateField, index)

    def parseNeedGoal(self, statePath, stateField, tokens, index):
        """Parse required goal

           method must be wrapped in appropriate try excepts
        """
        goalPath = None
        goalField = None
        direct = False
        goal = tokens[index]
        try:
            goal = Convert2StrBoolCoordNum(tokens[index])
            index += 1
            direct = True
        except ValueError:
            goalField, index = self.parseField(tokens, index)
            goalPath, index = self.parseIndirect(tokens, index)

        return (direct, goal, goalPath, goalField, index)

    def parseFramerNeedGoal(self, statePath, stateField, tokens, index):
        """
        Parse required goal for special framer need such as
           elapsed or recurred

        method must be wrapped in appropriate try excepts
        """
        goalPath = None
        goalField = None
        direct = False
        goal = tokens[index]
        try:
            goal = Convert2StrBoolCoordNum(tokens[index])
            index += 1
            direct = True
        except ValueError:
            if goal == 'goal':
                index += 1
                chunks = statePath.strip('.').split('.')
                try:
                    if chunks[0] == 'framer':
                        if chunks[2] == 'state':
                            chunks[2] = 'goal'
                    else:
                        msg = "ParseError: Goal = 'goal' without framer state path '%s'" % statePath
                        raise excepting.ParseError(msg, tokens, index)
                except IndexError:
                    msg = "ParseError: Goal = 'goal' without framer state path '%s'" % statePath
                    raise excepting.ParseError(msg, tokens, index)

                goalPath = '.'.join(chunks)
                goalField = stateField
            else:
                goalField, index = self.parseField(tokens, index)
                goalPath, index = self.parseIndirect(tokens, index)

        return (
         direct, goal, goalPath, goalField, index)

    def parseTolerance(self, tokens, index):
        """Parse a optional tolerance

           method must be wrapped in appropriate try excepts
        """
        tolerance = 0
        if index < len(tokens):
            connective = tokens[index]
            if connective == '+-':
                index += 1
                tolerance = tokens[index]
                index += 1
                tolerance = Convert2Num(tolerance)
                if isinstance(tolerance, str):
                    msg = "ParseError: Need has invalid tolerance '%s'" % tolerance
                    raise excepting.ParseError(msg, tokens, index)
        return (
         tolerance, index)

    def prepareSrcDstFields(self, src, srcFields, dst, dstFields, tokens, index):
        """
        Prepares and verifys a transfer of data
            from sourceFields in source
            to dstFields in dst
        Handles default conditions when fields are empty
            src and dst are shares
            fields are lists

        Ensure Actor._prepareSrcDstFields is the same
        """
        if not srcFields:
            if src:
                if 'value' in src:
                    srcFields = [
                     'value']
                else:
                    if dstFields:
                        srcFields = dstFields
                    else:
                        srcFields = src.keys()
            else:
                srcFields = ['value']
        else:
            self.verifyShareFields(src, srcFields, tokens, index)
            if not dstFields:
                if 'value' in dst:
                    dstFields = [
                     'value']
                else:
                    dstFields = srcFields
            self.verifyShareFields(dst, dstFields, tokens, index)
            if len(srcFields) != len(dstFields):
                msg = 'ParseError: Unequal number of source %s and destination %s fields' % (
                 srcFields, dstFields)
                raise excepting.ParseError(msg, tokens, index)
        for dstField, srcField in izip(dstFields, srcFields):
            if dstField != srcField and srcField != 'value':
                console.profuse("     Warning: Field names mismatch. '{0}' in {1} from '{2}' in {3}  ... creating anyway".format(dstField, dst.name, srcField, src.name))

        for field in srcFields:
            if field not in src:
                console.profuse("     Warning: Transfer from non-existent field '{0}' in share {1} ... creating anyway".format(field, src.name))
                src[field] = None

        for field in dstFields:
            if field not in dst:
                console.profuse("     Warning: Transfer into non-existent field '{0}' in share {1} ... creating anyway\n".format(field, dst.name))
                dst[field] = None

        return (
         srcFields, dstFields)

    def prepareDataDstFields(self, data, dataFields, dst, dstFields, tokens, index):
        """
        Prepares and verifys a transfer of data
            from dataFields in data
            to dstFields in dst
        Handles default conditions when fields are empty
            data is dict
            dst is share
            fields are lists

        Ensure Actor._prepareDstFields is similar
        """
        if not dstFields:
            if 'value' in dst:
                dstFields = [
                 'value']
            else:
                dstFields = dataFields
        self.verifyShareFields(dst, dstFields, tokens, index)
        if len(dataFields) != len(dstFields):
            msg = 'ParseError: Unequal number of source %s and destination %s fields' % (
             dataFields, dstFields)
            raise excepting.ParseError(msg, tokens, index)
        for dstField, dataField in izip(dstFields, dataFields):
            if dstField != dataField and dataField != 'value':
                console.profuse("     Warning: Field names mismatch. '{0}' in {1} from '{2}' ... creating anyway".format(dstField, dst.name, dataField))

        for field in dstFields:
            if field not in dst:
                console.profuse("     Warning: Transfer into non-existent field '{0}' in share {1} ... creating anyway\n".format(field, dst.name))
                dst[field] = None

        return (
         dataFields, dstFields)

    def verifyShareFields(self, share, fields, tokens, index):
        """
        Verify that updating fields in share won't violate the
           condition that when a share has field == 'value'
           it will be the only field

           fields is list of field names
           share is  share

        raises exception if condition would be violated

        Ensure Actor._verifyShareFields is same
        """
        if len(fields) > 1:
            if 'value' in fields:
                msg = "ParseError: Field = 'value' within fields = '%s'" % fields
                raise excepting.ParseError(msg, tokens, index)
        if share:
            for field in fields:
                if field not in share and ('value' in share or field == 'value'):
                    msg = "ParseError: Candidate field '%s' when fields = '%s' exist" % (
                     field, share.keys())
                    raise excepting.ParseError(msg, tokens, index)

    def validShareFields(self, share, fields):
        """Validates that updating fields in share won't violate the
           condition that when a share has field = 'value'
           it will be the only field

           fields is list of field names
           share is share

           returns False if condition would be violated
           return True otherwise
        """
        if len(fields) > 1:
            if 'value' in fields:
                return False
        if share:
            for field in fields:
                if field not in share:
                    if 'value' in share or field == 'value':
                        return False

        return True

    def verifyCurrentContext(self, tokens, index):
        """Verify that parse context has
           currentStore
           currentFramer
           currentFrame

           If not raises ParseError
        """
        if not self.currentStore:
            msg = "ParseError: Building verb '%s'. No current store" % tokens
            raise excepting.ParseError(msg, tokens, index)
        else:
            if not self.currentFramer:
                msg = "ParseError: Building verb '%s'. No current framer" % tokens
                raise excepting.ParseError(msg, tokens, index)
            msg = self.currentFrame or "ParseError: Building verb '%s'. No current frame" % tokens
            raise excepting.ParseError(msg, tokens, index)

    def verifyName(self, name, command, tokens, index):
        """Verify that name is a valid public identifyer
           Used for Tasker, Framer, and Frame names
        """
        if not REO_IdentPub.match(name) or name in Reserved:
            msg = "ParseError: Building verb '%s'. Invalid entity name '%s'" % (
             command, name)
            raise excepting.ParseError(msg, tokens, index)


def DebugShareFields(store, name):
    """ prints out  fields of share named name from store for debugging """
    share = store.fetch(name)
    if share is not None:
        console.terse('++++++++ Debug share fields++++++++\n{0} = {1}\n'.format(share.name, share.items))


def Test(fileName=None, verbose=False):
    """Module self test

    """
    import globaling, aiding, excepting, registering, storing, skedding, tasking, acting, poking, needing, goaling, traiting, fiating, wanting, completing, doing, arbiting, controlling, framing, logging, interfacing, housing, monitoring, testing
    allModules = [
     globaling, aiding, excepting, registering, storing, skedding,
     acting, poking, goaling, needing, traiting,
     fiating, wanting, completing,
     doing, arbiting, controlling,
     tasking, framing, logging, interfacing, serving,
     housing, monitoring, testing]
    if not fileName:
        fileName = 'mission.txt'
    b = Builder()
    if b.build(fileName=fileName):
        houses = b.houses
        for house in houses:
            house.store.changeStamp(0.0)
            for framer in house.actives:
                status = framer.runner.send(START)

            for tasker in house.taskers:
                status = tasker.runner.send(START)

        done = False
        while not done:
            done = True
            for house in houses:
                actives = []
                for framer in house.actives:
                    desire = framer.desire
                    if desire is not None:
                        control = desire
                    else:
                        control = RUN
                    status = framer.runner.send(control)
                    console.terse('Framer {0} control {1} resulting status = {2}\n'.format(framer.name, ControlNames[control], StatusNames[status]))
                    if not (status == STOPPED or status == ABORTED):
                        actives.append(framer)
                        done = False

                house.actives = actives
                for tasker in house.taskers:
                    status = tasker.runner.send(RUN)

                house.store.advanceStamp(0.125)

        for house in houses:
            for tasker in house.taskers:
                status = tasker.runner.send(STOP)

    return b


if __name__ == '__main__':
    Test()