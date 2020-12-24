deskripsi = """

1.Simple Send Data To Web

>>> # How To Send
>>> import wesnd
>>> wesnd.dns('code')


"""

from distutils.core import setup

setup(
  name = 'sdw',         # How you named your package folder (MyLib)
  packages = ['sdw'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple Modules Encode code python',   # Give a short description about your library
  long_description = deskripsi,
  author = 'Mr XsZ',                   # Type in your name
  author_email = 'wareares@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Mr-XsZ',   # Provide either the link to your github or to your website
  keywords = ['encode', 'python', 'pythonencode'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
