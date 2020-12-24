# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alec/workspace/khan/khan/deploy/zcml.py
# Compiled at: 2010-05-12 10:25:54
from __future__ import absolute_import
import logging
from zope.schema import TextLine, Int, List as ZopeSchemaList
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.config import GroupingContextDecorator, IConfigurationContext
from zope.interface import Interface, implements, implementedBy, providedBy
from zope.component import queryUtility, getSiteManager
logger = logging.getLogger(__name__)

class IUtilityDirective(Interface):
    """Register a utility."""
    component = GlobalObject(title='Component to use', description='Python name of the implementation object.  This must identify an object in a module using the full dotted name.  If specified, the ``factory`` field must be left blank.', required=False)
    factory = GlobalObject(title='Factory', description='Python name of a factory which can create the implementation object.  This must identify an object in a module using the full dotted name. If specified, the ``component`` field must be left blank.', required=False)
    provides = GlobalInterface(title='Provided interface', description='Interface provided by the utility.', required=False)
    name = TextLine(title='Name', description='Name of the registration.  This is used by application code when locating a utility.', required=False)
    maker = GlobalObject(title='maker', required=False)


class UtilityDirectiveDefinition(GroupingContextDecorator):
    """ 
    Handle ``utility`` ZCML directives
    """
    implements(IConfigurationContext, IUtilityDirective)

    def __init__(self, context, provides=None, component=None, factory=None, maker=None, name=''):
        self.context = context
        self.name = name
        self.component = component
        self.factory = factory
        self.provides = provides
        self.params = {}
        self.maker = maker

    def param(self, context, name):
        u"""
        app 参数
        """
        self.params[name] = var_substitute(self.context, context.info.text)

    def __call__(self):
        if self.factory and self.component:
            raise TypeError("Can't specify factory and component.")
        if self.provides is None:
            if self.factory:
                provides = list(implementedBy(self.factory))
            else:
                provides = list(providedBy(self.component))
            if len(provides) == 1:
                provides = provides[0]
            else:
                raise TypeError("Missing 'provides' attribute")
        else:
            provides = self.provides
        params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
        factory = self.factory
        if self.maker and not self.factory:
            factory = lambda : self.maker(self.context.global_conf, **params)
        elif self.factory and not self.maker:
            factory = lambda : self.factory(**params)
        site_mngr = getSiteManager()
        site_mngr.registerUtility(self.component, self.provides, self.name, factory=factory)
        return


class List(ZopeSchemaList):
    """
    继承自zope.schema.list，实现fromUnicode函数
    """

    def __init__(self, **keyword):
        super(List, self).__init__(**keyword)

    def _validate(self, value):
        try:
            value.split(' ')
            return True
        except:
            return False

    def fromUnicode(self, input):
        self.validate(input)
        return input.split(' ')


def var_substitute(context, text):
    vars_factory = queryUtility(IDefaultVarFactory, context.name)
    if not vars_factory:
        return text
    try:
        return text % vars_factory
    except:
        return text


class IDefaultVarFactory(Interface):

    def update(self, vars):
        pass

    def __getitem__(self, key):
        pass


class IDefaultVarSubDirective(Interface):
    name = TextLine(title='var name', required=True)


class IDefaultDirective(Interface):
    pass


class DefaultDirectiveDefinition(GroupingContextDecorator):
    implements(IConfigurationContext, IDefaultDirective)

    def __init__(self, context):
        self.context = context
        self.vars = {}

    def var(self, context, name):
        self.vars[name] = context.info.text

    def __call__(self):
        vars_factory = queryUtility(IDefaultVarFactory, self.context.name)
        if vars_factory is None:
            return
        else:
            vars_factory.update(self.vars)
            return


class IAppFactory(Interface):

    def __setitem__(self, name, val):
        pass


class ICompositeFactory(Interface):

    def __setitem__(self, name, val):
        pass


class IMiddlewareFactory(Interface):

    def __setitem__(self, name, val):
        pass


