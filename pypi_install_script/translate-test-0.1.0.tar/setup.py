
from setuptools import setup, find_packages

setup(
    name='translate-test',
    version='0.1.0',
    description='sogou',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers'
    ],
    author='chen',
    url='https://github.com/mydu27/deemo',
    author_email='chenjiageng@geekpark.net',
    packages=find_packages('requests'),
    include_package_data=False,
    zip_safe=True
)
