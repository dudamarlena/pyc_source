# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/slugs/SLUGS/slugs/app.py
# Compiled at: 2018-03-15 13:29:23
import argparse, cherrypy, os
from slugs import controllers
from slugs import plugins

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', type=str, default='/etc/slugs/slugs.conf', help='Configuration file path.')
    return parser


def check_arguments(args):
    if not os.path.exists(args.config):
        raise ValueError(("Configuration file path '{}' does not exist.").format(args.config))


def main():
    parser = build_parser()
    args = parser.parse_args()
    check_arguments(args)
    cherrypy.config.update(args.config)
    controller = controllers.MainController()
    application = cherrypy.tree.mount(controller, '/slugs', config=args.config)
    plugins.FileMonitoringPlugin(cherrypy.engine, application.config.get('data').get('user_group_mapping'), controller.update).subscribe()
    if hasattr(cherrypy.engine, 'block'):
        cherrypy.engine.start()
        cherrypy.engine.block()
    else:
        cherrypy.server.quickstart()
        cherrypy.engine.start()


if __name__ == '__main__':
    main()