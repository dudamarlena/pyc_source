from setuptools import setup, find_packages
setup(
    name='jfs',
    version='0.1.3',
    description='File Processing Library.',
    url='https://github.com/tech-pi/filesystem',
    author='Weijie Tao',
    author_email='twj2417@gmail.com',
    license='MIT',
    namespace_packages=['jfs'],
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=[
        'click',
        'rx',
        'pathlib',
        'fs',
        'doufo'
    ],
    scripts=[],
    zip_safe=False
)
