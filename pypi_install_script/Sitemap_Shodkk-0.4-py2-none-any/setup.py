from setuptools import setup

setup(name='Sitemap_Shodkk',
      version='0.1',
      description='A plugin to get the Sitemap of Any website',
      long_description=redme(),
      long_description_content_type="text/x-rst/mardown",
      url='https://shodkk.com/scrapy-libraries/sitemap_index.html',
      author='Shantanu Bombatkar',
      author_email='shodkk_shantanu@gmail.com',
      license='MIT',
      packages=['sitemap_shodkk'],
      install_requires= ["BeautifulSoup", "requests "]
      zip_safe=False)
