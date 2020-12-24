from setuptools import setup

setup(
    entry_points={
        'sqlalchemy.dialects': [
            'informix = sqlalchemy_gbase8t.ibmdb:InformixDialect',
        ]
    }
)
