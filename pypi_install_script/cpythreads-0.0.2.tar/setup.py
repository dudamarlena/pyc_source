import subprocess
import re
from setuptools import setup


def get_version_from_tag():
    tag = subprocess.Popen(
        [
            'git',
            'tag',
            '--points-at',
            'HEAD'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    regexp = re.compile(r'^[0-9]*(\.[0-9]+)*$')
    while True:
        line = tag.stdout.readline().decode().rstrip()
        if line:
            print(line)
            if regexp.match(line):
                print (line)
                return line
        else:
            break

    return '0.0.1'


setup(
    name='cpythreads',
    version=get_version_from_tag(),
    author='Steib Cristian',
    author_email='cristiansteib@gmail.com',
    packages=['cpythreads'],
    url='https://github.com/cristiansteib/cpythreads/',
    license='LICENSE.txt',
    description='Thread executor for Python3',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords = ['Threads', 'PoolThreads', 'thread'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX ",
        'License :: OSI Approved :: MIT License',
        "Development Status :: 5 - Production/Stable"
    ],
)