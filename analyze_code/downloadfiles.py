from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib
import difflib
from datetime import datetime
import os
import os.path
import requests
import json
import unicodedata
import re
import threading
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def downloadfile(*link_list):
    count=0
    i=0
    url_prefix="https://pypi.org/pypi/"
    url_suffix="/json"
    for name in link_list:
        url=url_prefix+name+url_suffix
        try:
            #print(url)
            x=requests.get(url,timeout=1)
        except:
            print("Connection Error:"+str(url))
            pass
        try:
            data=x.json()
            #print(data)
            if("urls" not in data):
                continue
            if(len(data["urls"])>0):
                downloadlink=data["urls"][0]["url"]
                filename=get_valid_filename(data["urls"][0]["filename"])
                filename=os.path.join("downloadedfiles",filename)
                #print(filename)
                #print(downloadlink)
                if os.path.exists(filename):
                    #print(threading.current_thread().name)
                    #print("exist")
                    continue  
                try:
                    urllib.urlretrieve(downloadlink, filename)
                    print(threading.current_thread().name+" "+filename+" "+str(count))
                    print(downloadlink)
                    count=count+1
                except:
                    print("error"+" "+downloadlink)
        except:
                i=i+1
        

      #print(name)
      #print("decode error")

    print(threading.current_thread().name)
    print("sum: errors:"+str(i))
    print("sum: downloaded:"+str(count))

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

sub_list1=link_list[0:50000]
sub_list2=link_list[50001:100000]
sub_list3=link_list[100001:150000]
sub_list4=link_list[150001:-1]
print("list_divided_done")

#downloadfile(link_list)

threads=[]
t1=threading.Thread(target=downloadfile,args=sub_list1)

t2=threading.Thread(target=downloadfile,args=sub_list2)

t3=threading.Thread(target=downloadfile,args=sub_list3)

t4=threading.Thread(target=downloadfile,args=sub_list4)

threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
for t in threads:
    t.start()








