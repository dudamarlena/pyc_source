# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\webservice.py
# Compiled at: 2013-02-15 22:49:32
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import base64, os, contextlib, sha
from operator import itemgetter, attrgetter
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import PySide.QtCore as _qc, PySide.QtGui as _qg, tornado, tornado.web, tornado.escape, threading, banta.db as _db, banta.packages as _pack, banta.utils as _utils

class WrongUser(Exception):

    def __init__(self, *args):
        Exception.__init__(self, b'Incorrect user or password')


class WrongSchema(Exception):

    def __init__(self, *args):
        Exception.__init__(self, b'Schema not supported, only Basic.')


class JsonWriter(object):
    """Context manager for a json writer.
        needs an argument, an instance that inherits from RequestHandler
        (which must implement the method write and set_header)
        it will create a dictionary in where the data should be stored
        When it finishes it writes everything back as a json, and sets the headers.
        if there where any exception, it sets the success flag to False, and logs the exception
        """

    def __init__(self, instance=None):
        self.ins = instance

    def __enter__(self):
        self.res = res = {b'success': False}
        return self.res

    def __exit__(self, exc_type, exc_val, exc_tb):
        act = 0
        if exc_type is None:
            self.res[b'success'] = True
            self.res[b'error'] = b''
        else:
            if exc_type == WrongSchema:
                self.ins.set_status(500)
                self.ins.set_header(b'WWW-Authenticate', b'basic realm="Banta"')
            elif exc_type == WrongUser:
                self.ins.set_status(401)
                self.ins.set_header(b'WWW-Authenticate:', b'basic realm="Banta"')
            error = unicode(exc_val)
            logger.exception(b'Caught exception on product modification.\n' + error)
            self.res[b'error'] = error
            self.res[b'success'] = False
            act = 1
        self.ins.set_header(b'Content-Type', b'application/json; charset=utf-8')
        json = tornado.escape.json_encode(self.res)
        if isinstance(json, unicode):
            json = json.encode(b'utf-8', b'replace')
        self.ins.write(json)
        self.ins.onAct.emit(act)
        return True


class BasicAuthHandler(_qc.QObject, tornado.web.RequestHandler):
    onAct = _qc.Signal(int)
    SUPPORTED_METHODS = ('GET', 'HEAD', 'POST', 'DELETE', 'PATCH', 'PUT', 'OPTIONS')

    def __init__(self, *args, **kwargs):
        _qc.QObject.__init__(self)
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

    def initialize(self, server_thread, *args, **kwargs):
        self.server_thread = server_thread
        self.onAct.connect(self.server_thread.bling, _qc.Qt.QueuedConnection)

    def get_current_user(self, root):
        scheme, sep, token = self.request.headers.get(b'Authorization', b'').partition(b' ')
        if scheme.lower() != b'basic':
            raise WrongSchema()
        username, pwd = token.decode(b'base64').decode(b'utf-8').split(b':', 1)
        for user in root[b'users']:
            if user.name == username:
                if user.password == pwd:
                    return user

        raise WrongUser()


class ProdImg(BasicAuthHandler):

    def get(self, *args, **kwargs):
        code = self.get_argument(b'code', None)
        if code:
            with _db.DB.threaded() as (root):
                self.set_header(b'Content-Type', b'image')
                if code in root[b'products']:
                    prod = root[b'products'][code]
                    if prod.thumb:
                        self.write(prod.thumb.open(b'r').read())
                        return
        return


