from distutils.core import setup
setup(
  name = 'ArrayMath2D',         # How you named your package folder (MyLib)
  version = '0.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple 2D Math',   # Give a short description about your library
  author = 'Array',                   # Type in your name
  author_email = 'ars2062@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/ars2062/2dmath',   # Provide either the link to your github or to your website
  keywords = ['2d', 'math', 'vector', 'trigonometry'],   # Keywords that define your package best
  install_requires=[],
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
    'Programming Language :: Python :: 3.8',
  ],
  python_requires='>=3.5'
)