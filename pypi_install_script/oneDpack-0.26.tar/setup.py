from setuptools import setup, find_packages


requires = ["mypulp"]

setup(
    name='oneDpack',
    version='0.26',
    description='one dimentional library',
    url='https://github.com/whatever/whatever',
    author='Kyle',
    author_email='hoge@gmail.com',
    license='MIT',
    keywords='one dimentional library',
    packages=["oneDpack"],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)