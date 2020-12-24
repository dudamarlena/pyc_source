"""Setup package."""

import distutils
from datetime import datetime


def get_minor_version() -> int:
    """Number of seconds since the beginning of the month."""
    utc_now = \
        datetime.utcnow()
    utc_beginning_of_month = \
        datetime.utcnow().replace(day=1, minute=0, second=0)
    return int((utc_now - utc_beginning_of_month).total_seconds())


def get_version():
    return datetime.utcnow().strftime(f'%Y.%m.{get_minor_version()}')


distutils.core.setup(
    name='oblivion',
    version=get_version(),
    packages=[
        'oblivion',
        'oblivion.cli'
    ],

    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'oblivion=oblivion.cli:cli',
        ],
    },
)
