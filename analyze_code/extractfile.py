from zipfile import ZipFile
import zipfile
import os
from shutil import copy
from collections import Counter
import tarfile
import bz2
sourcedir="downloadedfiles"
targetdir="dstdir"
zippedfiles=os.listdir(sourcedir)
listextension=[]
# for file in zippedfiles:
#     extension = os.path.splitext(file)[1][1:]
#     if(extension==""):
#         print(file)
#     listextension.append(extension)
# outlist=set(listextension)

# print(Counter(listextension).keys())
# print(Counter(listextension).values())
# print(outlist)

# print("end")

logfile=open("processlog\\extractfile.txt","a")
i=0

for file in zippedfiles:
    i = i+1
    try:
            unziptargetdir=os.path.join(targetdir,file)
            unziptargetdir=os.path.splitext(unziptargetdir)[0]
            unziptargetdir=os.path.join(unziptargetdir,"")
            #print(file)
            sourcefile=os.path.join(sourcedir,file)
            #print(unziptargetdir)
            # if(os.path.isdir(unziptargetdir)):
            #     print(unziptargetdir+" exist")
            #     continue
            if(os.path.isdir(unziptargetdir)):
                print(str(i)+": continued")
                continue
                
            if(not os.path.isdir(unziptargetdir)):
                os.mkdir(unziptargetdir)
                print(str(i)+": "+file+"added")
            #print(sourcefile)
            copy(sourcefile,unziptargetdir)
            zippedtargetfile=os.path.join(unziptargetdir,file)
            #print(zippedtargetfile)
            if(zipfile.is_zipfile(zippedtargetfile)):
                with ZipFile(zippedtargetfile, 'r') as zipObj:
                    try:
                        zipObj.extractall(path=unziptargetdir)
                    except ValueError:
                        logfile.write("file error: "+file+"\n")
                        print("file error: "+file)
                    zipObj.close()
            elif(zippedtargetfile.endswith("tar.gz") and tarfile.is_tarfile(zippedtargetfile)):
                try:
                    tar = tarfile.open(zippedtargetfile, "r:gz")
                    try:
                        tar.extractall(path=unziptargetdir)
                    except:
                        logfile.write("error: "+file+"\n")
                    tar.close()
                except ValueError or PermissionError:
                    logfile.write("file error: "+file+"\n")
                    print("file error: "+file)
            else:
                logfile.write("unsupport file format: " +file+"\n")
                print("unsupport file format: " +file)
    except:
        logfile.write("unknown error: " + file)
    logfile.flush()
logfile.close()







    
        
        

# os.mkdir(unzipdir+"\\test")