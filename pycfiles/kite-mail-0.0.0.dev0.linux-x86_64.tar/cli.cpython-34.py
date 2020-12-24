# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/kite_mail/cli.py
# Compiled at: 2015-07-05 09:31:01
# Size of source mod 2**32: 1301 bytes
import click
from kite.takosan import Tako
from kite_mail.mail import kiteMail
from kite_mail.utils import help_messages

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('takosan_url', nargs=1, required=True)
@click.option('--channel', 'channels', nargs=1, required=True, multiple=True, help=help_messages('channel'))
@click.option('--name', nargs=1, default='Mail Notify', help=help_messages('name'))
@click.option('--icon', nargs=1, default=':mailbox_with_mail:', help=help_messages('icon'))
@click.option('--body/--no-body', default=False, help=help_messages('body'))
def main(takosan_url, channels, name, icon, body):
    RAW_MAIL = click.get_text_stream('stdin')
    kite_mail = kiteMail(RAW_MAIL)
    factory = kite_mail.factory
    notify_payload = {'name': name, 
     'icon': icon, 
     'message': ':round_pushpin: *{0}*'.format(factory.get_subject()), 
     'pretext': ':black_nib: From: {0[0]} {0[1]}'.format(factory.get_address('from'))}
    if body:
        notify_payload['text'] = kite_mail.get_mailpart()
    kite = Tako(takosan_url, channels, notify_payload)
    kite.flying()


if __name__ == '__main__':
    main()