class IObjectFactory(Interface):

    def __setitem__(self, name, val):
        pass


class IServerFactory(Interface):

    def __setitem__(self, name, val):
        pass


class IDeploymentDirective(Interface):
    pass


class DeploymentDirectiveDefinition(GroupingContextDecorator):
    implements(IConfigurationContext, IDeploymentDirective)


class IParamSubDirective(Interface):
    name = TextLine(title='param value name', required=True)


class IAppDirective(Interface):
    name = TextLine(title='name', required=True)
    handler = GlobalObject(title='handler', required=False)
    factory = GlobalObject(title='factory', required=False)
    use = TextLine(title='use', required=False)
    maker = GlobalObject(title='maker', required=False)
    filter = TextLine(title='filter', required=False)


class AppDirectiveDefinition(GroupingContextDecorator):
    """ 
    Handle ``app`` ZCML directives
    """
    implements(IConfigurationContext, IAppDirective)

    def __init__(self, context, name, handler=None, factory=None, use=None, maker=None, filter=None):
        self.context = context
        self.name = name
        self.handler = handler
        self.factory = factory
        self.maker = maker
        self.use = use
        self.filter = filter
        self.params = {}

    def param(self, context, name):
        u"""
        app 参数
        """
        self.params[name] = var_substitute(self.context, context.info.text)

    def __call__(self):
        afactory = queryUtility(IAppFactory, self.context.name)
        if afactory is None:
            return
        else:
            if self.handler:
                handler = self.handler
                maker = lambda global_conf, *args, **kargs: handler
            elif self.factory:
                factory = self.factory
                maker = lambda global_conf, *args, **kargs: factory(*args, **kargs)
            elif self.use:
                maker = self.use
            elif self.maker:
                maker = self.maker
            else:
                raise ConfigurationError('One of the `factory` and `handler` and `use` and `maker` attribute must be specified.')
            params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
            afactory[self.name] = {'use': maker, 'params': params, 'filter': self.filter}
            return


class ICompositeDirective(Interface):
    name = TextLine(title='name', required=True)
    handler = GlobalObject(title='handler', required=False)
    factory = GlobalObject(title='factory', required=False)
    maker = GlobalObject(title='maker', required=False)
    use = TextLine(title='use', required=False)
    filter = TextLine(title='filter', required=False)


class CompositeDirectiveDefinition(GroupingContextDecorator):
    """ 
    Handle ``composite`` ZCML directives
    """
    implements(IConfigurationContext, ICompositeDirective)

    def __init__(self, context, name, handler=None, factory=None, use=None, maker=None, filter=None):
        self.context = context
        self.name = name
        self.handler = handler
        self.factory = factory
        self.maker = maker
        self.use = use
        self.filter = filter
        self.params = {}

    def param(self, context, name):
        u"""
        app 参数
        """
        self.params[name] = var_substitute(self.context, context.info.text)

    def __call__(self):
        cfactory = queryUtility(ICompositeFactory, self.context.name)
        if cfactory is None:
            return
        else:
            if self.handler:
                handler = self.handler
                maker = lambda global_conf, *args, **kargs: handler
            elif self.factory:
                factory = self.factory
                maker = lambda global_conf, *args, **kargs: factory(*args, **kargs)
            elif self.use:
                maker = self.use
            elif self.maker:
                maker = self.maker
            else:
                raise ConfigurationError('One of the `factory` and `handler` and `use` and `maker` attribute must be specified.')
            params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
            cfactory[self.name] = {'use': maker, 'params': params, 'filter': self.filter}
            return


class IMiddlewareDirective(Interface):
    name = TextLine(title='name', required=True)
    handler = GlobalObject(title='handler', required=False)
    factory = GlobalObject(title='factory', required=False)
    use = TextLine(title='use', required=False)
    maker = GlobalObject(title='maker', required=False)
    next = TextLine(title='next', required=False)


