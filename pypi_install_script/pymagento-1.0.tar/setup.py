from distutils.core import setup
import pymagento


setup(name = "pymagento",
      author = "Russ Amos",
      url = "http://github.com/russ-/pymagento",
      version = pymagento.__version__,
      packages = [
          'pymagento',
      ],
)
