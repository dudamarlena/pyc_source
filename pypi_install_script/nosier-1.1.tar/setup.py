import nosier.constants
import setuptools

setuptools.setup(name='nosier',
                 version=nosier.constants.VERSION_NUMBER,
                 description='Monitors paths and upon detecting changes runs the specified command',
                 long_description=open('README').read().strip(),
                 author='Meme Dough',
                 author_email='memedough@gmail.com',
                 url='http://bitbucket.org/memedough/nosier/overview',
                 packages=['nosier'],
                 install_requires=['inotifyx'],
                 entry_points={'console_scripts': ['nosier = nosier.nosier:main']},
                 license='MIT License',
                 zip_safe=False,
                 keywords='py.test pytest nose nosetest nosy auto test runner',
                 classifiers=['Development Status :: 5 - Production/Stable',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: POSIX :: Linux',
                              'Programming Language :: Python',
                              'Topic :: Software Development :: Testing'])
