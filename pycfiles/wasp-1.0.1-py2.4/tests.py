# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wasp/tests.py
# Compiled at: 2008-09-17 11:14:28
import os.path
from StringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite
from wasp import Message, Notification, Receiver
from wasp import send
from wasp.interfaces import ISendMessage, IProcessResponse, INotifyMessage, IReceiveMessage
from zope.app.appsetup.appsetup import getConfigContext
from zope.app.testing.functional import ZCMLLayer
from zope.app.testing.functional import FunctionalDocFileSuite
from zope.component import provideAdapter, provideUtility, ComponentLookupError
from zope.component.testing import tearDown as componentTearDown
from zope.configuration import xmlconfig
from zope.interface.verify import verifyObject
from zope.testbrowser.testing import Browser
from zope.testing import doctest

class BaseSendTests(TestCase):
    __module__ = __name__
    klass = None
    response = True

    def setUp(self):
        self.u = self.klass()

    def test_interface(self):
        verifyObject(ISendMessage, self.u)

    def test_send(self):
        self.assertEqual(self.u('123', 'test message', '456'), self.response)

    def test_send_no_id(self):
        self.assertEqual(self.u('123', 'test message'), self.response)


class BaseProcessResponse(TestCase):
    __module__ = __name__
    klass = None

    def setUp(self):
        self.u = self.klass()

    def cmp(self, actual, expected, u=None):
        actual = tuple(actual)
        self.assertEqual(len(expected), len(actual), 'Expected %i results, %i returned' % (len(expected), len(actual)))
        problems = []
        for (a, e) in zip(actual, expected):
            if a.__class__ is not e.__class__:
                problems.append('%r != %r' % (a.__class__, e.__class__))
                continue
            if a.__dict__ != e.__dict__:
                problems.append('%r != %r' % (a.__dict__, e.__dict__))

        if problems:
            self.fail('actual != expected:\n' + ('\n').join(problems))

    def test_interface(self):
        verifyObject(IProcessResponse, self.u)

    def test_message(self):
        raise NotImplementedError

    def test_notification(self):
        raise NotImplementedError


def test_import():
    """
    Mainly just as an example of a doc test ;-)
    
    >>> from wasp import send,Receiver,Message,Notification

    There's also a handy exception to raise when `wasp.send` fails:

    >>> from wasp import SendException
    >>> issubclass(SendException,Exception)
    True
    """
    pass


class Tests(TestCase):
    __module__ = __name__

    def test_statuses(self):
        import wasp.status
        for name in wasp.status.__dict__:
            i = name[0]
            if i == '_':
                continue
            obj = getattr(wasp.status, name)
            if i.isupper():
                self.failUnless(issubclass(obj, wasp.status.Status))
            else:
                self.failUnless(isinstance(obj, wasp.status.Status))

    def test_message_interface(self):
        self.failUnless(Message.interface is IReceiveMessage)

    def test_message_normal(self):
        m = Message('123', 'some text')
        self.assertEqual((m.msisdn, m.message_text), ('123', 'some text'))

    def test_message_keyword(self):
        m = Message(message_text='some text', msisdn='123')
        self.assertEqual((m.msisdn, m.message_text), ('123', 'some text'))

    def test_message_typerror(self):
        self.assertRaises(TypeError, Message, '123')
        self.assertRaises(TypeError, Message, '123', x='some text')

    def test_notification_interface(self):
        self.failUnless(Notification.interface is INotifyMessage)

    def test_notification_normal(self):
        from wasp.status import delivered
        n = Notification('123', delivered, '')
        self.assertEqual((n.message_id, n.status, n.details), ('123', delivered, ''))

    def test_notification_keyword(self):
        from wasp.status import failed
        n = Notification(details='something bad happened', message_id='123', status=failed)
        self.assertEqual((n.message_id, n.status, n.details), (
         '123', failed, 'something bad happened'))

    def test_notification_typerror(self):
        self.assertRaises(TypeError, Notification, '123')
        self.assertRaises(TypeError, Notification, '123', x='some text')


marker = object()

class TestSendUtility:
    __module__ = __name__

    def __call__(self, msisdn, message_text, message_id):
        self.msisdn = msisdn
        self.message_text = message_text
        self.message_id = message_id
        return marker


class SendTests(TestCase):
    __module__ = __name__

    def setUp(self):
        self.u = TestSendUtility()
        provideUtility(self.u, ISendMessage)

    tearDown = componentTearDown

    def test_send_no_utility(self):
        componentTearDown()
        self.assertRaises(ComponentLookupError, send, '123', 'message', 'xyz')

    def test_send(self):
        self.failUnless(send('123', 'message', 'xyz') is marker)
        self.assertEqual(self.u.msisdn, '123')
        self.assertEqual(self.u.message_text, 'message')
        self.assertEqual(self.u.message_id, 'xyz')

    def test_send_no_message_id(self):
        self.failUnless(send('123', 'message') is marker)
        self.assertEqual(self.u.msisdn, '123')
        self.assertEqual(self.u.message_text, 'message')
        self.assertEqual(self.u.message_id, None)
        return


