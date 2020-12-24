from setuptools import setup
import sys
from iot49connect.version import __version__

# https://python-packaging.readthedocs.io/en/latest/minimal.html
# https://realpython.com/pypi-publish-python-package/
# https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html
# https://pypi.org/project/twine/

"""
Install Locally
---------------

python setup.py sdist
pip install .

PyPi Test
---------

pip install twine
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
login/pwd: ttmetro, O_X

WAIT 10 secs, THEN:
pip install -i https://test.pypi.org/simple/ iot49connect==0.1.0


PyPi Release
------------

update version.py

THEN:
rm -rf dist
python setup.py sdist
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
ttmetro

pip install --upgrade iot49connect
"""

if sys.version_info < (3, 6):
    print('Python 3.6 or later requied')
    # maybe this works with other versions also ...
    # sys.exit(1)

install_req = [
    'pyserial',
    'pyopenssl',
]

setup(
    name = 'iot49connect',
    packages = ['iot49connect'],
    version = __version__,
    description = 'Replicate USB traffic on a socket',
    long_description = 'see https://github.com/ttmetro/iot49connect',
    license = 'MIT',
    author = 'Bernhard Boser',
    author_email = 'boser@berkeley.edu',
    url = 'https://iot49.github.io',
    keywords = ['micropython', 'iotpython'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    install_requires=install_req,
    entry_points = {
        'console_scripts': [
            'iot49connect=iot49connect:main'
        ],
    },
)