class HProducts(BasicAuthHandler):
    changed = _qc.Signal(int)
    deleteProduct = _qc.Signal(int)

    def initialize(self, server_thread):
        BasicAuthHandler.initialize(self, server_thread)
        self.changed.connect(self.server_thread.syncDB, _qc.Qt.QueuedConnection)
        self.deleteProduct.connect(self.server_thread.deleteProduct, _qc.Qt.QueuedConnection)

    def _prodDict(self, p):
        imgurl = p.thumb and b'../prod_img/?code=' + p.code or b'thumb.jpg'
        return {b'code': p.code, b'name': p.name, b'price': p.price, b'stock': p.stock, b'thumb': imgurl}

    def _prodFullDict(self, p):
        return {b'code': p.code, 
           b'name': p.name, b'price': p.price, b'stock': p.stock, b'external_code': p.external_code, 
           b'buy_price': p.buy_price, b'pack_units': p.pack_units, 
           b'provider': p.provider and p.provider.name or b'', 
           b'category': p.category and p.category.name or b''}

    def get(self, *args, **kwargs):
        """Lists one or many products
                depending on the parameters
                """
        code = self.get_argument(b'search_code', None)
        if code:
            self._getProduct(code)
        else:
            self._getProductList()
        return

    def _getProduct(self, code):
        with JsonWriter(self) as (res):
            with _db.DB.threaded() as (root):
                prods = []
                if code in root[b'products']:
                    prod = root[b'products'][code]
                    prods.append(self._prodDict(prod))
                else:
                    raise Exception(b'Producto no encontrado')
                res[b'count'] = len(prods)
                res[b'total'] = len(root[b'products'])
                res[b'data'] = prods

    def _getProductList(self):
        with JsonWriter(self) as (res):
            with _db.DB.threaded() as (root):
                start = int(self.get_argument(b'start', 0))
                limit = int(self.get_argument(b'limit', 100))
                search_name = self.get_argument(b'search_name', b'').lower()
                order_by = self.get_argument(b'order_by', b'').lower()
                reversed = self.get_argument(b'order_asc', b'1').lower() != b'1'
                products = root[b'products']
                prod_list = products.values()
                if order_by in ('stock', 'name', 'price', 'code'):
                    prod_list = sorted(prod_list, key=attrgetter(order_by), reverse=reversed)

                def filter_name(p):
                    return search_name in p.name.lower()

                if search_name:
                    prod_list = filter(filter_name, prod_list)
                prod_cant = len(prod_list)
                end = start + limit
                if end >= prod_cant:
                    end = prod_cant
                if start >= prod_cant:
                    prods = []
                else:
                    prods = map(self._prodDict, prod_list[start:end])
                res[b'count'] = len(prods)
                res[b'total'] = prod_cant
                res[b'data'] = prods

    def post(self, *args, **kwargs):
        """inserts or modify element"""
        row = -1
        with JsonWriter(self) as (res):
            with _db.DB.threaded() as (root):
                user = self.get_current_user(root)
                code = self.get_argument(b'code', b'').strip()
                old_code = self.get_argument(b'old_code', b'').strip()
                if code == b'':
                    raise Exception(b'El código no puede estar vacio')
                if old_code == b'' or old_code not in root[b'products']:
                    prod = _db.models.Product(code)
                else:
                    prod = root[b'products'][old_code]
                prod.setName(self.get_argument(b'name', b''))
                prod.price = float(self.get_argument(b'price', 0.0))
                nstock = float(self.get_argument(b'stock', 0.0))
                if nstock != prod.stock:
                    move = _db.models.Move(prod, b'Modificado con Banta Touch Control', nstock - prod.stock, root=root)
                prod.stock = nstock
                if code != old_code:
                    if code in root[b'products']:
                        raise Exception(b'El código ya existe')
                    if old_code in root[b'products']:
                        del root[b'products'][old_code]
                prod.code = code
                root[b'products'][code] = prod
                row = list(root[b'products'].keys()).index(code)
                res[b'data'] = [self._prodDict(prod)]
            self.changed.emit(row)

    def delete(self, *args, **kwargs):
        row = -1
        with JsonWriter(self) as (res):
            code = self.get_argument(b'code')
            with _db.DB.threaded() as (root):
                user = self.get_current_user(root)
                if code not in root[b'products']:
                    raise Exception(b'No existe el producto.')
                row = list(root[b'products'].keys()).index(code)
            res[b'code'] = code
            self.deleteProduct.emit(row)


