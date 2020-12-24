from setuptools import setup

setup(
    name='gitbackup',
    version='0.1.2',
    url='https://github.com/sciunto-org/gitbackup',
    maintainer='F. Boulogne',
    maintainer_email='devel@sciunto.org',
    license='GNU General Public License (GPL)',
    platforms=['all'],
    description='Mirror git repositories',
    packages=['libgitbackup',],
    provides=['gitbackup',],
    scripts=['gitbackup'],
    )
