from setuptools import setup

#__path__ = 'build.lib'

def read(fn):
    with open(fn, 'r') as f:
        return f.read()

setup(
        name='filecontrol',
        version='1.0.15',
        description='Control files',
        long_description=read('README.txt')
#        py_modules=['__init__.py', 'dircontrol.py']
)