class MiddlewareDirectiveDefinition(GroupingContextDecorator):
    """ 
    Handle ``middleware`` ZCML directives
    """
    implements(IConfigurationContext, IMiddlewareDirective)

    def __init__(self, context, name, handler=None, factory=None, use=None, maker=None, next=None):
        self.context = context
        self.name = name
        self.handler = handler
        self.factory = factory
        self.maker = maker
        self.use = use
        self.next = next
        self.params = {}

    def param(self, context, name):
        u"""
        middleware 参数
        """
        self.params[name] = var_substitute(self.context, context.info.text)

    def __call__(self):
        mfactory = queryUtility(IMiddlewareFactory, self.context.name)
        if mfactory is None:
            return
        else:
            if self.handler:
                handler = self.handler
                maker = lambda global_conf, *args, **kargs: handler
            elif self.factory:
                factory = self.factory
                maker = lambda global_conf, *args, **kargs: factory(*args, **kargs)
            elif self.use:
                maker = self.use
            elif self.maker:
                maker = self.maker
            else:
                raise ConfigurationError('One of the `factory` and `handler` and `use` and `maker` attribute must be specified.')
            params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
            mfactory[self.name] = {'use': maker, 'params': params, 'next': self.next}
            return


class IObjectDirective(Interface):
    name = TextLine(title='name', required=True)
    handler = GlobalObject(title='handler', required=False)
    factory = GlobalObject(title='factory', required=False)
    use = TextLine(title='use', required=False)
    maker = GlobalObject(title='maker', required=False)


class ObjectDirectiveDefinition(GroupingContextDecorator):
    """ 
    Handle ``object`` ZCML directives
    """
    implements(IConfigurationContext, IObjectDirective)

    def __init__(self, context, name, handler=None, factory=None, use=None, maker=None):
        self.context = context
        self.name = name
        self.handler = handler
        self.factory = factory
        self.maker = maker
        self.use = use
        self.params = {}

    def param(self, context, name):
        u"""
        object 参数
        """
        self.params[name] = var_substitute(self.context, context.info.text)

    def __call__(self):
        ofactory = queryUtility(IObjectFactory, self.context.name)
        if ofactory is None:
            return
        else:
            if self.handler:
                handler = self.handler
                maker = lambda global_conf, *args, **kargs: handler
            elif self.factory:
                factory = self.factory
                maker = lambda global_conf, *args, **kargs: factory(*args, **kargs)
            elif self.use:
                maker = self.use
            elif self.maker:
                maker = self.maker
            else:
                raise ConfigurationError('One of the `factory` and `handler` and `use` and `maker` attribute must be specified.')
            params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
            ofactory[self.name] = {'use': maker, 'params': params}
            return


class IServerDirective(Interface):
    """
    <server> interface
    """
    app = TextLine(title='app name', required=False)
    pipeline = List(title='apps pipe line', required=False, unique=True, value_type=TextLine(title='app name'))
    handler = GlobalObject(title='handler', required=False)
    factory = GlobalObject(title='factory', required=False)
    maker = GlobalObject(title='maker', required=False)
    use = TextLine(title='use object', required=False)
    name = TextLine(title='server alias name', required=False)


