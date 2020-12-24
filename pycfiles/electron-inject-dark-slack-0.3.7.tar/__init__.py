# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: electron_inject_dark_slack\__init__.py
# Compiled at: 2017-06-28 22:20:16
import requests, time, websocket, json, socket, subprocess, time, string
SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH = 'document.addEventListener("keydown", function (e) {\n    if (e.which === 123) {\n        //F12\n\t\tconsole.log("test");\n        require("electron").remote.BrowserWindow.getFocusedWindow().webContents.toggleDevTools();\n    } else if (e.which === 116) {\n        //F5\n        location.reload();\n    }\n});'
SCRIPT_ENABLE_DARK_THEME_SLACK = "\n\tvar cssPath = '" + string.replace(string.replace(__file__, '\\', '/'), '__init__.pyc', 'dark.css') + '\';\n\tvar css = require("fs").readFileSync(cssPath,\'utf8\');\n\tconst webview = document.querySelectorAll(\'webview\');\n\tfor (var i = 0; i < webview.length; i++) {\n\t\twebview[i].insertCSS(css);\n\t\t//webview[i].openDevTools();\n\t}\n\t\n'

class LazyWebsocket(object):

    def __init__(self, url):
        self.url = url
        self.ws = None
        return

    def _connect(self):
        if not self.ws:
            self.ws = websocket.create_connection(self.url)
        return self.ws

    def send(self, *args, **kwargs):
        return self._connect().send(*args, **kwargs)

    def recv(self, *args, **kwargs):
        return self.ws.recv(*args, **kwargs)

    def sendrcv(self, msg):
        self.send(msg)
        return self.recv()

    def close(self):
        self.ws.close()


class ElectronRemoteDebugger(object):

    def __init__(self, host, port):
        self.params = {'host': host, 'port': port}

    def windows(self):
        params = self.params.copy()
        params.update({'ts': int(time.time())})
        ret = []
        for w in self.requests_get('http://%(host)s:%(port)s/json/list?t=%(ts)d' % params).json():
            url = w.get('webSocketDebuggerUrl')
            if not url:
                continue
            w['ws'] = LazyWebsocket(url)
            ret.append(w)

        return ret

    def requests_get(self, url, tries=5, delay=1):
        last_exception = None
        for _ in xrange(tries):
            try:
                return requests.get(url)
            except requests.exceptions.ConnectionError as ce:
                last_exception = ce

            time.sleep(delay)

        raise ce
        return

    def sendrcv(self, w, msg):
        return w['ws'].sendrcv(msg)

    def eval(self, w, expression):
        data = {'id': 1, 'method': 'Runtime.evaluate', 
           'params': {'contextId': 1, 'doNotPauseOnExceptionsAndMuteConsole': False, 
                      'expression': expression, 
                      'gneratePreview': False, 
                      'includeCommandLineAPI': True, 
                      'objectGroup': 'console', 
                      'returnByValue': False, 
                      'userGesture': True}}
        ret = json.loads(w['ws'].sendrcv(json.dumps(data)))
        if 'result' not in ret:
            return ret
        return ret['result']

    @classmethod
    def execute(cls, path):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        cmd = '%s %s' % (path, '--remote-debugging-port=%d' % port)
        print cmd
        p = subprocess.Popen(cmd, shell=True)
        if not p > 0:
            raise Exception('Could not execute cmd: %r' % cmd)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for _ in xrange(30):
            result = sock.connect_ex(('localhost', port))
            if result > 0:
                break
            time.sleep(1)

        return cls('localhost', port=port)