class Reports(BasicAuthHandler):

    def get(self, *args, **kwargs):
        with JsonWriter(self) as (res):
            report_type = self.get_argument(b'type', b'product')
            rep_mod = _pack.optional.reports
            reports = {b'product': rep_mod.reportProduct, 
               b'category': rep_mod.reportCategory, 
               b'user': rep_mod.reportUser, 
               b'client': rep_mod.reportClient, 
               b'move': rep_mod.reportMove, 
               b'buy': rep_mod.reportBuy}
            start, today, end = map(_utils.dateTimeToInt, _utils.currentMonthDates())
            gen_report = reports[report_type]
            with _db.DB.threaded() as (root):
                user = self.get_current_user(root)
                results = gen_report((start, end), root)
                heads = results.pop(b'_headers')
                res[b'headers'] = heads
                res[b'idx_tag'] = results.pop(b'_idx_tag')
                res[b'idx_val'] = results.pop(b'_idx_val')
                l_results = [ i.toStringList() for i in sorted(results.values(), reverse=True) ]
                res[b'data'] = l_results
                res[b'count'] = len(l_results)


class Server(_qc.QThread):
    gotIP = _qc.Signal(str)

    def __init__(self, parent):
        _qc.QThread.__init__(self)
        self.parent = parent
        self.lbs = self.parent.app.window.lb_server
        self.blue = _qg.QPixmap(b':/same/SamegameCore/pics/blueStone.png')
        self.blue = self.blue.scaled(self.blue.size() / 2.0)
        self.red = _qg.QPixmap(b':/same/SamegameCore/pics/redStone.png')
        self.red = self.red.scaled(self.red.size() / 2.0)
        self.green = _qg.QPixmap(b':/same/SamegameCore/pics/greenStone.png')
        self.green = self.green.scaled(self.green.size() / 2.0)
        self.yellow = _qg.QPixmap(b':/same/SamegameCore/pics/yellowStone.png')
        self.yellow = self.yellow.scaled(self.yellow.size() / 2.0)
        self.pixs = [self.green, self.red, self.yellow, self.blue]
        self.timer = _qc.QTimer()
        self.timer.setInterval(500)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.blingOut)
        self.blingOut()
        self.gotIP.connect(self.showIP)

    @_qc.Slot(int)
    def syncDB(self, row):
        _db.DB.abort()
        _db.DB.cnx.sync()
        m = _pack.base.products.MODEL
        old = m.rowCount()
        m._setMaxRows()
        new = m.rowCount()
        start = m.index(row, 0)
        end = m.index(row + 1, m.columnCount())
        if old < new:
            m.beginInsertRows(_qc.QModelIndex(), old, old)
            m.endInsertRows()
        else:
            m.dataChanged.emit(start, end)

    @_qc.Slot(int)
    def deleteProduct(self, row):
        model = _pack.base.products.MODEL
        model.removeRows(row, 1)

    @_qc.Slot(int)
    def bling(self, activity=0):
        self.timer.stop()
        self.lbs.setPixmap(self.pixs[activity])
        self.timer.start()

    @_qc.Slot()
    def blingOut(self):
        self.lbs.setPixmap(self.blue)

    @_qc.Slot(str)
    def showIP(self, ip):
        self.lbs.setToolTip(b'IP: ' + ip)

    def _getIP(self):
        import socket
        n = b'No se pudo detectar'
        s = None
        try:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('google.com', 80))
                n = s.getsockname()[0]
            except Exception as e:
                logger.exception(b'Error when trying to get the local ip: ' + unicode(e))

        finally:
            if s:
                s.close()

        try:
            if not n:
                ips = [ ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith(b'127.') ]
                ips = ips[:1]
                if ips:
                    n = ips[0]
        except Exception as e:
            logger.exception(b'Error when trying to get the local ip 2: ' + unicode(e))

        return n

    def run(self, *args, **kwargs):
        ip = self._getIP()
        self.gotIP.emit(ip)
        pth = os.getcwd()
        pth = os.path.join(pth, b'static')
        application = tornado.web.Application([
         (
          b'/prods(.*)', HProducts, {b'server_thread': self}),
         (
          b'/reports(.*)', Reports, {b'server_thread': self}),
         (
          b'/prod_img(.*)', ProdImg, {b'server_thread': self})], gzip=True, static_path=pth)
        application.listen(_db.CONF.WEBSERVICE_PORT, b'0.0.0.0')
        tornado.ioloop.IOLoop.instance().start()


class WebService(_pack.GenericModule):
    REQUIRES = []
    NAME = b'webservice'

    def load(self):
        self.server = Server(self)
        self.server.start()