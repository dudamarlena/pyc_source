from setuptools import setup

name = 'lazy-write'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.1',
    description='Write to file if need',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='File Read Write',
    py_modules=[f'{module}'],
    install_requires=[]
)
