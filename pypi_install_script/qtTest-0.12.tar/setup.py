from setuptools import setup
import os


datadir = os.path.join('quantiacsToolbox','data')
datafiles=[ (d, [os.path.join(d, f) for f in files]) for d,folders,files in os.walk(datadir)]

setup(name='qtTest',
      version='0.12',
      description='The Quantiacs Toolbox for trading system development',
      url='http://quantiacs.com/',
      author='Vernie Redmon',
      author_email='vnredmon@quantiacs.com',
      license='MIT',
      packages=['qtTest'],
#      package_dir={'quantiacsToolbox': 'quantiacsToolbox/data/*'},
      include_package_data = True,

      install_requires=[
          'numpy','matplotlib', 'sys','urllib3','datetime'
      ],
      zip_safe=False,
#      data_files=datafiles
     )


