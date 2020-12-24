# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qtrequests/qtr.py
# Compiled at: 2014-06-18 15:46:22
from PySide import QtCore
from PySide import QtNetwork

class QClient(QtCore.QObject):
    """ Esta clase realiza las peticiones a servidores HTTP
    
    Ejemplo de uso:
    
        >>> from qtr import QClient
        >>> from PySide import QtGui
        >>> QtGui.QApplication([])
        >>> client = QClient()
        >>> client.addstep_seturl("http://www.gnu.org")
        >>> client.addstep_setscraper(scraper)
        >>> client.do()
        >>> results = client.getinternaldata()
    
    Revise la documentación para descubrir que otros pasos más tiene disponible.
    """
    nextstep = QtCore.Signal()
    finished = QtCore.Signal()
    abortexecution = QtCore.Signal(str, int)
    accumulate = QtCore.Signal()

    def __init__(self, qnamattr=None, parent=None):
        super(QClient, self).__init__(parent=parent)
        self.__stack = []
        self._url = QtCore.QUrl()
        self.__stepindex = None
        self.__request = QtNetwork.QNetworkRequest(self._url)
        self.__request.setOriginatingObject(self)
        self.___reply = None
        self.__data = QtCore.QByteArray()
        self.__internaldata = None
        self.__accumdata = []
        self._eventloop = QtCore.QEventLoop()
        self._finished = False
        if not parent:
            self.__qnm = QtNetwork.QNetworkAccessManager(self)
        else:
            self.__qnm = getattr(self.parent(), qnamattr)
        self.nextstep.connect(self.step)
        self.__qnm.finished[QtNetwork.QNetworkReply].connect(self._endrequest)
        self.abortexecution.connect(self.abort)
        self.accumulate.connect(self._accumulatedata)
        return

    def __add_step(self, **kwords):
        u""" Método de bajo nivel que añade pasos dentro de la pila de pasos
        
        :param dict kwords: debe contener al menos el la llave ``method``,        puede ser una cadena o un método o función de Python. Actualmente        la única cadena que tiene significado para este método es ``get``,        el verbo para hacer peticiones a servidores web.
        """
        if 'method' in kwords:
            method = kwords.get('method')
            if isinstance(method, str):
                if method == 'get':
                    kwords['verb'] = 'get'
                kwords['method'] = self._executerequest
            self.__stack.append(kwords)
        else:
            self.abortexecution.emit("No 'method' argument was giving!", 1)

    def _seturl(self, **kwords):
        u""" Método privado que estable la URL
        
        :param dict kwords: debe contener las llaves ``fromscraped``,        ``url`` y ``query``.
        :keyword bool fromscraped: indica si la URL a establecer se        encuentra en el almacenamiento interno        :attr:`qtr.QClient.__internaldata`.
        :keyword str url: La URL a usar.
        :keyword dict query: los *queries* a establecer en la URL.
        """
        fromscraped = kwords.get('fromscraped')
        if fromscraped:
            url = self.__internaldata
        else:
            url = kwords.get('url')
        query = kwords.get('query')
        if not url:
            self.abortexecution.emit('Setting empty urls is bad idea!', 1)
            return
        self._url.setUrl(url)
        if not self._url.isValid():
            self.abortexecution.emit(('This url "{}" is not valid!').format(url), 1)
            return
        if query:
            for key in query.keys():
                self._url.removeQueryItem(key)

            for key, value in query.iteritems():
                self._url.addQueryItem(key, value)

    def _executerequest(self, **kwords):
        u""" Ejecuta la petición al servidor web.
        
        :param dict kwords: debe contener la llave ``verb``        que indica el verbo HTTP que se usara para la        petición. Este método usa :attr:`qtr.QClient.__request`        previamente modificado para realizar la petición.
        
        Si la instancia QClient es hija de un objeto QtObject, establece
        como origen de la petición a sí misma.
        """
        self.__request.setUrl(self._url)
        if self.parent():
            self.__request.setOriginatingObject(self)
        if 'verb' not in kwords:
            self.abortexecution.emit('there is no HTTP verb in the arguments', 1)
            return
        verb = getattr(self.__qnm, kwords.get('verb'))
        verb(self.__request)

    def __execute_step(self):
        u""" Ejecuta el paso actual directamente de la pila
        
        cada paso debe contener la llave ``method``. Este método busca también
        por los siguientes llaves:
        
        :keyword bool block: indica si este paso bloquea el flujo de ejecución        hasta que algo le indique terminar. ``False`` por defecto.
        :keyword bool store: indica que lo devuelto por este paso, debe ser        almacenado en ``__internaldata``. ``False`` por defecto.
        :keyword bool isScrap: indica que este paso es un raspador. ``False``        por defecto.
        :keyword tuple args: indica que el paso contiene una llave con        una tupla dentro. ``tuple()`` por defecto.
        :keyword bool passargs: indica que hay que pasar ``args`` a        ``method``. ``False`` por defecto.
        :keyword bool passkwords: indica que hay que pasar ``step`` a        ``method``. ``True`` por defecto.
        :keyword bool passselfattribute: indica que hay que pasar un atributo        de la instancia del objeto ``QClient``. ``False`` por defecto.
        :keyword str selfattributename: indica el nombre del atributo de la        instancia del objeto ``QClient``. ``None`` por defecto.
        :keyword classmethod selfattribute: contiene el atributo tomado de la        instancia del objeto ``QClient``. No existe si        ``passselfattribute`` es ``False``
        :keyword bool selfattributeismethod: indica que el atributo no es        un atributo, sino un método que retorna algo. ``False`` por defecto.
        """
        if self.__stepindex + 1 > len(self.__stack):
            return True
        else:
            index = self.__stepindex
            step = self.__stack[index]
            method = step.get('method')
            block = step.get('block', False)
            store = step.get('store', False)
            stepisscrap = step.get('isScrap', False)
            args = step.get('args', tuple())
            passargs = step.get('passargs', False)
            passkwords = step.get('passkwords', True)
            passselfattribute = step.get('passselfattribute', False)
            selfattributename = step.get('selfattribute', None)
            if passselfattribute:
                selfattribute = getattr(self, selfattributename)
            selfattributeismethod = step.get('selfattributeibuteismethod', False)
            if passkwords:
                tmpinternaldata = method(**step)
            elif passargs:
                tmpinternaldata = method(*args)
            elif passargs and passkwords:
                tmpinternaldata = method(*args, **step)
            elif passselfattribute:
                if selfattributeismethod:
                    tmpinternaldata = method(selfattribute())
                else:
                    tmpinternaldata = method(selfattribute)
            elif stepisscrap:
                tmpinternaldata = method(self.__data.data())
            else:
                tmpinternaldata = method()
            if store or stepisscrap:
                self.__internaldata = tmpinternaldata
            if block:
                self._eventloop.exec_()
            self.__stepindex += 1
            return

    @QtCore.Slot()
    def getinternaldata(self, accumulated=False):
        """ Retorna los datos internos.
        
        :param bool accumulated: si es ``True``, retorna los datos        acumulados internos en vez de los internos.
        :return: una cadena, o una lista.
        """
        if accumulated:
            return self.__accumdata
        else:
            return self.__internaldata

    @QtCore.Slot(str, int)
    def abort(self, message, exception):
        u""" Aborta la ejecución de la secuencia de ordenes.
        """
        self._finished = True
        self.finished.emit()
        QtCore.QTimer.singleShot(5000, self._eventloop.quit)
        if exception == 1:
            raise RuntimeError(message)

    @QtCore.Slot(QtNetwork.QNetworkReply)
    def _endrequest(self, reply):
        u""" Almacena los datos devueltos por el servidor web.
        
        Este método hace que el loop de eventos se rompa y el flujo
        de la ejecución pueda continuar.
        """
        if self.parent() is None or self.parent() and reply.request().originatingObject() == self:
            self.__data = reply.readAll()
            self.__reply = reply
            if self._eventloop.isRunning():
                self._eventloop.quit()
        return

    @QtCore.Slot()
    def _accumulatedata(self):
        """ Acumula los datos para guardarlos de forma segura y evitar
        que sean sobre-escritos.
        """
        self.__accumdata.extend(self.__internaldata)

    def do(self):
        """ Inicia la secuencia de ordenes pre-programadas.
        """
        self.nextstep.emit()

    def step(self):
        u""" Emite una señal para que se ejecute un paso.
        Este método es llamado de forma recursiva hasta que
        se alcanza el final de la pila.
        """
        if self.__stepindex is None:
            self.__stepindex = 0
        self._finished = self.__execute_step()
        if not self._finished:
            self.nextstep.emit()
        else:
            self.finished.emit()
        return

    def addstep_seturl(self, url, query={}):
        u""" Establecerá la URL sobre la cual realizar la petición web.
        
        Se debe usar este método antes que
        :meth:`qtr.QClient.addstep_setrequest`.
        """
        if url is None or url == '':
            fromscraped = True
        else:
            fromscraped = False
        self.__add_step(method=self.__data.clear, passkwords=False)
        self.__add_step(method=self._seturl, url=url, fromscraped=fromscraped, query=query)
        return

    def addstep_setrequest(self, verb):
        u""" Establecerá el verbo de la petición web
        """
        self.__add_step(method=verb, block=True)

    def addstep_setscraper(self, method):
        u""" Establece el método que raspara el contenido web
        """
        self.__add_step(method=method, isScrap=True, store=True, passkwords=False)

    def addstep_setscraperpageurls(self, method, perpagescraper):
        u""" Establece el raspador que extraerá la lista de URLs en una lista
        y la función que repasara cada enlace raspando su contenido.
        
        :param classmethod method: el raspador de URLs.
        :param classmethod perpagescraper: el raspador que raspa el        contenido de cada URL
        """
        self.__add_step(method=method, isScrap=True, store=True, passkwords=False)
        self.__add_step(method=self._setpagescraper, scraper=perpagescraper)

    def _setpagescraper(self, **kwords):
        u""" Establece el raspador que raspara el contenido de cada enlace
        
        Este método es usado por :meth:`qtr.QClient.addstep_setscraperpageurls`
        y no hay razón para usarlo directamente.
        """
        scraper = kwords.get('scraper')
        for link in self.__internaldata:
            self.addstep_seturl(url=link)
            self.addstep_setrequest('get')
            self.addstep_setscraper(scraper)
            self.__add_step(method=self.accumulate.emit, passkwords=False)

    def status(self):
        u""" Retorna el código HTTP de la petición realizada
        
        :return: código HTTP
        :rtype: int
        """
        return self.__reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)

    def error(self):
        u""" Retorna el código de error de la petición realizada
        
        :return: código de error
        :rtype: int
        """
        return self.__reply.error()

    def geturl(self):
        """ Retorna la URL actual
        
        :return: url
        :rtype: unicode
        """
        self._url.toString()