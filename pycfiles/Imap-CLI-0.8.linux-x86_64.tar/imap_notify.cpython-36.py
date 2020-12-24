# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/scripts/imap_notify.py
# Compiled at: 2018-04-21 11:53:05
# Size of source mod 2**32: 2388 bytes
"""Use IMAP CLI to gt a summary of IMAP account state."""
import logging, os, sys, time, docopt, pynotify, imap_cli
from imap_cli import config
app_name = os.path.splitext(os.path.basename(__file__))[0]
usage = 'Usage: imap-cli-notifier [options] <directories>...\n\nOptions:\n    -d, --delay=<delay>         Delay (in seconds) between notifications\n    -c, --config-file=<FILE>    Configuration file (`~/.config/imap-cli`)\n    -f, --format=<FMT>          Output format\n    -v, --verbose               Generate verbose messages\n    -h, --help                  Show help options.\n    --version                   Print program version.\n\n----\nCopyright (C) 2014 Romain Soufflet\nLicense MIT\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n'
log = logging.getLogger(app_name)

def main():
    args = docopt.docopt('\n'.join(usage.split('\n')))
    logging.basicConfig(level=(logging.DEBUG if args['--verbose'] else logging.WARNING),
      stream=(sys.stdout))
    pynotify.init(app_name)
    connection_config = config.new_context_from_file((args['--config-file']), section='imap')
    if connection_config is None:
        return 1
    try:
        delay = int(args['--delay'] or 60)
    except ValueError:
        log.error('Wrong value for options "delay"')
        return 1
    else:
        format_str = args['--format'] or ' '.join([
         '{recent:<3} new mails in ',
         '{directory} ({count} total)'])
        imap_account = (imap_cli.connect)(**connection_config)
        time_count = 0
        sys.stdout.write('\n')
        while True:
            time_count += 1
            if time_count % delay == 0:
                notifications = []
                for status in imap_cli.status(imap_account):
                    if status['directory'] in args['<directories>'] and status['recent'] != '0':
                        notifications.append((format_str.format)(**status))

                if len(notifications) > 0:
                    notifier = pynotify.Notification('IMAP Notify', '\n'.join(notifications))
                    notifier.show()
            time.sleep(1)

        return 0


if __name__ == '__main__':
    sys.exit(main())