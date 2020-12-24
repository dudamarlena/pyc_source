# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/geodadata.py
# Compiled at: 2019-11-18 22:46:38
# Size of source mod 2**32: 2239 bytes
import requests
from bs4 import BeautifulSoup

def type_of_script():
    """Helper function to determine run context"""
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'jupyter'
        if 'terminal' in ipy_str:
            return 'ipython'
    except:
        return 'terminal'


class Dataset:

    def __init__(self, name, description, n, k, download_url, explain_url):
        self.name = name
        self.description = description
        self.n = n
        self.k = k
        self.download_url = download_url
        self.explain_url = explain_url
        self.dir = name.replace(' ', '_')

    def __repr__(self):
        return '%s' % self.description

    def explain(self, width=700, height=350):
        """Describe the dataset
        """
        page = requests.get(self.explain_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text = soup.get_text(' ')
        trim_idx = text.index('DOWNLOAD DATA')
        text = text[trim_idx + len('DOWNLOAD DATA'):]
        self.text = text.replace('\xa0', ' ')
        if type_of_script() == 'jupyter':
            from IPython.display import IFrame
            return IFrame((self.explain_url), width=width, height=height)
        print(self.text)

    def json_dict(self):
        d = {}
        d['name'] = self.name
        d['description'] = self.description
        d['download_url'] = self.download_url
        d['explain_url'] = self.explain_url
        d['dir'] = self.dir
        return d


url = 'https://geodacenter.github.io/data-and-lab//'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
samples = soup.find(class_='samples')
rows = samples.find_all('tr')
datasets = {}
for row in rows[1:]:
    data = row.find_all('td')
    name = data[0].text.strip()
    description = data[1].text
    n = data[2].text
    k = data[3].text
    targets = row.find_all('a')
    download_url = targets[1].attrs['href']
    explain_url = targets[0].attrs['href']
    datasets[name] = Dataset(name, description, n, k, download_url, explain_url)