class ServerDirectiveDefinition(GroupingContextDecorator):
    """ 
    ZCML的server指令

    ... note:

       handler, factory, use, marker 有且仅有一个属性必须被设计

    """
    implements(IConfigurationContext, IServerDirective)

    def __init__(self, context, **keyword):
        if 'pipeline' in keyword and 'app' in keyword:
            raise ConfigurationError('only one: app, pipeline')
        elif 'pipeline' not in keyword and 'app' not in keyword:
            raise ConfigurationError('must one: app, pipeline')
        self.context = context
        self.params = {'host': '0.0.0.0', 
           'port': 7010}
        self.name = keyword.get('name', 'main')
        maker = None
        for i in ['handler', 'factory', 'use', 'maker']:
            if i in keyword:
                if maker is not None:
                    raise ConfigurationError('\n                     server only one:\n                     handler, factory, use, maker\n                     ')
                if i == 'factory':
                    params = dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))
                    maker = keyword.pop(i)(**params)
                else:
                    maker = keyword.pop(i)
                break

        if maker is None:
            raise ConfigurationError('server must one: handler, factory, use, maker')
        self.maker = maker
        self.config = keyword
        if 'pipeline' in keyword:
            self.config['app'] = keyword.get('pipeline')[0]
        return

    def param(self, context, name):
        self.params[name] = var_substitute(self.context, context.info.text.strip())

    def __call__(self):
        factory = queryUtility(IServerFactory, self.context.name)
        if factory is None:
            return
        else:
            try:
                factory[self.name] = {'entry_point': self.maker, 
                   'config': dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.config.items())), 
                   'params': dict(map(lambda x: (x[0].encode('utf-8'), x[1]), self.params.items()))}
            except:
                logger.error('server directive __call__ function failed', exc_info=True)

            return


class ILoggingDirective(Interface):
    """
    <logging> interface
    """
    keys = List(title='available loggers', required=False, unique=True, value_type=TextLine(title='available logger name'))
    level = TextLine(title='logger level', description='logging basic config level', required=False, default='INFO')


class ILoggingLoggerDirective(Interface):
    """
    <logger> interface
    """
    name = TextLine(title='name', description='logger name', required=True)
    handlers = List(title='logger use handlers', required=True, unique=True, value_type=TextLine(title='logger use handlers'))
    level = TextLine(title='logger level', description='logger level', required=False, default='INFO')
    propagate = Int(title='logger can be propagated', required=False, default=1)
    qualname = TextLine(title='logger level', description='logger level', required=False)


class ILoggingHandlerDirective(Interface):
    """
    <handler> interface
    """
    name = TextLine(title='name', description='logger handlername', required=True)
    cls = GlobalObject(title='logger handler class', required=True)
    formatter = TextLine(title='logger handler use formatter', required=True)
    args = TextLine(title='logger handler args', required=False, default='')
    level = TextLine(title='logger handler level', required=False, default='NOTSET')


class ILoggingFormatterDirective(Interface):
    """
    <formatter> interface
    """
    name = TextLine(title='name', description='logger handlername', required=True)
    cls = GlobalObject(title='logger handler class', required=False, default='logging.Formatter')
    args = TextLine(title='args of the fomatter class', required=False, default='')


class LoggingDirectiveDefinition(GroupingContextDecorator):
    implements(IConfigurationContext, ILoggingDirective)

    def __init__(self, context, keys=[], level='INFO'):
        if not keys:
            raise ConfigurationError('keys invalid')
        self.context = context
        self.available_loggers = keys
        self.level = level
        self.loggers = {}
        self.handlers = {}
        self.formatters = {}

    def logger(self, context, name, handlers, qualname=None, propagate=1, level='INFO'):
        if name in self.loggers:
            raise ConfigurationError('logger "%s" already exists' % name)
        self.loggers[name] = {'level': level, 
           'handlers': handlers, 
           'qualname': qualname, 
           'propagate': propagate}

    def handler(self, context, name, cls, formatter, args='', level='NOTSET'):
        if name in self.handlers:
            raise ConfigurationError('handler "%s" already exists' % name)
        self.handlers[name] = {'cls': cls, 
           'formatter': formatter, 
           'args': args, 
           'level': level}

    def formatter(self, context, name, cls, args=''):
        if name in self.formatters:
            raise ConfigurationError('formatter "%s" already exists' % name)
        self.formatters[name] = {'cls': cls, 
           'args': args}

    def __call__(self):
        lobj = queryUtility(ILoggingObject)
        if lobj is None:
            return
        else:
            lobj.loggers.update(self.loggers)
            lobj.handlers.update(self.handlers)
            lobj.formatters.update(self.formatters)
            lobj.available_loggers = self.available_loggers
            lobj.level = self.level
            return


class ILoggingObject(Interface):
    pass