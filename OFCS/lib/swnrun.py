"""
25.09.2020
SWAN çalıştıran kod
M.Burak Soran
Emre Çalışır

All right reserved. C 2020
"""

#%% Modules
import os
import glob
import datetime
import pandas as pd
from natsort import natsorted


#%% Functions


#%%

outfiles = glob.glob(globals()["out_wd"] + "/*.nc")
file_size = []


logfile=open(globals()["log_wd"] + "/output.log","w+")

writelines = []

logfile.write("createdate createtime filename size status" + "\n")

for i in range(len(outfiles)):
            
    file_size.append(os.stat(outfiles[i]).st_size/(1024*1024))
    
    if file_size[i] > 2:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(outfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
        + " "+ str(outfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
    else:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(outfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        + " "+ str(outfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
        
for i in range(len(writelines)):
    logfile.write(writelines[i] + "\n")
    
logfile.close()

swnlog = pd.read_csv(globals()["log_wd"]+"/swn.log", sep=" ")
outlog = pd.read_csv(globals()["log_wd"]+"/output.log", sep=" ")


outlog = outlog.replace("outNC", "swn", regex=True)
outlog = outlog.replace("nc", "swn", regex=True)

if outlog.shape[0] == 0:
    missingdate = natsorted(swnlog["filename"])
    
else:
    missingdate = list(set(list(swnlog["filename"])) - set(list(outlog["filename"])))
    missingdate = natsorted(missingdate)

for m in range(len(missingdate)):
    
    outdate = globals()["out_wd"] + "\outNC_" + missingdate[m].split("_")[1].split(".")[0] + ".nc"
    
    swnname = "swn_" + str(outdate).split("_")[1].split(".")[0]
    
    os.chdir(globals()["var_wd"] + "\swn")
    
    f = open("run.sh","w")

    f.write("bash swanrun -input " + swnname + " -omp 16")
    
    f.close()
    
    print(str(datetime.datetime.now()) + " Starting SWAN simulation.")
    
    os.system("bash.exe run.sh")
    
    os.chdir(globals()["main_wd"])
    
    outfiles = glob.glob(globals()["out_wd"] + "/*.nc")
    file_size = []
    
    
    logfile=open(globals()["log_wd"] + "/output.log","w+")
    
    writelines = []
    
    logfile.write("createdate createtime filename size status" + "\n")
    
    for i in range(len(outfiles)):
                
        file_size.append(os.stat(outfiles[i]).st_size/(1024*1024))
        
        if file_size[i] > 2:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(outfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
            + " "+ str(outfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
        else:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(outfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            + " "+ str(outfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
            
    for i in range(len(writelines)):
        logfile.write(writelines[i] + "\n")
        
    logfile.close()

    print(str(datetime.datetime.now()) + " SWAN simulation done.")
    
    exec(open("lib/graphic1.py").read())








