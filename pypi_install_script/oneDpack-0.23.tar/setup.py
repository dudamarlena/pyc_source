from setuptools import setup,find_packages

requires = ["requests>=2.14.2"]


setup(
    name='oneDpack',
    version='0.23',
    description='1-dimentional binpacking library',
    url='https://github.com/hogehoge',
    author='Kyle',
    author_email='hoge@address.com',
    license='MIT',
    keywords='sample setuptools development',
    packages=find_packages(),
    install_requires=["mypulp"],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)