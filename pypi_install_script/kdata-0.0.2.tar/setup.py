from setuptools import setup, find_packages

requires = [
    "pandas",
    "rqalpha",
    "Click",
]

setup(name='kdata',
      version='0.0.2',
      description='kdata.',
      url='https://github.com/jungamer/kdata',
      author='jungamer',
      author_email='624621566@qq.com',
      license='MIT',
      #packages=['kdata'],
      packages=find_packages(),
      install_requires=requires,
      include_package_data=True,
      entry_points='''
        [console_scripts]
        stick=kdata.stick:get_tick_data
      ''',
      zip_safe=False)
