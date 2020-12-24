from setuptools import setup

dep_ver = "0.2.20171113"
dep_repo = "git+https://github.com/mbientlab/ParsePy.git"
pip_dep_suffix = "@master#egg=parse_rest-" + dep_ver

setup(
    name='metacloud',
    author="MbientLab",
    author_email="hello@mbientlab.com",
    download_url="https://github.com/mbientlab/MetaCloud-SDK-Python/archive/0.2.0.tar.gz",
    version='0.2.0',
    packages=['mbientlab', 'mbientlab.metacloud'],
    license='https://mbientlab.com/license/',
    install_requires=[
        'parse_rest==' + dep_ver,
    ],
    extras_require={
        'metawear': ['metawear>=0.3.0']
    },
    dependency_links=[
        dep_repo + '/' + pip_dep_suffix,
        dep_repo + pip_dep_suffix
    ],
    long_description=open('README.rst').read(),
)
