from setuptools import setup
from sys import platform

requirements = []
if platform == "win32":
    requirements.append('windows-curses')

setup(
    name='jswitch',
    version='0.0.2',
    description='JSwitch: text-based menu for switching between Java environments',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/DevDungeon/issh',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    py_modules=['jswitch'],
    entry_points={
        'console_scripts': [
            'jsw = jswitch:main',
        ],
    }
    ,
    zip_safe=False,
    install_requires=[
        requirements,
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    python_requires='<3.6',
)
