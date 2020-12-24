
import os
import shutil
src_folder="downloadefile"
dest_folder="downloadedfiles"
files = os.listdir(src_folder)
cwd=os.getcwd()
#print(cwd)
#print(files[1])
#print(os.path.join(dest_folder,files[1]))
files=files[2:-1]
for f in files:
    if(f=="downloadedfiles"):
        continue
    if(f=="movefile.py"):
        continue
    src=f
    
    dst=os.path.join(dest_folder,f)
    print(dst)
    try:
        shutil.move(src,dst)
    except:
        pass