# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/stats.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 4926 bytes
__doc__ = '\nstats.py: Simple statistics for PyLink IRC Services.\n'
import datetime, time
from pylinkirc import conf, utils, world
from pylinkirc.coremods import permissions
from pylinkirc.log import log

def timediff(before, now):
    """
    Returns the time difference between "before" and "now" as a formatted string.
    """
    td = datetime.timedelta(seconds=(now - before))
    days = td.days
    hours, leftover = divmod(td.seconds, 3600)
    minutes, seconds = divmod(leftover, 60)
    return '%d day%s, %02d:%02d:%02d' % (td.days, 's' if td.days != 1 else '',
     hours, minutes, seconds)


DEFAULT_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S +0000'

@utils.add_cmd
def uptime(irc, source, args):
    """[<network> / --all]

    Returns the uptime for PyLink and the given network's connection (or the current network if not specified).
    The --all argument can also be given to show the uptime for all networks."""
    permissions.check_permissions(irc, source, ['stats.uptime'])
    try:
        network = args[0]
    except IndexError:
        network = irc.name

    if network == '--all':
        ircobjs = {k:v for k, v in world.networkobjects.items() if v.connected.is_set() if v.connected.is_set()}
    else:
        try:
            ircobjs = {network: world.networkobjects[network]}
        except KeyError:
            irc.error('No such network %r.' % network)
            return

    if not world.networkobjects[network].connected.is_set():
        irc.error('Network %s is not connected.' % network)
        return
    current_time = int(time.time())
    time_format = conf.conf.get('stats', {}).get('time_format', DEFAULT_TIME_FORMAT)
    irc.reply('PyLink uptime: \x02%s\x02 (started on %s)' % (
     timediff(world.start_ts, current_time),
     time.strftime(time_format, time.gmtime(world.start_ts))))
    for network, ircobj in sorted(ircobjs.items()):
        irc.reply('Connected to %s: \x02%s\x02 (connected on %s)' % (
         network,
         timediff(ircobj.start_ts, current_time),
         time.strftime(time_format, time.gmtime(ircobj.start_ts))))


def handle_stats(irc, source, command, args):
    """/STATS handler. Currently supports the following:

    c - link blocks
    o - oper blocks (accounts)
    u - shows uptime
    """
    stats_type = args['stats_type'][0].lower()
    perms = [
     'stats.%s' % stats_type]
    if stats_type == 'u':
        perms.append('stats.uptime')
    else:
        try:
            permissions.check_permissions(irc, source, perms)
        except utils.NotAuthorizedError as e:
            irc.msg(source, ('Error: %s' % e), notice=True)
            return

        log.info('(%s) /STATS %s requested by %s', irc.name, stats_type, irc.get_hostmask(source))

        def _num(num, text):
            irc.numeric(args['target'], num, source, text)

        if stats_type == 'c':
            for netname, serverdata in sorted(conf.conf['servers'].items()):
                _num(213, 'C %s * %s %s [%s:%s:%s]' % (
                 serverdata.get('ip', '0.0.0.0'),
                 netname,
                 serverdata.get('port', 0),
                 serverdata['protocol'],
                 'ssl' if serverdata.get('ssl') else 'no-ssl',
                 serverdata.get('encoding', 'utf-8')))

        else:
            if stats_type == 'o':
                for accountname, accountdata in conf.conf['login'].get('accounts', {}).items():
                    networks = accountdata.get('networks', [])
                    if irc.name in networks or not networks:
                        _num(243, 'O %s * %s :%s' % ' '.join(accountdata.get('hosts', ['*@*']), accountname, 'needoper' if accountdata.get('require_oper') else ''))

            else:
                if stats_type == 'u':
                    _num(242, ':Server Up %s' % timediff(world.start_ts, int(time.time())))
                else:
                    log.info('(%s) Unknown /STATS type %r requested by %s', irc.name, stats_type, irc.get_hostmask(source))
    _num(219, '%s :End of /STATS report' % stats_type)


utils.add_hook(handle_stats, 'STATS')