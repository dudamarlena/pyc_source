
import os
from distutils.core import setup

def loadMods(pkgName, modules, packageDirs):
   # read the modules names
   mods = open(os.path.join(pkgName, 'modules'), 'r').read().split()
   
   # remove the ".py" extensions, format into a full module name and
   # add to the modules list
   for mod in mods:
      modules.append('spug.%s.%s' % (pkgName, os.path.splitext(mod)[0]))
   
   # add the package to the package dirs dictionary
   packageDirs['spug.%s' % pkgName] = pkgName

# bootstrap with the spug.web modules (since that has its own setup.py)
modules = [
   'spug.web.cgi', 
   'spug.web.cxml', 
   'spug.web.form',
   'spug.web.forms',
   'spug.web.html', 
   'spug.web.htmlo',
   'spug.web.mgi',
   'spug.web.xmlo', 
   'spug.web.xparse',
   'spug.web.wof',
   
   'spug.__init__',
]
packageDirs = { 'spug.web': 'web', 'spug': '' }
loadMods('nml', modules, packageDirs)
loadMods('util', modules, packageDirs)
loadMods('win', modules, packageDirs)
loadMods('io', modules, packageDirs)
loadMods('net', modules, packageDirs)
loadMods('curses', modules, packageDirs)

setup(name = 'spuglib',
      version = '0.16',
      author = 'Michael A. Muller',
      author_email = 'mmuller@enduden.com',
      url = 'http://www.mindhog.net/~mmuller/spug_lib',
      description = 'General libraries for lots of different things.',
      py_modules = modules,
      package_dir = packageDirs
      )
