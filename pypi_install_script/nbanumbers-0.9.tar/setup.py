from setuptools import setup

setup(name='nbanumbers',
      version='0.9',
      description='nbanumbers: a simple nba stats retrieval package',
      url='http://github.com/sidharthrajaram/nbanumbers',
      author='Sid Rajaram',
      author_email='tmzturtle@gmail.com',
      long_description="Easily get season stats of any current NBA player. To retrieve a tensor of a player's stats, catch the result of nbanumbers.stats(PLAYER_NAME_STRING).",
      license='MIT',
      packages=['nbanumbers'],
      install_requires=['google-api-python-client','pandas',
      'urllib3','bs4','requests','numpy','regex'],
      zip_safe=False)

