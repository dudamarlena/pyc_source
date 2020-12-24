# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/test.py
# Compiled at: 2010-05-30 13:30:03
__doc__ = "\n    == Making The Plugins Available ==\n    \n    If pysmvt is installed, you should see the following in the output of\n    `nosetests --help`:\n    \n        ...\n        --pysmvt-app-profile=PYSMVT_PROFILE\n                    The name of the test profile in settings.py\n        ...\n    \n    == Using the Plugins ==\n    \n    You **must** be inside a pysmvt application's package directory for\n    these plugins to work:\n    \n        `cd .../myproject/src/myapp-dist/myapp/`\n    \n    === Init Current App Plugin ===\n    \n    This plugin does two things:\n        \n        - initializes a WSGI application for the current application\n          (optionally allowing you to specify which profile you want used\n          to initlize the application)\n        - automatically includes test's from packages if so defined in the\n          profile which is loaded.\n    \n    You don't have to do anything explicit to use this plugin.  It is\n    enabled automatically when `nosetests` is run from inside an\n    application's directory structure.  Assuming your make_wsgi() function\n    is setup correctly, globaly proxy objects like 'ag' should now function\n    correctly.  Request level objects, like 'rg' will not yet be available\n    however.\n    \n    In order to get access to the wsgi application that was instantiated,\n    you can do:\n        \n        from pysmvt import ag\n        \n        testapp = ag._wsgi_test_app\n        \n    `testapp` could now be used in the pysmvt.utils.wrapinapp() decorator.\n    \n    The default profile used with this plugin is 'Test'.  If you need to\n    specifiy a different profile, do:\n        \n        `nosetests  --pymvt-app-profile=mytestprofile`\n        \n    To include tests from packges outside the application's directory\n    structure, you can put a `testing.include_pkgs` attribute in your test\n    profile. For example:\n    \n        class TestPysapp(Test):\n            def __init__(self):\n                # call parent init to setup default settings\n                Test.__init__(self)\n                \n                # include pysapp tests\n                self.testing.include_pkgs = 'pysapp'\n        testpysapp = TestPysapp\n    \n    Running:\n        \n        `nosetests  --pysmvt-app-profile=testpysapp`\n    \n    Would be equivelent to running:\n    \n        `nosetests pysapp`\n    \n    Packages can also be specified as a list/tuple:\n        \n        # include multiple tests\n        self.testing.include_pkgs = ('pysapp', 'somepkg')        \n"
import os, logging, nose.plugins
from nose.tools import make_decorator
from pysmvt import ag, settings
from pysmvt.script import _app_name
from pysmvt.utils import import_app_str
from pysutils import tolist
from werkzeug import Client as WClient, BaseRequest, BaseResponse, cached_property
from webhelpers.html import tools
try:
    from webtest import TestApp as WTTestApp
    from webtest import TestResponse as WTTestResponse
except ImportError:
    WTTestApp = None

class InitCurrentAppPlugin(nose.plugins.Plugin):
    opt_app_profile = 'pysmvt_profile'
    val_app_profile = None
    opt_app_name = 'pysmvt_name'
    val_app_name = None
    opt_disable = 'pysmvt_disable'
    val_disable = False

    def add_options(self, parser, env=os.environ):
        """Add command-line options for this plugin"""
        env_opt = 'NOSE_WITH_%s' % self.name.upper()
        env_opt.replace('-', '_')
        parser.add_option('--pysmvt-app-profile', dest=self.opt_app_profile, type='string', default='Test', help='The name of the test profile in settings.py')
        parser.add_option('--pysmvt-app-name', dest=self.opt_app_profile, type='string', default='Test', help="The name of the application's package, defaults to top package of current working directory")
        parser.add_option('--pysmvt-disable', dest=self.opt_disable, action='store_true', help='Disable plugin')

    def configure(self, options, conf):
        """Configure the plugin"""
        self.val_disable = getattr(options, self.opt_disable, False)
        if not self.val_disable:
            if hasattr(options, self.opt_app_profile):
                self.val_app_profile = getattr(options, self.opt_app_profile)
            if hasattr(options, self.opt_app_name):
                self.val_app_name = getattr(options, self.opt_app_name)
            else:
                try:
                    self.val_app_name = _app_name()
                except Exception, e:
                    if 'package name could not be determined' not in str(e):
                        raise
                else:
                    if not self.val_app_name:
                        self.val_disable = True
        if not self.val_disable:
            apps_pymod = __import__('%s.applications' % self.val_app_name, globals(), locals(), [''])
            ag._wsgi_test_app = apps_pymod.make_wsgi(self.val_app_profile)
            for callstring in tolist(settings.testing.init_callables):
                tocall = import_app_str(callstring)
                tocall()

    def loadTestsFromNames(self, names, module=None):
        if not self.val_disable:
            try:
                names.extend(tolist(settings.testing.include_pkgs))
            except AttributeError, e:
                if "has no attribute 'testing'" not in str(e):
                    raise


