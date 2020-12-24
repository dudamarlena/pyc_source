from distutils.core import setup
setup(
  name='slackstatus',
  packages=['slackstatus'],
  version='0.0.2',
  license='MIT',
  description='A simple cli for setting your slack status.',
  author='Anthony Corletti',
  author_email='anthcor@gmail.com',
  url='https://github.com/anthcor/slackstatus',
  download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords=['slack', 'status', 'python3', 'dateparser'],
  install_requires=[
          'dateparser',
          'slackclient',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points = {
    'console_scripts': [
        'slackstatus = slackstatus.__main__:main'
     ]
  }
)
