# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyops\main.py
# Compiled at: 2020-04-17 12:18:34
# Size of source mod 2**32: 4298 bytes
import pytest, logging
from .base import *
from .py_request import PyRequest
logger = logging.getLogger()

@pytest.fixture
def test_data(request):
    print('==================================================')
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run test_data => [{module}.{cls}.{func}]")
    data = get_data_by_func_name(func, cls, module, request)
    logger.debug(f"end test_data => [{module}.{cls}.{func}]")
    data['test_data'] = True
    yield data


@pytest.fixture
def test_flow(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run test_flow => [{module}.{cls}.{func}]")
    flow = get_flow_by_func_name(func, cls, module, request)
    for f in flow:
        if f.argcount == 2:
            status = f(test_data, PyRequest(request))
        else:
            status = f(test_data)
        if status is False:
            test_data['result'] = False
            test_data['msg'] = f"execute flow {f.__name__} Failed."
            break

    logger.debug(f"end test_flow => [{module}.{cls}.{func}]")
    test_data['test_flow'] = True
    yield flow


@pytest.fixture
def test_check(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run test_check => [{module}.{cls}.{func}]")
    if 'result' in test_data:
        logger.info(f"test_check msg => [{test_data['msg']}]")
        assert test_data['result']
        check = None
    else:
        check = get_check_by_func_name(func, cls, module, request)
        for f in check:
            if f.argcount == 2:
                if not f(test_data, PyRequest(request)):
                    raise AssertionError
                elif not f(test_data):
                    raise AssertionError

    logger.debug(f"end test_check => [{module}.{cls}.{func}]")
    test_data['test_check'] = True
    yield check


@pytest.fixture
def init(request, test_data):
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run setup => [{module}.{cls}.{func}]")
    init = get_init_by_name(cls, module, request)
    for f in init:
        if f.argcount == 2:
            status = f(test_data, PyRequest(request))
        else:
            status = f(test_data)
        if status is False:
            raise ValueError(f"setup failed for [{module}.{cls}.{func}]")

    logger.debug(f"end setup => [{module}.{cls}.{func}]")
    test_data['init'] = True
    yield


@pytest.fixture
def dest(request, test_data):
    yield
    test_data['dest'] = True
    func = request.function.__name__
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run teardown => [{module}.{cls}.{func}]")
    dest = get_dest_by_name(cls, module, request)
    for f in dest:
        if f.argcount == 2:
            status = f(test_data, PyRequest(request))
        else:
            status = f(test_data)
        if status is False:
            raise ValueError(f"teardown failed for [{module}.{cls}.{func}]")

    logger.debug(f"end teardown => [{module}.{cls}.{func}]")


@pytest.fixture(scope='class')
def class_init(request):
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run setup_class => [{module}.{cls}]")
    dest = get_class_init_by_name(cls, module, request)
    request.config.ah_class_config = get_global_config(cls, module, request)
    for f in dest:
        status = f(PyRequest(request))
        if status is False:
            raise ValueError(f"setup failed for [{module}.{cls}]")

    logger.debug(f"end setup_class => [{module}.{cls}]")
    yield


@pytest.fixture(scope='class')
def class_dest(request):
    yield
    cls = request.cls.__name__
    module = request.module.__name__
    logger.debug(f"run teardown_class => [{module}.{cls}]")
    dest = get_class_dest_by_name(cls, module, request)
    for f in dest:
        status = f(PyRequest(request))
        if status is False:
            raise ValueError(f"teardown failed for [{module}.{cls}]")

    request.config.ah_class_config = {}
    logger.debug(f"end teardown_class => [{module}.{cls}]")