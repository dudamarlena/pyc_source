
from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'kbtype',         # How you named your package folder (MyLib)
  packages = ['kbtype'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python module to simulate keyboard typing that works with multiple keyboard layouts',   # Give a short description about your library
  long_description = long_description,
  author = 'Niklas Ziermann',                   # Type in your name
  author_email = 'n-ziermann@protonmail.com',      # Type in your E-Mail
  url = 'https://github.com/N-Ziermann/kbtype',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/N-Ziermann/kbtype/releases/download/V1.0.0/kbtype.py',    # I explain this later on
  keywords = ["keyboard", "type", "write", "hid"],   # Keywords that define your package best
  install_requires=["pyperclip", "pyautogui"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
