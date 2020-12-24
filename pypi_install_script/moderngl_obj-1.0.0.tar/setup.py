import os

if os.environ.get('READTHEDOCS') == 'True':
    from distutils.core import setup

else:
    from setuptools import setup

setup(
    name='moderngl_obj',
    version='1.0.0',
    description='ModernGL extension for loading obj files',
    url='https://github.com/cprogrammer1994/ModernGL.ext.obj',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    license='MIT',
    install_requires=['ModernGL'],
    packages=['moderngl_obj'],
    platforms=['any']
)
