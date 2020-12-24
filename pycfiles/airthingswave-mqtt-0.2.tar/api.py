# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\administrator\pycharmprojects\airtest_for_h9\airtest\webgui\routers\api.py
# Compiled at: 2014-12-03 20:37:50
import os, time, flask, airtest, cv2
from . import utils
app = None
bp = flask.Blueprint('api', __name__)

@bp.route('/')
def home():
    return 'API documentation'


@bp.route('/snapshot')
def snapshot():
    global app
    filename = '%d-screen.png' % int(time.time())
    if os.path.exists(filename):
        os.unlink(filename)
    app.takeSnapshot(os.path.join(utils.TMPDIR, filename))
    return flask.jsonify(dict(filename=filename))


@bp.route('/crop')
def crop():
    rget = flask.request.args.get
    filename = rget('filename')
    screen = rget('screen')
    x, y = int(rget('x')), int(rget('y'))
    width, height = int(rget('width')), int(rget('height'))
    screen_file = screen.lstrip('/').replace('/', os.sep)
    screen_path = os.path.join(utils.selfdir(), screen_file)
    output_path = os.path.join(utils.workdir(), filename)
    assert os.path.exists(screen_path)
    im = cv2.imread(screen_path)
    cv2.imwrite(output_path, im[y:y + height, x:x + width])
    return flask.jsonify(dict(success=True, message='文件已保存: ' + output_path.encode('utf-8')))


@bp.route('/run')
def run_code():
    code = flask.request.args.get('code')
    try:
        exec code
    except Exception as e:
        return flask.jsonify(dict(success=False, message=str(e)))

    return flask.jsonify(dict(success=True, message=''))


@bp.route('/connect')
def connect():
    global app
    device = flask.request.args.get('device')
    devno = flask.request.args.get('devno')
    try:
        app = airtest.connect(devno, device=device, monitor=False)
    except Exception as e:
        return flask.jsonify(dict(success=False, message=str(e)))

    return flask.jsonify(dict(success=True, message=''))