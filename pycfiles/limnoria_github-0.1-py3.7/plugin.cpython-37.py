# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limnoria_github/plugin.py
# Compiled at: 2020-05-08 12:52:23
# Size of source mod 2**32: 20677 bytes
import re, sys, json, time, hmac, urllib, socket, hashlib, fnmatch, threading
from string import Template
import supybot.log as log
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.httpserver as httpserver
if sys.version_info[0] < 3:
    from cStringIO import StringIO
    from urlparse import urlparse
    quote_plus = urllib.quote_plus
else:
    from io import StringIO
    from urllib.parse import urlparse
    quote_plus = urllib.parse.quote_plus
    basestring = str
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('GitHub')
except:
    _ = lambda x: x
    internationalizeDocstring = lambda x: x

if sys.version_info[0] >= 3:

    def b(s):
        return s.encode('utf-8')


    def u(s):
        return s


    urlencode = urllib.parse.urlencode
else:

    def u(s):
        return s.decode('utf-8')


    def b(s):
        return s


    urlencode = urllib.urlencode

def flatten_subdicts(dicts, flat=None):
    """Change dict of dicts into a dict of strings/integers. Useful for
    using in string formatting."""
    if flat is None:
        flat = {}
    if isinstance(dicts, list):
        return flatten_subdicts(dict(enumerate(dicts)))
    if isinstance(dicts, dict):
        for key, value in dicts.items():
            if isinstance(value, dict):
                value = dict(flatten_subdicts(value))
                for subkey, subvalue in value.items():
                    flat['%s__%s' % (key, subkey)] = subvalue

            else:
                flat[key] = value

        return flat
    return dicts


class GithubCallback(httpserver.SupyHTTPServerCallback):
    name = 'GitHub announce callback'
    defaultResponse = _("\n    You shouldn't be here, this subfolder is not for you. Go back to the\n    index and try out other plugins (if any).")

    def doPost(self, handler, path, form):
        headers = dict(self.headers)
        if sys.version_info[0] >= 3 and isinstance(form, bytes):
            valid_signatures = ['sha1=' + hmac.new(s.encode(), form, hashlib.sha1).hexdigest() for s in self.plugin.registryValue('announces.secret')]
        else:
            if sys.version_info[0] == 2:
                if isinstance(form, str):
                    valid_signatures = ['sha1=' + hmac.new(s.encode(), form, hashlib.sha1).hexdigest() for s in self.plugin.registryValue('announces.secret')]
                else:
                    valid_signatures = []
            elif valid_signatures and headers.get('X-Hub-Signature', None) not in valid_signatures:
                log.warning('%s', valid_signatures)
                log.warning('%s', headers.get('X-Hub-Signature', None))
                log.warning("'%s' tried to act as a web hook for Github,\n            but is not GitHub (no secret or invalid secret)." % handler.address_string())
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b('Error: you are not a GitHub server.'))
            else:
                try:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b('Thanks.'))
                except socket.error:
                    pass

                if 'X-GitHub-Event' in headers:
                    event = headers['X-GitHub-Event']
                else:
                    event = headers['x-github-event']
                if event == 'ping':
                    log.info('Got ping event from GitHub.')
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b('Thanks.'))
                    return
                payload = json.loads(form.decode('utf8'))
                self.plugin.announce.onPayload(headers, payload)


def query(caller, type_, uri_end, args):
    args = dict([(x, y) for x, y in args.items() if y is not None])
    url = '%s/%s/%s?%s' % (caller._url(), type_, uri_end,
     urlencode(args))
    if sys.version_info[0] >= 3:
        return json.loads(utils.web.getUrl(url).decode('utf8'))
    return json.load(utils.web.getUrlFd(url))


instance = None

