import os
import sys
import re
from setuptools import setup

# long_description: Take from README file
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

# Version Number
version = '0.13.5'

def check_dependencies():
    requirements = [line.strip() for line in open('requirements.txt')]

    # Just make sure dependencies exist, I haven't rigorously
    # tested what the minimal versions that will work are
    # (help on that would be awesome)
    try:
        import pandas
    except ImportError:
        requirements.append('pandas')

    return requirements

# Dependencies
if sys.platform.startswith('win') or sys.platform.startswith('linux'):
    requirements = [line.strip() for line in open('requirements.txt')]
else:
    raise OSError("目前只支持windows和linux系统.")

# This shouldn't be necessary anymore as we dropped official support for < 2.7 and < 3.3
if (sys.version_info[0] == 2 and sys.version_info[:2] < (2, 7)) or (sys.version_info[0] == 3 and sys.version_info[:2] < (3, 2)):
    requirements = requirements + []

setup(
    name='pmipy',
    version=version,
    license='MIT',
    author='biojim',
    author_email='biojxz@163.com',
    description='A tool for my team.',
    long_description=readme,
    packages=['pmipy'],
    package_data={'pmipy': ['tests/*.png', 'support/*.py', 'Rscript/*.r', 'OCM/*.py', 'xlwings.applescript'],},
    keywords=["I don't want to tell you!"],
    install_requires=requirements,
    entry_points={'console_scripts': ['pmipy=pmipy.command_line:main'],},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'License :: OSI Approved :: BSD License'],
    platforms=['Windows'],
)
