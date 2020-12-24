from setuptools import setup

setup(name='mygame',
      version='0.1.2',
      description='My misguided attempt to do something interesting.',
      url='https://bitbucket.org/mradecki/mygame',
      author='Marek Radecki',
      author_email='marek.radecki@gmail.com',
      license='MIT',
      packages=['mygame'],
      install_requires=[
        'cocos2d'
      ],
      tests_requre=['pytest'],
      entry_points = {
        'console_scripts': ['my-game=mygame.command_line:main']
      },
      test_suite='mygame.tests',
      zip_safe=False,
      include_package_data=True,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Games/Entertainment :: Arcade',
        'Programming Language :: Python :: 3.5',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License'
      ]
)