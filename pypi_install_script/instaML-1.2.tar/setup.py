from distutils.core import setup
setup(
  name = 'instaML',         # How you named your package folder (MyLib)
  packages = ['instaML'],   # Chose the same as "name"
  version = '1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'It is a python package to ease the process of applying concepts of machine learning and deep learning',   # Give a short description about your library
  author = 'Vikneshwar Selvam',                   # Type in your name
  author_email = 'selvamvikneshwar@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/vikneshwarselvam/instaML',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vikneshwarselvam/instaML/archive/v1.2.tar.gz',    # I explain this later on
  keywords = ['Easy', 'Simple', 'Best'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'face_recognition',
          'face_recognition_models',
          'Pillow',
          'dlib',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
