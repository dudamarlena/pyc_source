from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib
import difflib
from datetime import datetime
import os
import requests
import json


html_page = urllib.urlopen("https://pypi.org/simple/")
soup = BeautifulSoup(html_page)
link_list=["a"]
i=0
for link in soup.findAll('a'):
   a=link.get('href')[8:]
   a=a[:-1]
   link_list.append(a)
   #print(a)
   i=i+1
print("name list load done\n")
i=0

url_prefix="https://pypi.python.org/pypi/"
url_suffix="/json"
for name in link_list:
   url=url_prefix+name+url_suffix
   x=requests.get(url)
   try:
      filename=name+".json"
      jsonfile = open(filename, 'w')
      data=x.json()
      json.dump(data, jsonfile)
      jsonfile.close
   except ValueError:
      #print(name)
      #print("decode error")
      i=i+1
print(i)
   





