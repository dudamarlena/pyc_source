from distutils import log
import os

from setuptools import find_packages, setup


def prerelease_local_scheme(version):
    """Return local scheme version unless building on master in Gitlab.

    This function returns the local scheme version number
    (e.g. 0.0.0.dev<N>+g<HASH>) unless building on Gitlab for a
    pre-release in which case it ignores the hash and produces a
    PEP440 compliant pre-release version number (e.g. 0.0.0.dev<N>).

    """

    from setuptools_scm.version import get_local_node_and_date

    if 'CI_COMMIT_REF_NAME' in os.environ and \
       os.environ['CI_COMMIT_REF_NAME'] == 'master':
        return ''
    else:
        return get_local_node_and_date(version)


def list_files_recursive(relpath):
    for root, dirs, files in os.walk(relpath):
        install_root = os.path.join('share', 'stumpf', root)
        yield install_root, [os.path.join(root, file) for file in files]


if not os.path.exists(os.path.join('static', 'index.html')):
    log.warn(
        'Static assets are not built.  Run "npm install && npm run build" '
        'in the web directory prior to packaging stumpf.'
    )

data_files = []
data_files.extend(list_files_recursive('migrations'))
data_files.extend(list_files_recursive('static'))


setup(
    name='stumpf',
    use_scm_version={'local_scheme': prerelease_local_scheme},
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'alembic',
        'apispec>=1.0.0b5',
        'apispec-webframeworks',
        'blinker',
        'boto3',
        'faker',
        'flask>=1.1',
        'flask-cors',
        'flask-dance',
        'flask-login',
        'flask-migrate',
        'flask-sqlalchemy',
        'marshmallow>=3.0.0',
        'psycopg2-binary',
        'python-dateutil<2.8.1',  # /me shakes fist at botocore
        'python-dotenv',
        'pyyaml',
        'sentry-sdk[flask]>=0.13',
        'statsd',
        'sqlalchemy-utils',
        'tabulate',
        'celery[redis]'
    ],
    license='Apache Software License 2.0',
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'stumpf-generate-sample-data=stumpf.cli:sample_data',
            'stumpf-create-tables=stumpf.cli:create_tables',
            'stumpf-trace=stumpf.cli:trace'
        ],
        'stumpf.pipeline.celery.conf': [
            'core=stumpf.celery.config:default_config'
        ],
        'stumpf.pipeline.tasks.task_status_change': [],
        'stumpf.pipeline.tasks.assignment_status_change': [],
        'stumpf.pipeline.models': []
    },
    extras_require={
        'crypto': ['m2crypto']
    }
)
