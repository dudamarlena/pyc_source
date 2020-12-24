from setuptools import setup
from os import path, chdir, getcwd
from glob import glob

chdir(path.abspath(path.dirname(__file__)))

with open(path.join(getcwd(),'README.md'), 'r') as f:
    long_description = f.read() + '\n'

def read(*parts):
    with open(path.join(getcwd(), *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    import re
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

def get_package_data_list():
    from sys import version_info
    from platform import machine, system
    python_version_id=''.join(map(str, version_info[:2]))
    platform_id='-'.join( [ machine(), system() ] )

    if system().lower() == "linux":
        if machine().lower() == "x86_64":
            ends_with = "linux-gnu.so"
        if machine().lower() == "armv7l":
            ends_with = "arm-linux-gnueabihf.so"

    if system().lower() == "windows":
        if machine().lower() == "amd64":
          ends_with = "win_amd64.pyd"

    if system().lower() == "darwin":
      ends_with = "darwin.so"


    _find_all_files = []
    from os import walk
    from re import search, IGNORECASE
    for root, subfiles, files in walk('src'):
        for file in files:
            if file.endswith(".pye") or (file.endswith(ends_with) and search(python_version_id,file, IGNORECASE)):
                absfile = path.abspath( path.join( root, file ) )
                print("Selecting",absfile)
                _find_all_files.append( absfile )

    return _find_all_files

setup(
    name='sourcedefender',
    version=find_version('src/__init__.py'),
    python_requires="!=2.*,>=3.6",
    description='Advanced encryption protecting your python codebase.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='SOURCEdefender',
    keywords="encryption source aes",
    packages=[ 'sourcedefender' ],
    package_dir={ 'sourcedefender': 'src' },
    package_data={ 'sourcedefender': get_package_data_list() },
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        'console_scripts': [
        'sourcedefender = sourcedefender.encrypt:main',
        ]
    },
    zip_safe=True,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',

        'License :: Other/Proprietary License',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
