from setuptools import setup, find_packages
setup(
    name='icefun-prog',
    packages=find_packages(),
    install_requires=['pyserial'],
    version='2.0.0',
    description='Programmer for the iceFUN FPGAs https://www.robot-electronics.co.uk/icefun.html)',
    author='Petr Otoupal',
    author_email='petr.otoupal@gmail.com',
    url='https://github.com/pitrz/icefunprog',
    keywords=['fpga', 'icefun', 'programmer', 'bitstream'],
    license='GNU General Public License v3.0',
    classifiers=[],
    entry_points={
        'console_scripts':[
            'icefunprog = icefunprog.__main__:main'
        ]
    },
)