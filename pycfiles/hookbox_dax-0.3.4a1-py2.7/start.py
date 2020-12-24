# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/hookbox/start.py
# Compiled at: 2012-07-04 04:55:04
import output_wrapper, eventlet
from server import HookboxServer
import os, sys
from hookbox.config import HookboxConfig
import hookbox.log as log
from eventlet import hubs

def create_server(bound_socket, bound_api_socket, config, outputter):
    server = HookboxServer(bound_socket, bound_api_socket, config, outputter)
    return server


def run_objgraph(server, config):
    import objgraph
    eventlet.sleep(config['objgraph'])
    print 'creating objgraph image file now'
    objgraph.show_backrefs([server])
    sys.exit(0)


def main(bound_socket=None, bound_api_socket=None):
    hubs.use_hub('pyevent')
    config = HookboxConfig()
    config.update_from_commandline_arguments(sys.argv)
    log.setup_logging(config)
    server = create_server(bound_socket, bound_api_socket, config, output_wrapper.outputter)
    if config['objgraph']:
        eventlet.spawn(run_objgraph, server, config)
    if config['debug']:
        eventlet.spawn(debugloop)
    try:
        server.run().wait()
    except KeyboardInterrupt:
        print 'Ctr+C pressed; Exiting.'


def debugloop():
    from pyjsiocompile.compile import main as pyjsiocompile
    files = {}
    for f in ['hookbox.pkg', 'hookbox.js']:
        files[f] = os.stat(os.path.join(os.path.dirname(__file__), 'js_src', f))[7]

    while True:
        eventlet.sleep(0.1)
        recompile = False
        for f in ['hookbox.pkg', 'hookbox.js']:
            modified = os.stat(os.path.join(os.path.dirname(__file__), 'js_src', f))[7]
            if files[f] != modified:
                files[f] = modified
                recompile = True

        if recompile:
            src = os.path.join(os.path.dirname(__file__), 'js_src', 'hookbox.pkg')
            out = os.path.join(os.path.dirname(__file__), 'static', 'hookbox.js')
            pyjsiocompile([src, '--output', out])


if __name__ == '__main__':
    main()