from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib
import difflib
from datetime import datetime
import os

file_suffix="releaseList.txt"
file_prefix=str(datetime.date(datetime.now()))
file_name=file_prefix+file_suffix
file = open(file_name,"w") 
html_page = urllib.urlopen("https://pypi.org/simple/")
soup = BeautifulSoup(html_page)
link_list=["a"]
i=0
for link in soup.findAll('a'):
   a=link.get('href')[8:]
   a=a[:-1]
   file.write(a)
   file.write("\n")
   link_list.append(a)
   #print(a)
   i=i+1
file.write(str(i))
print("write done\n")



