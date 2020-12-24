from setuptools import setup, find_packages

setup(
    name='visitor_mark_down',
    version='0.0.1',
    url='https://github.com/dozymoe/visitor_mark_down',
    download_url='https://github.com/dozymoe/visitor_mark_down/tarball/0.0.1',
    author='Fahri Reza',
    author_email='dozymoe@gmail.com',
    description='Advance strip_tags().',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    install_requires=[],
)
