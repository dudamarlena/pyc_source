import os

keyword = "base64"  # ask the user for keyword, use raw_input() on Python 2.x
logfile=open("processlog\\searchresult.txt","a")
logfile.write("------------------------------------------------------------")
logfile.write("search for "+keyword+"\n")
root_dir = "pycfiles"  # path to the root directory to search
count=0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir
        file_path = os.path.join(root, filename)  # build the file path
        try:
            with open(file_path, "rb") as f:  # open the file for reading
                # read the file line by line
                for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                    try:
                        line = line.decode("utf-8")  # try to decode the contents to utf-8
                    except ValueError:  # decoding failed, skip the line
                        continue
                    if keyword in line:  # if the keyword exists on the current line...
                        count=count+1
                        try:
                            logfile.write(file_path+"\n")
                            logfile.write(line+"\n")
                        except:
                            logfile.write("error")
                        print(file_path)  # print the file path
                        break
        except (IOError, OSError):  # ignore read and permission errors
            pass
logfile.write("sum : all have "+str(count)+" "+keyword)
print(count)