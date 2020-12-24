# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ibis/ymartin/WellInverter/pyLoadBalancer/pyLoadBalancer/Monitor/MonitoringApp.py
# Compiled at: 2016-11-09 09:27:10
# Size of source mod 2**32: 3706 bytes
import tornado.auth, tornado.escape, tornado.ioloop, tornado.options, tornado.web, os.path, json, pprint
from tornado.escape import json_decode
from tornado.escape import json_encode
import zmq
from ..colorprint import cprint
import argparse, sys
from tornado.options import define, options
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
    print('MONITOR - Conected to ', LB_HEALTHADRESS)


def sendReq(LBReqSock, command):
    try:
        LBReqSock.connect(LB_HEALTHADRESS)
        command['MONITOR'] = command.pop('iwouldlike')
        print('SENDING : ', command)
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
          '/jsontoLB/', WorkersHandler)]
        settings = dict(debug=True, template_path=os.path.join(os.path.dirname(__file__), 'templates'), static_path=os.path.join(os.path.dirname(__file__), 'static'))
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', messages=None)


class WorkersHandler(tornado.web.RequestHandler):

    def post(self):
        global LBReqSock
        json_obj = json_decode(self.request.body)
        print('Post data received')
        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        if 'iwouldlike' in json_obj:
            response_to_send = sendReq(LBReqSock, json_obj)
        print('Response to return')
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))


def main():
    global LBReqSock
    global LB_HEALTHADRESS
    parser = argparse.ArgumentParser(description='Monitor Server Script for the pyLoadBalancer module.')
    parser.add_argument('-p', '--pfile', default=None, help='parameter file, in JSON format')
    parser.add_argument('-port', '--port', default=9000, help='web server port')
    parser.add_argument('-a', '--adress', default='127.0.0.1', help='web server ip adress')
    args = parser.parse_args()
    with open(os.path.join(os.path.dirname(__file__), '../parameters.json'), 'r') as (fp):
        CONSTANTS = json.load(fp)
    if args.pfile != None:
        try:
            with open(args.pfile, 'r') as (fp):
                CONSTANTS.update(json.load(fp))
        except:
            cprint('ERROR : %s is not a valid JSON file' % args.pfile, 'FAIL')
            sys.exit()

    define('port', default=args.port, help='run on the given port', type=int)
    LB_HEALTHADRESS = 'tcp://' + CONSTANTS['LB_IP'] + ':' + str(CONSTANTS['LB_HCREPPORT'])
    LBReqSock = context.socket(zmq.REQ)
    setLBReqSock(LBReqSock)
    app = Application()
    app.listen(options.port, address=args.adress)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()