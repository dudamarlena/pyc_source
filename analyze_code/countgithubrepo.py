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
    logfile.flush()
    count_sourceforge=0
    count_github=0
    count_gitlab=0
    count_nohomepage=0
    count=0
    processflag=0
    i=0
    url_prefix="https://pypi.python.org/pypi/"
    url_suffix="/json"
    for name in link_list:
        processflag=processflag+1
        print(processflag)
        url=url_prefix+name+url_suffix
        try:
            x=requests.get(url)
        except:
            print("ConnectionError:")
            print(url)
            logfile.write("connection error: "+name+"\n")
            i=i+1
            pass
        try:
            data=x.json()
        except:
            logfile.write("json decode error: "+str(name))
            i=i+1
            continue
            #print(data)
        homepagelink=data["info"]["home_page"]
        if(homepagelink is None):
            logfile.write("error: Nonetype homepagelink"+name+" : "+str(homepagelink))
            continue
        if("github.com" in homepagelink):
            count_github=count_github+1
            continue
        if("gitlab.com" in homepagelink):
            count_gitlab=count_gitlab+1
            continue
        if("sourceforge.net" in homepagelink):
            count_sourceforge=count_sourceforge+1
            continue
        count_nohomepage=count_nohomepage+1
        try:
            logfile.write(str(name)+" "+str(homepagelink)+"\n")
        except:
            logfile.write("unknown error "+str(name)+"\n")
            i=i+1
        count=count+1
        logfile.flush()

    #print(name)
    #print("decode error")
    print(threading.current_thread().name)
    print("sum: errors:"+str(i))
    print("sum: downloaded:"+str(count))
    logfile.write(threading.current_thread().name+"sum: errors: "+str(i)+" sum: downloaded: "+str(count)+"\n")
    logfile.write(threading.current_thread().name+"github: "+str(count_github))
    logfile.write(threading.current_thread().name+"gitlab: "+str(count_gitlab))
    logfile.write(threading.current_thread().name+"sourceforge: "+str(count_sourceforge))
    logfile.write(threading.current_thread().name+"unknown: "+str(count_nohomepage))



html_page = urllib.urlopen("https://pypi.org/simple/")
soup = BeautifulSoup(html_page)
link_list=[]
i=0
logfile=open("processlog\\githubrepo.txt","a")
logfile.write("\n")
for link in soup.findAll('a'):
   a=link.get('href')[8:]
   a=a[:-1]
   link_list.append(a)
   #print(a)
   i=i+1
print("name list load done\n")
print(len(link_list))
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








