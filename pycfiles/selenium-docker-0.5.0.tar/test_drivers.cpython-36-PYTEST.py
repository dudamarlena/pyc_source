# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blake/code/vivint-selenium-docker/tests/test_drivers.py
# Compiled at: 2017-11-07 17:39:04
# Size of source mod 2**32: 896 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from selenium_docker.drivers import DockerDriverBase
from selenium_docker.drivers.chrome import ChromeDriver
from selenium_docker.drivers.firefox import FirefoxDriver

@pytest.mark.parametrize('cls', [ChromeDriver, FirefoxDriver])
@pytest.mark.parametrize('ua', [None, 'custom', lambda : 'custom-fn'])
def test_driver(cls, ua, factory):
    for attr in ('BROWSER', 'CONTAINER', 'DEFAULT_ARGUMENTS', 'SELENIUM_PORT', 'Flags'):
        @py_assert3 = hasattr(cls, attr)
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1':@pytest_ar._saferepr(cls) if 'cls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cls) else 'cls',  'py2':@pytest_ar._saferepr(attr) if 'attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr) else 'attr',  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None

    flags = cls.Flags
    for flag in [flags.ALL, flags.DISABLED]:
        driver = cls(user_agent=ua, flags=flag, factory=factory)
        @py_assert3 = isinstance(driver, DockerDriverBase)
        if not @py_assert3:
            @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(driver) if 'driver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(driver) else 'driver',  'py2':@pytest_ar._saferepr(DockerDriverBase) if 'DockerDriverBase' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DockerDriverBase) else 'DockerDriverBase',  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        driver.get('https://vivint.com')
        @py_assert1 = driver.title
        if not @py_assert1:
            @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.title\n}') % {'py0':@pytest_ar._saferepr(driver) if 'driver' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(driver) else 'driver',  'py2':@pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None
        driver.quit()
        driver.close_container()