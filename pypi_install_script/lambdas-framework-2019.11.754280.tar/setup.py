"""Setup package."""

import distutils
from datetime import datetime


def get_minor_version() -> int:
    """Number of seconds since the beginning of the month."""
    utc_now = \
        datetime.utcnow()
    utc_beginning_of_month = \
        datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    return int((utc_now - utc_beginning_of_month).total_seconds())


def get_version():
    return datetime.utcnow().strftime(f'%Y.%m.{get_minor_version()}')


distutils.core.setup(
    name='lambdas-framework',
    version=get_version(),
    packages=[
        'lambdas',
        'lambdas.cli',
    ],
    install_requires=[
        'aiohttp==3.6.2',
        'flask==1.1.1',
        'pyopenssl==19.0.0',
        'requests==2.22.0',
        'ruamel.yaml==0.16.5',
    ],
    entry_points={
        'console_scripts': [
            'lambdas=lambdas.cli:cli',
        ],
    },
)
