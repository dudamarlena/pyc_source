from distutils.core import setup
setup(
  name = 'YoutubeScraper',         # How you named your package folder (MyLib)
  packages = ['YoutubeScraper'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Scraper to get information from youtube video page',   # Give a short description about your library
  author = 'Leonardo ALchieri',                   # Type in your name
  author_email = 'l.alchieri2@campus.unimib.it',      # Type in your E-Mail
  url = 'https://github.com/LeonardoAlchieri/youtube_scraper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LeonardoAlchieri/youtube_scraper/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['Youtube', 'Scraping', 'Selenium'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'datetime',
          'bcolors',
          'lxml',
          'selenium',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
