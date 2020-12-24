from setuptools import setup, find_packages

setup(
    name='avalon-fsn',
    version='1.0.4',
    description='protect your source code with cython',
    py_modules=["avalon_fsn"],
    long_description="protect your source code with cython",
    url='https://gitee.com/umaru_ex/avalon-fsn',
    author='umaru',
    author_email='15875339926@139.com',
    classifiers=[],
    keywords='',
    install_requires=['cython', 'PyInstaller'],
    extras_require={},
    packages=find_packages(),
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'avalon-fsn-build=avalon_fsn.build:build',
            'avalon-fsn-release=avalon_fsn.action:release',
            'avalon-fsn-package=avalon_fsn.action:package',
        ],
    },
    project_urls={},
)
