import os
import re
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    version_file = open(
        os.path.join(
            os.path.dirname(__file__), 'amanita_barrier', '__init__.py')
    ).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    author='Max Lit',
    author_email='max.lit.mbox@gmail.com',
    name='amanita_barrier',
    version=get_version(),
    license='LGPL-3',
    description='Amanita Barriers',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='http://gitlab.com/amanita-barrier/services',
    keywords=['barriers', 'odoo', 'amanita'],
    download_url='http://gitlab.com/amanita-barrier/services/-/archive/'
                 'master/services-master.tar.gz',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'alembic',
        'click',
        'jinja2',
        'graypy',
        'nameko',
        'nameko-sqlalchemy',
        'nameko-odoo>=1.0.2',
        'odoorpc',
        'psutil',
        'pyyaml>=5.1',
        'pyserial',
        'setproctitle',
        'sqlalchemy',
    ],
    entry_points='''
        [console_scripts]
        amanitabar=amanita_barrier.cli:main
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
