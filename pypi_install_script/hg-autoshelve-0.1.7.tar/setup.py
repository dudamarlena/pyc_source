import io
import os.path
from distutils.core import setup

ROOT_PATH = os.path.dirname(__file__)


def read_file(*path):
    fullpath = os.path.join(ROOT_PATH, *path)
    with io.open(fullpath, encoding='utf-8') as fobj:
        return fobj.read()


def get_metadata():
    """Return metadata."""
    metadata = {}
    exec(read_file('hgext3rd', 'autoshelve', 'metadata.py'), metadata)
    metadata['readme'] = read_file('README')
    return metadata


METADATA = get_metadata()


setup(
    name='hg-autoshelve',
    version=METADATA['__version__'].decode('utf-8'),
    author='Alain Leufroy',
    author_email='~alainl/hg-autoshelve@lists.sr.ht',
    maintainer='Alain Leufroy',
    maintainer_email='~alainl/hg-autoshelve@lists.sr.ht',
    url='https://hg.sr.ht/~alain/hg-autoshelve',
    description=METADATA['readme'].split('\n', 2)[1],
    long_description=METADATA['readme'],
    long_description_content_type='text/x-rst',
    keywords='hg mercurial shelve',
    license='GPLv2+',
    packages=['hgext3rd.autoshelve'],
    package_dir={'hgext3rd': os.path.join(ROOT_PATH, 'hgext3rd')},
)
