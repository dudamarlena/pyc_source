from distutils.core import setup

from Cython.Build import cythonize

setup(
    name='ppxt',
    ext_modules=cythonize([
        "ppxt/__init__.py",
        "ppxt/base.py",
        "ppxt/fcoin.py",
        "ppxt/gate.py",
        "ppxt/whale.py",
    ])
)
