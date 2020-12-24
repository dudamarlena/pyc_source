import os
import shutil
import sysconfig
from distutils.core import setup

setup(
    name="zen-of-numpy", version="0.1", py_modules=["np_this"],
)

try:
    import numpy
except ImportError:
    lib = sysconfig.get_paths()["purelib"]
    npdir = os.path.join(lib, "numpy")
else:
    npdir = os.path.dirname(numpy.__file__)

if not os.path.exists(npdir):
    os.makedirs(npdir)
    npinit = os.path.join(npdir, "__init__.py")
    with open(npinit, "a"):
        pass

npthis = os.path.join(npdir, "this.py")
shutil.copy("np_this.py", npthis)
