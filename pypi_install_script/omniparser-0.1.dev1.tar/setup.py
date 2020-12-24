import os
from distutils.core import setup


PATH = os.path.split(os.path.abspath(__file__))[0]


def get_dependencies(path):
    dependencies = []
    with open(os.path.join(path, 'requirements.txt'), 'r') as f:
        for line in f.readlines():
            dependencies.append(line)
    return dependencies


setup(
    name='omniparser',
    version='0.1.dev1',
    author='Oscar Butler Aldridge',
    author_email='oscarb@protonmail.com',
    packages=['omniparser', 'omniparser.test'],
    url='',
    license='LICENSE.txt',
    description='A base to build your specific parsers on!',
    long_description=open(os.path.join(PATH, 'README.rst'), 'r').read(),
    install_requires=get_dependencies(PATH)
)