@internationalizeDocstring
class GitHub(callbacks.Plugin):
    __doc__ = 'Add the help for "@plugin help GitHub" here\n    This should describe *how* to use this plugin.'

    def __init__(self, irc):
        global instance
        self._GitHub__parent = super(GitHub, self)
        callbacks.Plugin.__init__(self, irc)
        instance = self
        callback = GithubCallback()
        callback.plugin = self
        httpserver.hook('github', callback)
        for cb in self.cbs:
            cb.plugin = self

        if 'reply_env' not in ircmsgs.IrcMsg.__slots__:
            log.error("Your version of Supybot is not compatible with reply environments. So, the GitHub plugin won't be able to announce events from GitHub.")

    class announce(callbacks.Commands):

        def _shorten_url(self, url):
            try:
                data = urlencode({'url': url})
                if sys.version_info[0] >= 3:
                    data = data.encode()
                    f = utils.web.getUrlFd('https://git.io/', data=data)
                    url = list(filter(lambda x: x[0] == 'Location', f.headers._headers))[0][1].strip()
                else:
                    f = utils.web.getUrlFd('https://git.io/', data=data)
                    url = filter(lambda x: x.startswith('Location: '), f.headers.headers)[0].split(': ', 1)[1].strip()
            except Exception as e:
                try:
                    log.error('Cannot connect to git.io: %s (%s)' % (e, url))
                    return
                finally:
                    e = None
                    del e

            return url

        def _createPrivmsg(self, irc, channel, payload, event):
            bold = ircutils.bold
            format_ = self.plugin.registryValue('format.%s' % event, channel)
            if not format_.strip():
                return
            else:
                repl = flatten_subdicts(payload)
                for key, value in dict(repl).items():
                    if isinstance(value, basestring):
                        if value.startswith(('http://', 'https://')):
                            if key + '__tiny' in format_:
                                host = urlparse(value).netloc
                                if host == 'github.com' or host.endswith('.github.com'):
                                    url = self._shorten_url(value)
                                    if url:
                                        repl[key + '__tiny'] = url
                                    else:
                                        repl[key + '__tiny'] = value
                                else:
                                    repl[key + '__tiny'] = value
                        elif isinstance(value, basestring):
                            if re.search('^[a-f0-9]{40}$', value):
                                repl[key + '__short'] = value[0:7]
                        if key == 'commits':
                            repl['__num_commits'] = len(value)
                        elif key.endswith('ref'):
                            try:
                                repl[key + '__branch'] = value.split('/', 2)[2] if value else None
                            except IndexError:
                                pass

                        elif not isinstance(value, str):
                            if not sys.version_info[0] < 3 or isinstance(value, unicode):
                                repl[key + '__firstline'] = value.split('\n', 1)[0]

                tokens = callbacks.tokenize(format_)
                return tokens or None
            fake_msg = ircmsgs.IrcMsg(command='PRIVMSG', args=(
             channel, 'GITHUB'),
              prefix='github!github@github',
              reply_env=repl)
            try:
                self.plugin.Proxy(irc, fake_msg, tokens)
            except Exception as e:
                try:
                    self.plugin.log.exception('Error occured while running triggered command:')
                finally:
                    e = None
                    del e

        def onPayload(self, headers, payload):
            if 'reply_env' not in ircmsgs.IrcMsg.__slots__:
                log.error("Got event payload from GitHub, but your version of Supybot is not compatible with reply environments, so, the GitHub plugin can't announce it.")
            else:
                if 'full_name' in payload['repository']:
                    repo = payload['repository']['full_name']
                else:
                    if 'name' in payload['repository']['owner']:
                        repo = '%s/%s' % (payload['repository']['owner']['name'],
                         payload['repository']['name'])
                    else:
                        repo = '%s/%s' % (payload['repository']['owner']['login'],
                         payload['repository']['name'])
                if 'X-GitHub-Event' in headers:
                    event = headers['X-GitHub-Event']
                else:
                    event = headers['x-github-event']
            announces = self._load()
            repoAnnounces = set()
            for dbRepo, network, channel in announces:
                if fnmatch.fnmatch(repo, dbRepo):
                    repoAnnounces.add((network, channel))

            if len(repoAnnounces) == 0:
                log.info('Commit for repo %s not announced anywhere' % repo)
                return
            for network, channel in repoAnnounces:
                if network == '':
                    for irc in world.ircs:
                        if channel in irc.state.channels:
                            break

                else:
                    irc = world.getIrc(network)
                    if not irc:
                        log.warning('Received GitHub payload with announcing enabled in %s on unloaded network %s.', channel, network)
                        return
                if channel not in irc.state.channels:
                    log.info("Cannot announce event for repo %s in %s on %s because I'm not in %s." % (
                     repo, channel, irc.network, channel))
                if event == 'push':
                    commits = payload['commits']
                    hidden = None
                    if len(commits) == 0:
                        log.warning('GitHub push hook called without any commit.')
                    else:
                        last_commit = commits[(-1)]
                        max_comm = self.plugin.registryValue('max_announce_commits', channel)
                        if len(commits) > max_comm + 1:
                            hidden = len(commits) - max_comm
                            commits = commits[:max_comm]
                        payload2 = dict(payload)
                        self._createPrivmsg(irc, channel, payload2, 'before.push')
                        for commit in commits:
                            payload2['__commit'] = commit
                            self._createPrivmsg(irc, channel, payload2, 'push')

                    if hidden:
                        payload2['__hidden_commits'] = hidden
                        self._createPrivmsg(irc, channel, payload2, 'push.hidden')
                elif event == 'gollum':
                    pages = payload['pages']
                    if len(pages) == 0:
                        log.warning('GitHub gollum hook called without any page.')
                    else:
                        payload2 = dict(payload)
                        for page in pages:
                            payload2['__page'] = page
                            self._createPrivmsg(irc, channel, payload2, 'gollum')

                else:
                    self._createPrivmsg(irc, channel, payload, event)

        def _load(self):
            announces = instance.registryValue('announces').split(' || ')
            if announces == ['']:
                return []
            announces = [x.split(' | ') for x in announces]
            output = []
            for annc in announces:
                repo = annc[0]
                if len(annc) < 3:
                    net = ''
                    chan = annc[1]
                else:
                    net = annc[1]
                    chan = annc[2]
                output.append((repo, net, chan))

            return output

        def _save(self, data):
            stringList = []
            for announcement in data:
                stringList.extend([' | '.join(announcement)])

            string = ' || '.join(stringList)
            instance.setRegistryValue('announces', value=string)

        @internationalizeDocstring
        def add(self, irc, msg, args, channel, owner, name):
            """[<channel>] <owner> <name>

            Announce the commits of the GitHub repository called
            <owner>/<name> in the <channel>. Globs are also supported for
            <owner> and <name>.
            <channel> defaults to the current channel."""
            repo = '%s/%s' % (owner, name)
            announces = self._load()
            for dbRepo, net, chan in announces:
                if not dbRepo == repo or net == '' or net == irc.network:
                    if chan == channel:
                        irc.error(_('This repository is already announced to this channel.'))
                        return

            announces.append((repo, irc.network, channel))
            self._save(announces)
            irc.replySuccess()

        add = wrap(add, ['channel', 'something', 'something'])

        @internationalizeDocstring
        def remove(self, irc, msg, args, channel, owner, name):
            """[<channel>] <owner> <name>

            Don't announce the commits of the GitHub repository called
            <owner>/<name> in the <channel> anymore.
            <channel> defaults to the current channel."""
            repo = '%s/%s' % (owner, name)
            announces = self._load()
            for annc in announces:
                if not annc[0] == repo or annc[1] == '' or annc[1] == irc.network:
                    if annc[2] == channel:
                        announces.remove(annc)
                        self._save(announces)
                        irc.replySuccess()
                        return

            irc.error(_('This repository is not yet announced to this channel.'))

        remove = wrap(remove, ['channel', 'something', 'something'])

    class repo(callbacks.Commands):

        def _url(self):
            url = instance.registryValue('api.url')
            if url == 'http://github.com/api/v2/json':
                url = 'https://api.github.com'
                instance.setRegistryValue('api.url', value=url)
            return url

        @internationalizeDocstring
        def search(self, irc, msg, args, search, optlist):
            """<searched string> [--page <id>] [--language <language>]

            Searches the string in the repository names database. You can
            specify the page <id> of the results, and restrict the search
            to a particular programming <language>."""
            args = {'page':None, 
             'language':None}
            for name, value in optlist:
                if name in args:
                    args[name] = value

            results = query(self, 'legacy/repos/search', quote_plus(search), args)
            reply = ' & '.join(('%s/%s' % (x['owner'], x['name']) for x in results['repositories']))
            if reply == '':
                irc.error(_('No repositories matches your search.'))
            else:
                irc.reply(u(reply))

        search = wrap(search, ['something',
         getopts({'page':'id',  'language':'somethingWithoutSpaces'})])

        @internationalizeDocstring
        def info(self, irc, msg, args, owner, name, optlist):
            """<owner> <repository> [--enable <feature> <feature> ...]             [--disable <feature> <feature>]

            Displays informations about <owner>'s <repository>.
            Enable or disable features (ie. displayed data) according to the
            request)."""
            enabled = [
             'watchers', 'forks', 'pushed_at', 'open_issues',
             'description']
            for mode, features in optlist:
                features = features.split(' ')
                for feature in features:
                    if mode == 'enable':
                        enabled.append(feature)
                    else:
                        try:
                            enabled.remove(feature)
                        except ValueError:
                            pass

            results = query(self, 'repos', '%s/%s' % (owner, name), {})
            output = []
            for key, value in results.items():
                if key in enabled:
                    output.append('%s: %s' % (key, value))

            irc.reply(u(', '.join(output)))

        info = wrap(info, ['something', 'something',
         getopts({'enable':'anything',  'disable':'anything'})])

    def die(self):
        self._GitHub__parent.die()
        httpserver.unhook('github')


Class = GitHub