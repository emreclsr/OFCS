"""
25.09.2020
ECMWF'den inen nc dosyalarını SWAN da kullanmak için wnd yapan kod
Emre Çalışır
M.Burak Soran


All right reserved. C 2020
"""

#%% Modules
import os
import glob
import datetime
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from natsort import natsorted



#%% Functions



#%%

wndfiles = glob.glob(globals()["wnd_wd"] + "/*.wnd")
file_size = []


logfile=open(globals()["log_wd"] + "/wnd.log","w+")

writelines = []

logfile.write("createdate createtime filename size status" + "\n")

for i in range(len(wndfiles)):
            
    file_size.append(os.stat(wndfiles[i]).st_size/(1024*1024))
    
    if file_size[i] > 3:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(wndfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
        + " "+ str(wndfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
    else:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(wndfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        + " "+ str(wndfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
        
for i in range(len(writelines)):
    logfile.write(writelines[i] + "\n")
    
logfile.close()

marsNClog = pd.read_csv(globals()["log_wd"]+"/marsNC.log", sep=" ")
wndlog = pd.read_csv(globals()["log_wd"]+"/wnd.log", sep=" ")

marsNClog = marsNClog.replace("marsNC", "wnd", regex=True)
marsNClog = marsNClog.replace("nc", "wnd", regex=True)


if wndlog.shape[0] == 0:
    missingdate = natsorted(marsNClog["filename"])
    
else:
    missingdate = list(set(list(marsNClog["filename"])) - set(list(wndlog["filename"])))
    missingdate = natsorted(missingdate)

for m in range(len(missingdate)):
    
    
    ncfile = globals()["marsNC_wd"] + "\marsNC_" + missingdate[m].split("_")[1].split(".")[0] + ".nc"
    
    nc = Dataset(ncfile,"r")
    
    uas = np.asarray(nc.variables["u10"][:])
    vas = np.asarray(nc.variables["v10"][:])
    
    wnd = np.zeros((uas.shape[0]*2,uas.shape[1]*uas.shape[2]))
    
    a=0
    b=0
    for i in range(uas.shape[0]):
        for j in range(uas.shape[1]):
            wnd[a][b:uas.shape[2]+b] = uas[i][j]
            wnd[a+1][b:uas.shape[2]+b] = vas[i][j]
            
            b += uas.shape[2]
        
        a += 2
        b=0
        
    savename = globals()["wnd_wd"] + "\\" +  missingdate[m]
        
    np.savetxt(savename, wnd, fmt="%.3f", delimiter=" ")
    
    
    nc.close()

    wndfiles = glob.glob(globals()["wnd_wd"] + "/*.wnd")
    file_size = []
    
    
    logfile=open(globals()["log_wd"] + "/wnd.log","w+")
    
    writelines = []
    
    logfile.write("createdate createtime filename size status" + "\n")
    
    for i in range(len(wndfiles)):
        
        x = os.stat(wndfiles[i]).st_size        
        
        file_size.append(x/(1024*1024))
        
        if file_size[i] > 3:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(wndfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
            + " "+ str(wndfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
        else:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(wndfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            + " "+ str(wndfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
            
    for i in range(len(writelines)):
        logfile.write(writelines[i] + "\n")
        
    logfile.close()
    
    print(str(datetime.datetime.now()) + " Wind output ready for SWAN.")
    
exec(open("lib/swanmaker.py").read())















