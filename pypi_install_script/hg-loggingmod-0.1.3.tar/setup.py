from setuptools import setup


setup(
    name='hg-loggingmod',
    version='0.1.3',
    author='Georges Racinet',
    author_email='georges.racinet@octobus.net',
    url='https://dev.heptapod.net/heptapod/hgext-loggingmod',
    description='Managing Mercurial logs with the standard Python logging module',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='hg mercurial',
    license='GPLv2+',
    packages=['hgext3rd', 'hgext3rd.loggingmod'],
    install_requires=['Mercurial'],
)