class Client(WClient):

    def open(self, *args, **kwargs):
        """
            if follow_redirects is requested, a (BaseRequest, response) tuple
            will be returned, the request being the last redirect request
            made to get the response
        """
        fr = kwargs.get('follow_redirects', False)
        if fr:
            kwargs['as_tuple'] = True
        retval = WClient.open(self, *args, **kwargs)
        if fr:
            return (BaseRequest(retval[0]), retval[1])
        return retval


def mock_smtp(cancel_override=True):
    ''' A decorator that allows you to test emails that are sent during
        functional or unit testing by mocking SMTP lib objects with the
        MiniMock library and giving the test function the tracker object
        to do tests with.
        
        :param cancel_override: in testing, we often will have email_overrides
            set so that emails don't get sent out for real.  Since this function
            prevents live emails from being sent, we will most often want
            to cancel that setting for the duration of the test so that the
            email tested is exactly what would be sent out if the emails were
            live.
        :raises: :exc:`ImportError` if the MiniMock library is not installed
        
    Example use::

    @mock_smtp()
    def test_user_form(self, mm_tracker=None):
        add_new_user_which_sends_email_to_user(form_data)
        look_for = """Called smtp_connection.sendmail(
    '...',
    [u'%s'],
    'Content-Type:...To: %s...You have been added to our """             """system of registered users...REQUIRED to change it...
Called smtp_connection.quit()""" % (form_data['email_address'], form_data['email_address'])
        assert mm_tracker.check(look_for), mm_tracker.diff(look_for)
        # make sure only one email is sent out.  Can't == b/c from address
        # will change, but length is ~837, so 1000 seems safe
        assert len(mm_tracker.dump()) <= 1000, len(mm_tracker.dump())
          
        @mock_smtp()
        def test_that_fails():
            assert mm_tracker.check('Called smtp_connection.sendmail(...%s...has been issu'
                        'ed to reset the password...' % user.email_address)
    
    Other tracker methods::
        mm_tracker.dump(): returns minimock usage captured so far
        mm_tracker.diff(): returns diff of expected output and actual output
        mm_tracker.clear(): clears the tracker of everything captured
    '''
    try:
        import minimock
    except ImportError:
        raise ImportError('use of the assert_email decorator requires the minimock library')

    import smtplib

    def decorate(func):

        def newfunc(*arg, **kw):
            try:
                override = None
                tt = minimock.TraceTracker()
                smtplib.SMTP = minimock.Mock('smtplib.SMTP', tracker=None)
                smtplib.SMTP.mock_returns = minimock.Mock('smtp_connection', tracker=tt)
                if cancel_override:
                    override = settings.emails.override
                    settings.emails.override = None
                kw['mm_tracker'] = tt
                func(*arg, **kw)
            finally:
                minimock.restore()
                if cancel_override:
                    settings.emails.override = override

            return

        newfunc = make_decorator(func)(newfunc)
        return newfunc

    return decorate


class LoggingHandler(logging.Handler):
    """ logging handler to check for expected logs when testing"""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [], 'critical': []}


def logging_handler(logger_to_examine):
    lr = logging.getLogger(logger_to_examine)
    lh = LoggingHandler()
    lr.addHandler(lh)
    return lh


class TestResponse(BaseResponse):

    @cached_property
    def fdata(self):
        return self.filter_data()

    @cached_property
    def wsdata(self):
        return self.filter_data(strip_links=False)

    def filter_data(self, normalize_ws=True, strip_links=True):
        data = super(TestResponse, self).data
        if normalize_ws:
            data = (' ').join(data.split())
        if not strip_links:
            return data
        return tools.strip_links(data)


if WTTestApp:

    class TestApp(WTTestApp):
        pass


    def pyquery(self):
        """
        Returns the response as a `PyQuery <http://pyquery.org/>`_ object.

        Only works with HTML and XML responses; other content-types raise
        AttributeError.
        """
        if 'html' not in self.content_type and 'xml' not in self.content_type:
            raise AttributeError('Not an HTML or XML response body (content-type: %s)' % self.content_type)
        try:
            from pyquery import PyQuery
        except ImportError:
            raise ImportError('You must have PyQuery installed to use response.pyquery')

        d = PyQuery(self.body)
        return d


    WTTestResponse.pyq = property(pyquery, doc=pyquery.__doc__)
else:

    def TestApp(object):

        def __init__(self, *args, **kwargs):
            raise ImportError('You must have WebTest installed to use TestApp')