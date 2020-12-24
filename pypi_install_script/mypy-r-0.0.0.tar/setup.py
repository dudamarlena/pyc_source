from distutils.core import setup

setup(
    name='mypy-r',
    description='Recursive mypy that find package directories',
    author='Joe Ceresini',
    author_email='joe@ceresini.com',
    packages=['mypy_r'],
    entry_points={
        'console_scripts': [
            'mypy-r=mypy_r.__main__:console_script',
        ]
    },
    install_requires=[
        'mypy',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
