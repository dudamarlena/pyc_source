from distutils.core import setup

VERSION = '0.2'
REPOSITORY = 'https://gitlab.com/edricgarran/hot_reload'
ARCHIVE = (
    '{repository}/repository/archive.tar.gz?ref={version}'
).format(repository=REPOSITORY, version=VERSION)

setup(
    name='hot_reload',
    py_modules=['hot_reload'],
    version=VERSION,
    description='A runtime code reloader.',
    author='Felipe Trzaskowski',
    author_email='666.felipe@gmail.com',
    url=REPOSITORY,
    download_url=ARCHIVE,
)
