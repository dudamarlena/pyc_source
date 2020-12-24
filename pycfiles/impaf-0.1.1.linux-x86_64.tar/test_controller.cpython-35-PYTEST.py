# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/controller/tests/test_controller.py
# Compiled at: 2015-07-18 14:00:01
# Size of source mod 2**32: 4489 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from collections import defaultdict
from mock import MagicMock
from mock import patch
from mock import sentinel
from pytest import fixture
from pytest import yield_fixture
from pytest import raises
from .. import Controller
from ..exceptions import FinalizeController
from ..exceptions import QuitController

class ExampleController(Controller):

    def run(self):
        self.runned = defaultdict(lambda : False)
        return super().run()

    def _before_context(self):
        super()._before_context()
        self.runned['_before_context'] = True

    def _before_make(self):
        super()._before_make()
        self.runned['_before_make'] = True

    def _after_make(self):
        super()._after_make()
        self.runned['_after_make'] = True

    def _create_widgets(self):
        super()._create_widgets()
        self.runned['_create_widgets'] = True

    def _before_quit(self):
        super()._before_quit()
        self.runned['_before_quit'] = True

    def _get_request_cls(self):
        return lambda x: x


class ControllerFixtures(object):

    @fixture
    def mroot_factory(self):
        return MagicMock()

    @fixture
    def mrequest(self):
        return MagicMock()

    @fixture
    def controller(self, mroot_factory, mrequest):
        return ExampleController(mroot_factory, mrequest)

    @yield_fixture
    def mmake(self, controller):
        patcher = patch.object(controller, 'make')
        with patcher as (mock):
            yield mock


class TestController(ControllerFixtures):

    def test_normaln_run(self, controller, mrequest, mroot_factory):
        response = controller()
        @py_assert1 = controller.context
        @py_assert4 = {'request': mrequest, 'route_path': mrequest.route_path}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = controller.request
        @py_assert3 = @py_assert1 == mrequest
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.request\n} == %(py4)s', ), (@py_assert1, mrequest)) % {'py4': @pytest_ar._saferepr(mrequest) if 'mrequest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mrequest) else 'mrequest', 'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = controller.root_factory
        @py_assert3 = @py_assert1 == mroot_factory
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.root_factory\n} == %(py4)s', ), (@py_assert1, mroot_factory)) % {'py4': @pytest_ar._saferepr(mroot_factory) if 'mroot_factory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mroot_factory) else 'mroot_factory', 'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = controller.response
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.response\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert3 = controller.context
        @py_assert1 = response == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.context\n}', ), (response, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response', 'py2': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = controller.runned
        @py_assert4 = {'_before_context': True, '_before_make': True, '_after_make': True, '_create_widgets': True}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.runned\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_on_response_setted(self, controller):
        """
        When .response on controller is not None, controller should return this
        response.
        """
        controller.response = sentinel.response
        @py_assert1 = controller()
        @py_assert5 = sentinel.response
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py6)s\n{%(py6)s = %(py4)s.response\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel', 'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_on_finalizing(self, controller, mrequest, mmake):
        """
        When .make raises FinalizeController, then all the rest of the
        controller mechanics should run normally. FinalizeController.context
        should be added to controller context.
        """
        mmake.side_effect = FinalizeController({'fin': True})
        @py_assert1 = controller()
        @py_assert4 = {'request': mrequest, 'route_path': mrequest.route_path, 'fin': True}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_on_quit(self, controller, mmake):
        """
        QuitController should end up controller immediately and return whit
        what object was initalized.
        """
        mmake.side_effect = QuitController({'quit': True})
        @py_assert1 = controller()
        @py_assert4 = {'quit': True}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = controller.runned
        @py_assert4 = {'_before_context': True, '_before_make': True, '_before_quit': True}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.runned\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


class TestControllerUtils(ControllerFixtures):

    @yield_fixture
    def mHTTPFound(self):
        patcher = patch('impaf.controller.utils.HTTPFound')
        with patcher as (mock):
            yield mock

    def test_add_widget(self, controller, mrequest):
        mwidget = MagicMock()
        controller.context = {}
        controller.add_widget('myname', mwidget)
        @py_assert1 = controller.context
        @py_assert4 = {'myname': mwidget}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        mwidget.feed_request.assert_called_once_with(mrequest)

    def test_redirect(self, controller, mrequest, mHTTPFound):
        controller.redirect('somewhere', kw='arg')
        @py_assert1 = controller.response
        @py_assert5 = mHTTPFound.return_value
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.response\n} == %(py6)s\n{%(py6)s = %(py4)s.return_value\n}', ), (@py_assert1, @py_assert5)) % {'py4': @pytest_ar._saferepr(mHTTPFound) if 'mHTTPFound' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mHTTPFound) else 'mHTTPFound', 'py0': @pytest_ar._saferepr(controller) if 'controller' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(controller) else 'controller', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        mHTTPFound.assert_called_once_with(location=mrequest.route_url.return_value, headers=mrequest.response.headerlist)
        mrequest.route_url.assert_called_once_with('somewhere', kw='arg')

    def test_redirect_with_quit(self, controller):
        with raises(QuitController):
            controller.redirect('somewhere', True, kw='arg')