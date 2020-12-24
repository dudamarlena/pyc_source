# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/domain.py
# Compiled at: 2009-01-30 08:10:10
"""
Реализация основных классов доменов.
"""
import hashlib
from zope.interface import implements
from twisted.internet import defer
from spamfighter.interfaces import IDomain, IDomainBindable
from spamfighter.plugin import loadPlugin, IDefaultDomainProvider
from spamfighter.utils import config

class DomainKeyError(Exception):
    """
    В данном домене нет указанного значения.
    """
    pass


class DomainPathError(Exception):
    """
    Указанный путь в поддоменах отсутствует.
    """
    pass


class DomainDuplicateError(Exception):
    """
    У данного домена уже есть поддомен с таким же именем.
    """
    pass


class BaseDomain(object):
    """
    Домен - единица настроек, привязки локальных элементов 
    внутренного устройства СпамоБорца. 
    
    Все домены связаны в дерево, начинающееся главным доменом 
    (глобально известным серверу).

    Базовый класс доменов представляет домены "в памяти", без какого-либо 
    сохранения, а также без "детей".

    @ivar _name: имя домена
    @type _name: C{str}
    @ivar _key: ключ домена
    @type _key: C{str}
    @ivar _parent: предок данного домена
    @type _parent: L{IDomain}
    @ivar _dict: хеш (словарь) атрибутов, заданных в данном домене
    @type _dict: C{dict}
    @ivar _children: хэш поддоменов по их именам
    @type _children: C{dict}
    """
    implements(IDomain)

    def __init__(self, key=None, name=None, parent=None, dict=None):
        u"""
        Конструктор.

        @param parent: предок текущего домена
        @type parent: L{IDomain}
        @param dict: начальное значение домена
        @type dict: C{dict}
        """
        assert key is not None or name is not None and parent is not None
        self._parent = parent
        if key is not None:
            self._key = key
        else:
            self._key = hashlib.md5(self._parent.key() + name).hexdigest()
        self._name = name
        self._children = {}
        self._dict = {}
        if dict is not None:
            self._dict = dict.copy()
            for (property, value) in self._dict.iteritems():
                if IDomainBindable.providedBy(value):
                    value.bind(self, property)

        return

    def name(self):
        u"""
        Имя домена (относительно пути).

        Если домен корневой или не содержится в пути,
        имя может быть C{None}.

        @return: имя домена
        @rtype: C{str}
        """
        return self._name

    def key(self):
        u"""
        Ключ домена. Уникальное и постоянное свойство
        каждого домена.

        @return: ключ домена
        @rtype: C{str}
        """
        return self._key

    def parent(self):
        u"""
        Получить предка данного домена.

        Если предка нет, будет возвращено C{None}.

        @rtype: L{IDomain}
        """
        return self._parent

    def children(self):
        u"""
        Получить список "дочерних" доменов.

        @return: Deferred, результат - хэш (имя домена: домен) (C{dict(}L{IDomain}C{)})
        @rtype: C{twisted.internet.defer.Deferred}
        """
        return defer.succeed(self._children)

    def createSubdomain(self, name):
        u"""
        Создать дочерний поддомен.

        @param name: имя поддомена
        @type name: C{str}
        @return: Deferred с созданным поддоменом, L{IDomain}
        @rtype: C{twisted.internet.defer.Deferred}
        @raise DomainDuplicateError: два поддомена с одинаковым именем не могут существовать
        """
        if name in self._children:
            return defer.fail(DomainDuplicateError(name))
        domain = BaseDomain(parent=self, name=name)
        self._children[name] = domain
        return defer.succeed(domain)

    def walk(self, path):
        u"""
        "Пройти" по пути от текущего домена.

        @param path: путь относительно текущего домена, строка со слэшами
        @type path: C{str}
        @return: Deferred, найденный домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred}
        @raise DomainPathError: домен не найден
        """

        def _walk(domain, components):
            if len(components) == 0:
                return defer.succeed(domain)
            component = components.pop(0)
            if component == '':
                return _walk(domain, components)

            def gotChildren(children):
                if not children.has_key(component):
                    raise DomainPathError, path
                return _walk(children[component], components)

            return domain.children().addCallback(gotChildren)

        components = path.split('/')
        return _walk(self, components)

    def get(self, property):
        u"""
        Получить значение свойства домена.

        Если текущий домен не содержит информацию о данном свойстве, будет
        предпринято обращение к предку домена за данным свойством.

        @param property: имя свойства
        @type property: C{str}
        @return: значение свойства
        """
        if self._dict.has_key(property):
            return self._dict[property]
        else:
            if self._parent is not None:
                return self._parent.get(property)
            raise DomainKeyError, property
            return

    def has(self, property):
        u"""
        Есть ли у домена указанное свойство?

        @param property: имя свойства
        @type property: C{str}
        @rtype: C{bool}
        """
        return property in self._dict

    def delete(self, property):
        u"""
        Удалить свойство из домена.

        При следующем обращении к свойству оно будет получено через предка домена,
        т.е. это эквивалентно сбросу на "значение по умолчанию".

        @param property: имя свойства
        @type property: C{str}
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """
        if self._dict.has_key(property):
            del self._dict[property]
        return defer.succeed(None)

    def set(self, property, value):
        u"""
        Установить значение свойства в домене.

        Данный метод может также создать свойство, если оно ранее не существовало 
        и переопределить свойство домена-предка.

        @param property: имя свойства
        @type property: C{str}
        @param value: значение свойства
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """
        try:
            if IDomainBindable.providedBy(value):
                value.bind(self, property)
            self._dict[property] = value
        except:
            return defer.fail()

        return defer.succeed(None)

    def list(self):
        u"""
        Получить список имён свойств домена.

        @return: список имён свойств
        @rtype: C{list(str)}
        """
        return self._dict.keys()


def getDefaultDomain():
    u"""
    Получить домен по умолчанию, который является предком всех доменов.

    Получаем через провайдер домена по умолчанию.

    @return: домен по умолчанию
    @rtype: L{IDomain}
    """
    return getDefaultDomainProvider().getDefaultDomain()


defaultDomainProvider = None

def getDefaultDomainProvider():
    u"""
    Получить провайдер домена по умолчанию.

    Загружаем как плагин, предсоставляющий интерфейс L{IDefaultDomainProvider} с именем 
    из конфига: config.plugins.domain.default_provider

    @return: провайдер домена по умолчанию
    @rtype: L{IDefaultDomainProvider}
    """
    global defaultDomainProvider
    if defaultDomainProvider is None:
        defaultDomainProvider = loadPlugin(IDefaultDomainProvider, config.plugins.domain.default_provider)
    return defaultDomainProvider