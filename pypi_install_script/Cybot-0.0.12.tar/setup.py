import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'Cybot',         # How you named your package folder (MyLib)
  packages = [
              'cybot/Cybot/messenger',
              'cybot/Cybot/telegram',
              'cybot/Cybot/telegram/flask',
              'cybot/Cybot/telegram/flask/json',
              'cybot/Cybot/instagram',
              'cybot/Cybot/whatsapp', 
              'cybot/Cybot/whatsapp/webwhatsapi/objects',

              ],   # Chose the same as "name"
  version = '0.0.12',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Whatsapp framework bot',   # Give a short description about your library
  long_description=long_description,
  author = 'Francis Taylor',                   # Type in your name
  author_email = 'FrancisTrapp2000@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Francis-Taylor/Cybot',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/francis-taylor/Cybot.git',    # I explain this later on
  keywords = ['whatsapp', 'Bot', 'Python', "whatsapp-bot", "framework"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'requests',
          'flask',
          'pyfiglet',
          'PythonColorize',
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
  ],python_requires='>=3.6',
)
