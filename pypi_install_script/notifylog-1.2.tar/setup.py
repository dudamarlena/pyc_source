from setuptools import setup


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='notifylog',
    version='1.2',
    author='George P.',
    author_email='digitalduke@gmail.com',
    description='org.freedesktop.Notifications eavesdropper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/digitalduke/notify-log',
    packages=[
        'notifylog',
    ],
    install_requires=[
        'dbus-python==1.2.16',
        'PyGObject==3.34.0',
        'colorama==0.4.3',
        'beautifulsoup4 >=4.8.2, <4.9',
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'notify-log=notifylog.notifylog:run',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Topic :: Utilities',
    ],
)
