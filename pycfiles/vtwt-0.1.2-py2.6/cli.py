# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/cli.py
# Compiled at: 2010-07-13 10:04:43
import os, sys, traceback
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python.filepath import FilePath
from twisted.python.text import greedyWrap
from jersey import cli, log
from vtwt import util
from vtwt.svc import VtwtService
from oauth import oauth
from twisted.python import reflect

def safe_unicode(obj):
    return reflect._safeFormat(unicode, obj)


reflect.safe_str = safe_unicode

class Options(cli.Options):
    pass


class CommandBase(cli.Command):

    def __init__(self, config):
        cli.Command.__init__(self, config)

    def failWhale(self, error):
        config = self.config
        while config.parent and 'COLUMNS' not in config:
            config = config.parent

        columns = config.get('COLUMNS', 80)
        return util.failWhale(error, columns)

    def formatMsgSimple(self, msg, screenNameWidth=None):
        snw = screenNameWidth if screenNameWidth else len(msg.user.screen_name)
        padding = ' ' * (snw + 2)
        fmt = '{msg.user.screen_name:{snw}}  {text}'
        return self._formatMsg(msg, fmt, padding, snw)

    def formatMsgLong(self, msg, screenNameWidth=None):
        snw = screenNameWidth if screenNameWidth else len(msg.user.screen_name)
        padding = '  '
        fmt = '* {msg.user.screen_name}  {msg.id}  {msg.created_at}\n' + padding + '{text}\n'
        return self._formatMsg(msg, fmt, padding, snw)

    def _formatMsg(self, msg, fmt, padding, snw):
        fmt = unicode(fmt)
        text = unicode(self._wrapText(msg, fmt, padding))
        out = fmt.format(msg=msg, text=text, snw=snw)
        return out

    def _wrapText(self, msg, fmt, padding):
        width = self.config.parent['COLUMNS'] - len(padding)
        lines = greedyWrap(msg.text, width)
        return ('\n' + padding).join(lines)

    def _print(self, text, stream=None):
        if stream is None:
            stream = sys.stdout
        enc = getattr(stream, 'encoding', None)
        if enc:
            text.encode(enc)
        print >> stream, text
        return


class Command(CommandBase):

    def __init__(self, config):
        CommandBase.__init__(self, config)
        self.vtwt = self._buildVtwt()

    def _buildVtwt(self):
        if 'oauth-token' not in self.config.parent or 'oauth-token-secret' not in self.config.parent:
            raise cli.UsageError('No authentication token specified')
        oauthToken = oauth.OAuthToken(self.config.parent['oauth-token'], self.config.parent['oauth-token-secret'])
        svc = VtwtService(oauthToken)
        svc.setServiceParent(self)
        return svc


class CommandFactory(cli.CommandFactory):
    pass


class VtwtOptions(cli.PluggableOptions):
    defaultSubCommand = 'watch'
    optFlags = [
     [
      'debug', 'D', 'Turn debugging messages on']]
    optParameters = [
     [
      'config-file', 'c',
      os.path.expanduser('~/.vtwtrc'), 'Vtwt config file'],
     [
      'oauth-token', 'o', None, 'OAuth access token.'],
     [
      'oauth-token-secret', 'O', None, 'OAuth access token secret.']]

    @property
    def commandPackage(self):
        import vtwt
        return vtwt

    def postOptions(self):
        if self['debug']:
            self.logLevel = log.TRACE
        else:
            self.logLevel = log.ERROR + 1
        cf = FilePath(self['config-file'])
        if cf.exists():
            self.readConfigFile(cf)
        if self.subCommand != 'oauth' and not (self['oauth-token'] and self['oauth-token-secret']):
            raise cli.UsageError("No OAuth token specified.  Run the 'oauth' subcommand.")
        self['COLUMNS'] = int(os.getenv('COLUMNS', 80))

    def readConfigFile(self, configFile):
        fileNS = dict()
        execfile(configFile.path, fileNS)
        for configKey in fileNS.iterkeys():
            k = configKey.replace('_', '-')
            if k in self and self[k] is None:
                self[k] = fileNS[configKey]

        return


class VtwtCommander(cli.PluggableCommandRunner):

    def preApplication(self):
        import logging
        logging.raiseExceptions = False


def run(args=sys.argv[:]):
    program = os.path.basename(args[0])
    args = args[1:]
    opts = VtwtOptions(program)
    try:
        opts.parseOptions()
        vtwt = VtwtCommander(program, opts)
        vtwt.run()
    except cli.UsageError, ue:
        print >> sys.stderr, str(opts)
        print >> sys.stderr, str(ue)
        raise SystemExit(os.EX_USAGE)
    else:
        raise SystemExit(vtwt.exitValue)