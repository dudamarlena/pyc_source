# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/__main__.py
# Compiled at: 2018-03-07 03:59:08
# Size of source mod 2**32: 2323 bytes
import logging, os, sys, traceback
from pathlib import Path
import aiohttp_jinja2, jinja2
from aiohttp import web
from kipp.options import opt
from kipp.utils import check_is_allow_to_running, EmailSender
from ramjet.utils import logger
from ramjet.app import setup_web_handlers
from ramjet import settings
from ramjet.engines import shutdown_all_engines

def setup_template(app):
    aiohttp_jinja2.setup(app,
      loader=(jinja2.FileSystemLoader(str(Path(settings.CWD, 'tasks')))))


def setup_args():
    for k, v in settings.__dict__.items():
        opt.set_option(k, v)

    opt.add_argument('-t', '--tasks', default='', help='Tasks you want to run')
    opt.add_argument('-e', '--exclude-tasks', default='', help='Tasks you do not want to run')
    opt.add_argument('--debug', action='store_true', default=False)
    opt.add_argument('--smtp_host', type=str, default=None)
    opt.parse_args()


def setup_options():
    opt.set_option('email_sender', EmailSender(host=(settings.MAIL_HOST), port=(settings.MAIL_PORT),
      username=(settings.MAIL_USERNAME),
      passwd=(settings.MAIL_PASSWD)))


def main():
    try:
        try:
            setup_args()
            setup_options()
            if opt.debug:
                logger.info('start application in debug mode')
                logger.setLevel(logging.DEBUG)
            else:
                logger.info('start application in normal mode')
                logger.setLevel(logging.INFO)
            from ramjet.tasks import setup_tasks
            app = web.Application()
            setup_tasks(app)
            setup_template(app)
            setup_web_handlers(app)
            web.run_app(app, host='localhost', port=(opt.PORT))
        except Exception:
            logger.exception('ramjet got error:')
            opt.email_sender.send_email(mail_to=(settings.MAIL_TO_ADDRS),
              mail_from=(settings.MAIL_FROM_ADDR),
              subject='ramjet error',
              content=(traceback.format_exc()))

    finally:
        os._exit(0)


if __name__ == '__main__':
    main()