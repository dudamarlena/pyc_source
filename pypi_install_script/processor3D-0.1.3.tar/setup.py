import setuptools


setuptools.setup(
    name = 'processor3D',
    version = '0.1.3',
    packages = setuptools.find_packages('src'),
    package_dir = {"":'src'},
    #packages = setuptools.find_namespace_packages(where),
    author = 'Roman Dvorak',
    author_email = 'dvorak.roman@thunderfly.cz',
    description = '',
    data_files=[
        ("resources", ("src/resources/Slic3r-1.3.1.AppImage",))
    ],
    #packages = setuptools.find_packages(),
    classifiers = [
	'Development Status :: 3 - Alpha',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.6',
    ],
    keywords = ['3Dprint', 'Slicing', 'gcode'],
    install_requires=[
	'termcolor',
    ],
    python_requies='>3.6',
    scripts=['processor3D']
)
