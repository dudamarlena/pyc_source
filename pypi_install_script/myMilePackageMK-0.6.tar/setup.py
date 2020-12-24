from setuptools import setup, find_packages

setup(
    name='myMilePackageMK',
    version='0.6',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/khalad-hasan/myMileConverter',
    author='MK Hasan',
    author_email='khalad.hasan@gmail.com'
)