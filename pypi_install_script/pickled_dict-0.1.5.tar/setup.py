from distutils.core import setup

setup(name='pickled_dict',  # How you named your package folder (MyLib)
      packages=['pickled_dict'],  # Chose the same as "name"
      version='0.1.5',  # Start with a small number and increase it with every change you make
      license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
      description='Have a persistant Dictionary saved as file',  # Give a short description about your library
      author='David Brielbeck',  # Type in your name
      author_email='dbrielbeck@gmail.com',  # Type in your E-Mail
      url='https://github.com/Daveismus/pickled_dict',  
      download_url='https://github.com/Daveismus/pickled_dict/archive/0.1.tar.gz',
      keywords=['pickle', 'dict', 'peristant'],  # Keywords that define your package best
      classifiers=['Development Status :: 3 - Alpha',
                   # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
                   'Intended Audience :: Science/Research',  # Define that your audience are developers
                   'Topic :: Software Development :: Build Tools',
                   'License :: OSI Approved :: MIT License',  # Again, pick a license
                   'Programming Language :: Python :: 3',
                   # Specify which pyhton versions that you want to support
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8', ], )
