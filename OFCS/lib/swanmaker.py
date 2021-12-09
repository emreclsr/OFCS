"""
25.09.2020
SWN dosyası hazırlayan kod
M.Burak Soran
Emre Çalışır

All right reserved. C 2020
"""

#%% Modules
import os
import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np
import datetime
from natsort import natsorted


#%% Functions

    


#%%

swnfiles = glob.glob(globals()["swn_wd"] + "/*.swn")
file_size = []


logfile=open(globals()["log_wd"] + "/swn.log","w+")

writelines = []

logfile.write("createdate createtime filename size status" + "\n")

for i in range(len(swnfiles)):
            
    file_size.append(os.stat(swnfiles[i]).st_size)
    
    if file_size[i] > 0:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(swnfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
        + " "+ str(swnfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "bytes done"))
    else:
        writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(swnfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        + " "+ str(swnfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "bytes error"))
        
for i in range(len(writelines)):
    logfile.write(writelines[i] + "\n")
    
logfile.close()

wndlog = pd.read_csv(globals()["log_wd"]+"/wnd.log", sep=" ")
swnlog = pd.read_csv(globals()["log_wd"]+"/swn.log", sep=" ")

wndlog = wndlog.replace("wnd", "swn", regex=True)


if swnlog.shape[0] == 0:
    missingdate = natsorted(wndlog["filename"])
    
else:
    missingdate = list(set(list(wndlog["filename"])) - set(list(swnlog["filename"])))
    missingdate = natsorted(missingdate)



for m in range(len(missingdate)):
    
    ncfile = globals()["marsNC_wd"] + "\marsNC_" + missingdate[m].split("_")[1].split(".")[0] + ".nc"
    
    nc = Dataset(ncfile,"r")
    
    time = np.asarray(nc.variables["time"][:],dtype=np.float64)*60*60
    
    diff = (datetime.datetime(1900, 1, 1, 0, 0)-datetime.datetime(1970,1,1)).total_seconds()
    
    firsttime = datetime.datetime.fromtimestamp(np.nanmin(time)+diff, datetime.timezone.utc).strftime("%Y%m%d:%H%M%S")
    lasttime = datetime.datetime.fromtimestamp(time[3*24]+diff, datetime.timezone.utc).strftime("%Y%m%d:%H%M%S")



    readdefault = open(globals()["bin_wd"]+"\default.swn","rt")
    
    data = readdefault.read()
    
    
    WindStart = firsttime
    WindStop = lasttime

    WindFileName = missingdate[m].replace("swn", "wnd")    
    SpatialSaveName = missingdate[m].replace("swn", "nc").replace("nc_", "outNC_")
    
    SimStart = WindStart
    SimStop = WindStop

    
    data = data.replace("11111111:222222",str(WindStart))
    data = data.replace("33333333:444444",str(WindStop))

    data = data.replace("ERA5_1996.wnd",str(WindFileName))
    data = data.replace("spatial.nc",str(SpatialSaveName))
    
    data = data.replace("00000000:000000",str(SimStart))
    data = data.replace("99999999:999999",str(SimStop))
    
    data = data.replace("00000000", str(SimStart)[:8])
    data = data.replace("99999999", str(SimStop)[:8])
    
    newswn = open(globals()["swn_wd"] + "/"+ missingdate[m], "w")
    
    newswn.write(data)
    
    newswn.close()

    nc.close()

    swnfiles = glob.glob(globals()["swn_wd"] + "/*.swn")
    file_size = []
    
    
    logfile=open(globals()["log_wd"] + "/swn.log","w+")
    
    writelines = []
    
    logfile.write("createdate createtime filename size status" + "\n")
    
    for i in range(len(swnfiles)):
                
        file_size.append(os.stat(swnfiles[i]).st_size)
        
        if file_size[i] > 0:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(swnfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
            + " "+ str(swnfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "bytes done"))
        else:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(swnfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            + " "+ str(swnfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "bytes error"))
            
    for i in range(len(writelines)):
        logfile.write(writelines[i] + "\n")
        
    logfile.close()
    
    print(str(datetime.datetime.now()) + " swn files ready for SWAN.")

exec(open("lib/swnrun.py").read())







