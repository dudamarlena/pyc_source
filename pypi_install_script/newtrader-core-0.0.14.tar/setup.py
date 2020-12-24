import os
import glob
from setuptools import setup




from setuptools import Extension
from setuptools.command.build_ext import build_ext as _build_ext

ext = 'c'
sources = []
cython_modules = ['indicator/indicators', 'quotation',
                  'trade', 'broker', 'runner', 'strategies']
for m in cython_modules:
    sources+=glob.glob(f'newtrader/core/{m}/*.%s' % (ext,))
extensions = [
    Extension(source.split('.')[0].replace(os.path.sep, '.'),
              sources=[source],
            #   include_dirs=[numpy.get_include()]
              )
    for source in sources]

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

cmdclass = {'build_ext': build_ext}



setup(
    name="newtrader-core",
    version="0.0.14",
    author='Jiayi Su',
    author_email='nathaniel@finop.cloud',
    ext_modules=extensions,
    url="http://newtrader.finop.cloud",
    package_dir={
        "newtrader.core": "newtrader/core"
    },
    install_requires=[
        "numpy",
        "pandas",
        "prettytable",
        "tqdm",
        "tables",
        "click",
    ],
    setup_requires=[
        "numpy",
    ],
    package_data={
        "":["*.pxd","*.c"],
    },
    python_requires='>=3.8.1',
    cmdclass=cmdclass,
    zip_safe=False,
    packages=["newtrader.core",
              "newtrader.core.indicator",
              "newtrader.core.indicator.indicators",
              "newtrader.core.indicator.analyzer",
              "newtrader.core.indicator.generator",
              "newtrader.core.indicator.wrappers",
              "newtrader.core.broker",
              "newtrader.core.trade",
              "newtrader.core.config",
              "newtrader.core.util",
              "newtrader.core.quotation", "newtrader.core.strategies", "newtrader.core.runner"],
)
