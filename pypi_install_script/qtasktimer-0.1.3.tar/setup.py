from setuptools import setup


setup(
    name='qtasktimer',
    version='0.1.3',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    maintainer='Vasily Kuznetsov',
    maintainer_email='kvas.it@gmail.com',
    license='MIT',
    url='https://github.com/kvas-it/qtasktimer',
    description='Simple timer for timeboxing built with PyQt 5',
    py_modules=['qtasktimer'],
    install_requires=['PyQt5'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Scheduling',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={'console_scripts': ['qtt=qtasktimer:main']},
)
