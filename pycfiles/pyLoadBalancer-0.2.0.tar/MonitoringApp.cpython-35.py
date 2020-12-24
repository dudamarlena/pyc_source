# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ibis/ymartin/WellInverter/pyLoadBalancer/pyLoadBalancer/Monitor/MonitoringApp.py
# Compiled at: 2017-05-03 05:23:36
# Size of source mod 2**32: 4521 bytes
import tornado.escape, tornado.ioloop, tornado.options, tornado.web, os.path, json, pprint
from tornado.escape import json_decode
from tornado.escape import json_encode
import zmq
from ..colorprint import cprint
import argparse, sys
from tornado.options import define, options
import atexit, signal
context = zmq.Context()
LB_HEALTHADRESS = None
LBReqSock = None
SOCKET_TIMEOUT = 1000

def setLBReqSock(LBReqSock):
    global LB_HEALTHADRESS
    LBReqSock.setsockopt(zmq.RCVTIMEO, SOCKET_TIMEOUT)
    LBReqSock.setsockopt(zmq.SNDTIMEO, SOCKET_TIMEOUT)
    LBReqSock.setsockopt(zmq.REQ_RELAXED, 1)
    LBReqSock.setsockopt(zmq.LINGER, 0)
    LBReqSock.connect(LB_HEALTHADRESS)


def sendReq(LBReqSock, command):
    try:
        LBReqSock.connect(LB_HEALTHADRESS)
        command['MONITOR'] = command.pop('iwouldlike')
        LBReqSock.send_json(command)
        return LBReqSock.recv_json()
    except Exception as e:
        cprint('MONITOR - FAILED REQUESTING LOAD BALANCER: LB DOWN ? %s' % str(e), 'FAIL')
        LBReqSock.disconnect(LB_HEALTHADRESS)
        setLBReqSock(LBReqSock)
        return 0


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
         (
          '/', MainHandler),
         (
          '', MainHandler),
         (
          '/jsontoLB/', WorkersHandler)]
        settings = dict(autoreload=False, template_path=os.path.join(os.path.dirname(__file__), 'templates'), static_path=os.path.join(os.path.dirname(__file__), 'static'))
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', messages=None)


class WorkersHandler(tornado.web.RequestHandler):

    def post(self):
        global LBReqSock
        json_obj = json_decode(self.request.body)
        if 'iwouldlike' in json_obj:
            response_to_send = sendReq(LBReqSock, json_obj)
        self.write(json.dumps(response_to_send))


def startMonitorServer(parametersfile=None):
    global LBReqSock
    global LB_HEALTHADRESS
    with open(os.path.join(os.path.dirname(__file__), '../parameters.json'), 'r') as (fp):
        CONSTANTS = json.load(fp)
    if parametersfile != None:
        try:
            with open(parametersfile, 'r') as (fp):
                CONSTANTS.update(json.load(fp))
        except:
            cprint('ERROR : %s is not a valid JSON file' % parametersfile, 'FAIL')
            sys.exit()

        define('port', default=CONSTANTS['MONITOR_PORT'], help='run on the given port', type=int)
        LB_HEALTHADRESS = 'tcp://' + CONSTANTS['LB_IP'] + ':' + str(CONSTANTS['LB_HCREPPORT'])
        LBReqSock = context.socket(zmq.REQ)
        setLBReqSock(LBReqSock)
        app = Application()
        WSGI = False
        if WSGI:
            from tornado.wsgi import WSGIAdapter
            import wsgiref.simple_server
            wsgi_app = WSGIAdapter(app)
            server = wsgiref.simple_server.make_server(args.adress, args.port, wsgi_app)
            server.serve_forever()
    else:
        app.listen(options.port, address=CONSTANTS['MONITOR_IP'])
        loop = tornado.ioloop.IOLoop.instance()

        def sighup_handler(*args):
            cprint('EXITING Monitor', 'OKBLUE')
            loop.stop()

        atexit.register(sighup_handler)
        signal.signal(signal.SIGTERM, sighup_handler)
        signal.signal(signal.SIGINT, sighup_handler)
        loop.start()
        cprint('EXITED Monitor', 'OKGREEN')


def main():
    parser = argparse.ArgumentParser(description='Monitor Server Script for the pyLoadBalancer module.')
    parser.add_argument('-p', '--pfile', default=None, help='parameter file, in JSON format')
    parser.add_argument('-port', '--port', default=9000, help='web server port')
    parser.add_argument('-a', '--adress', default='127.0.0.1', help='web server ip adress')
    args = parser.parse_args()
    startMonitorServer(parametersfile=args.pfile, port=args.port, adress=args.adress)


if __name__ == '__main__':
    main()