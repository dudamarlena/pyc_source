import afs_pytest_plugin
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='afs_pytest_plugin',
    version=afs_pytest_plugin.__version__,
    entry_points={
        'pytest11': [
            'server = afs_pytest_plugin.afs_server',
            'api_version = afs_pytest_plugin.afs_api_version',
            'init_api_worker = afs_pytest_plugin.afs_init_api_worker',
            'init_active_testcase = afs_pytest_plugin.afs_init_active_testcase',
            'testrun_data = afs_pytest_plugin.afs_testrun_data',
            'init_active_testrun = afs_pytest_plugin.afs_init_active_testrun',
            'init_active_testsuite = afs_pytest_plugin.afs_init_active_testsuite',
            'init_active_project = afs_pytest_plugin.afs_init_active_project',
        ],
    },
    install_requires=['pytest', 'afs-api-worker'],
    author='Yurii Chudakov',
    author_email='kappa@ksprojects.ru',
    description='AFS Pytest plugins',
    license='Apache2',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read()
)


