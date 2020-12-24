from setuptools import setup

package_name = 'piety'


setup(
    name=package_name,
    description='A modern curses compatible terminal built using Vulcan and GLFW',
    version='0.1.0',
    packages=[package_name],
    classifiers=[
        'Development Status :: 1 - Planning',

        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',

        'Framework :: AsyncIO',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.7',
        ],
    keywords=['vulcan', 'glfw', 'terminal', 'curses'],
    )
