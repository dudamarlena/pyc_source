import os
from os import path
 
from distutils.core import setup
 
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)
 
package_dir = "./"
 
packages = []
for dirpath, dirnames, filenames in os.walk(package_dir):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README')).read()

REQUIREMENTS = [
'pyserial'
]
       
setup(
	name = 'weeemake_pi',
	version = '0.0.6',
	license = 'MIT',    
	author = 'Juneral',                       
	author_email = 'juneral@weeemake.com',
	url = 'https://www.weeemake.com.cn',
	description = 'Raspberry Python for Weeemake_Pi',
	long_description=LONG_DESCRIPTION,
	packages=packages
)
