# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/uuids.py
# Compiled at: 2017-01-31 21:59:16
# Size of source mod 2**32: 1490 bytes
__doc__ = 'Configure psycopg2 to support UUID conversion.'
import psycopg2.extras
from postpy.admin import install_extensions
CRYPTO_EXTENSION = 'pgcrypto'
UUID_OSSP_EXTENSION = 'uuid-ossp'

def register_client():
    """Have psycopg2 marshall UUID objects automatically."""
    psycopg2.extras.register_uuid()


def register_crypto():
    """Support for UUID's on server side.

    Lighter dependency than uuid-ossp supporting
    random_uuid_function for UUID generation.
    """
    install_extensions([CRYPTO_EXTENSION])


def register_uuid():
    """Support for UUID's on server side.

    Notes
    -----
    uuid-ossp can be problematic on some platforms. See:
    https://www.postgresql.org/docs/current/static/uuid-ossp.html
    """
    install_extensions([UUID_OSSP_EXTENSION])


def random_uuid_function(schema=None):
    """Cryptographic random UUID function.

    Generates random database side UUID's.

    Notes
    -----
    Lighter dependency than uuid-ossp, but higher
    fragmentation on disk if used as auto-generating primary key UUID.
    """
    return '{}gen_random_uuid()'.format(_format_schema(schema))


def uuid_sequence_function(schema=None):
    """Sequential UUID generation.

    Sequential UUID creation on database side offering
    less table fragmentation issues when used as UUID primary key.
    """
    return '{}uuid_generate_v1mc()'.format(_format_schema(schema))


def _format_schema(schema):
    if schema:
        return '{}.'.format(schema)
    return ''