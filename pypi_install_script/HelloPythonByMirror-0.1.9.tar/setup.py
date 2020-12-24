from distutils.core import setup

setup(
    name='HelloPythonByMirror',
    version='0.1.9',
    author='mirrorhanyu',
    author_email='mirrorhanyu@gmail.com',
    packages=['hellopythonbymirror', ],
    url='http://pypi.python.org/pypi/HelloPythonByMirror/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    install_requires=['requests >= 2.10.0', ],
    entry_points={
        'console_scripts': ['define=hellopythonbymirror.sayHello:main']
    }, )