class Request(dict):
    __module__ = __name__

    def __init__(self, body=None, form=None, zope=0):
        dict.__init__(self)
        if form is not None:
            self.update(form)
        self.body = body
        self.zope = zope
        if body and zope == 2:
            self['BODY'] = body
        return

    @property
    def bodyStream(self):
        if self.zope == 2:
            raise AttributeError
        return StringIO(self.body or '')

    @property
    def form(self):
        return self


class TestProcessUtility:
    __module__ = __name__

    def __init__(self, notify=None):
        self.notify = notify

    def process(self, request, form, body):
        self.request = request
        self.form = form
        self.body = body
        if self.notify:
            yield self.notify

    def response(self):
        return 'done!'


class ReceiverIProcessReponseTests(TestCase):
    __module__ = __name__

    def setUp(self):
        self.u = TestProcessUtility()
        provideUtility(self.u, IProcessResponse)

    tearDown = componentTearDown

    def test_receiver_noutility(self):
        componentTearDown()
        self.assertRaises(ComponentLookupError, Receiver(object(), Request()))

    def test_Receiver_form(self):
        form = {'x': 1, 'y': '2'}
        r = Request(form=form)
        self.assertEqual(Receiver(object(), r)(), 'done!')
        self.failUnless(self.u.request is r)
        self.assertEqual(self.u.form, form)
        self.assertEqual(self.u.body, '')

    def test_Receiver_Zope3_body(self):
        r = Request(body='test', zope=3)
        self.assertEqual(Receiver(object(), r)(), 'done!')
        self.failUnless(self.u.request is r)
        self.assertEqual(self.u.form, {})
        self.assertEqual(self.u.body, 'test')

    def test_Receiver_Zope2_body(self):
        r = Request(body='test', zope=2)
        self.assertEqual(Receiver(object(), r)(), 'done!')
        self.failUnless(self.u.request is r)
        self.assertEqual(self.u.form, {'BODY': 'test'})
        self.assertEqual(self.u.body, 'test')


class Context:
    __module__ = __name__


class ReceiverAdapterUtilityTests(TestCase):
    __module__ = __name__

    def setUp(self):
        provideUtility(TestProcessUtility(Message('123', 'message')), IProcessResponse)

    tearDown = componentTearDown
    interface = IReceiveMessage
    expected = {'msisdn': '123', 'message_text': 'message'}

    def test_nothing(self):
        self.assertRaises(ComponentLookupError, Receiver(object(), Request()))

    def test_adapter(self):

        class Adapter:
            __module__ = __name__

            def __init__(self, context):
                Adapter.context = context

            @classmethod
            def __call__(cls, **kw):
                cls.params = kw

        provideAdapter(Adapter, adapts=(Context,), provides=self.interface)
        c = Context()
        Receiver(c, Request())()
        self.assertEqual(Adapter.params, self.expected)
        self.failUnless(Adapter.context is c)

    def test_utility(self):

        class Utility:
            __module__ = __name__

            def __call__(self, **kw):
                self.params = kw

        u = Utility()
        provideUtility(u, self.interface)
        Receiver(None, Request())()
        self.assertEqual(u.params, self.expected)
        return

    def test_both(self):

        class Adapter:
            __module__ = __name__

            def __init__(self, context):
                Adapter.context = context

            @classmethod
            def __call__(cls, **kw):
                cls.params = kw

        provideAdapter(Adapter, adapts=(Context,), provides=self.interface)

        class Utility:
            __module__ = __name__

            def __call__(self, **kw):
                self.params = kw

        u = Utility()
        provideUtility(u, self.interface)
        c = Context()
        Receiver(c, Request())()
        self.assertEqual(Adapter.params, self.expected)
        self.failUnless(Adapter.context is c)


def setUp(test):
    config = getConfigContext()

    def load_zcml(text):
        xmlconfig.string(text, config)

    test.globs['load_zcml'] = load_zcml
    browser = Browser()
    browser.handleErrors = False
    test.globs['browser'] = browser


FunctionalLayer = ZCMLLayer(os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'), __name__, 'wasp Functional Layer', allow_teardown=True)

def test_suite():
    doc_suite = FunctionalDocFileSuite('readme.txt', setUp=setUp, tearDown=componentTearDown, optionflags=doctest.REPORT_NDIFF | doctest.ELLIPSIS)
    doc_suite.layer = FunctionalLayer
    return TestSuite((doc_suite, doctest.DocTestSuite(), makeSuite(Tests), makeSuite(SendTests), makeSuite(ReceiverIProcessReponseTests), makeSuite(ReceiverAdapterUtilityTests)))