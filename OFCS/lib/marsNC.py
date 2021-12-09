"""
24.09.2020
ECMWF'den forecast indirmeye yarayan kod.
Authors:
M.Burak Soran
Emre Çalışır

All right reserved. C 2020
"""

#%% Modules

import os
import gc
import time 
import glob
import datetime
import pickle

#%% Functions

def wind(wind_date):
    from ecmwfapi import ECMWFService
      
    server = ECMWFService("mars")
    server.execute({
            "dataset" : "mars",
            "class"   : "od",
            "date"    : wind_date,
            "expver"  : "1",
            "levtype" : "sfc",
            "param"   : "165.128/166.128",
            "step"    : "0/1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/70/71/72/73/74/75/76/77/78/79/80/81/82/83/84/85/86/87/88/89/90/93/96/99/102/105/108/111/114/117/120/123/126/129/132/135/138/141/144/150/156/162/168/174/180/186/192/198/204/210/216/222/228/234/240",
            "stream"  : "oper",
            "time"    : "00:00:00",
            "type"    : "fc",
            "grid"    : "0.125/0.125",
            "area"    : "48/-7/29/42",
            "format"  : "netcdf"},
            globals()["marsNC_wd"] + "/" + "marsNC_"+ str(wind_date) +".nc")
    
            




#%%

while True:
    

    marsNCfiles = glob.glob(globals()["marsNC_wd"] + "/*.nc")
    file_size = []
    
    
    logfile=open(globals()["log_wd"] + "/marsNC.log","w+")
    
    logfile.write("createdate createtime filename size status" + "\n")
    
    writelines = []
    
    for i in range(len(marsNCfiles)):
                
        file_size.append(os.stat(marsNCfiles[i]).st_size/(1024*1024))
        
        if file_size[i] > 3:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
            + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
        else:
            writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB error"))
            
    for i in range(len(writelines)):
        logfile.write(writelines[i] + "\n")
        
    logfile.close() 
    
    
    log=open(globals()["log_wd"] + "/marsNC.log","r")
    
    lastline= log.readlines()[-1]
    
    last= lastline.split(" ")[-1]
    
    if last == "done" + "\n":
        years = int(lastline.split("_")[1].split("-")[0])
        months = int(lastline.split("_")[1].split("-")[1])
        days = int(lastline.split("_")[1].split("-")[2].split(".")[0])
        
        second =((datetime.datetime(years, months, days)-datetime.datetime(1970,1,1)).total_seconds())
          
        try: 
            newsecond = second+86400
            newdate = datetime.datetime.fromtimestamp(newsecond,datetime.timezone.utc).strftime("%Y-%m-%d")
            
            wind(newdate)
            
            marsNCfiles = glob.glob(globals()["marsNC_wd"] + "/*.nc")
            file_size = []
            
            
            logfile=open(globals()["log_wd"] + "/marsNC.log","w+")
            
            logfile.write("createdate createtime filename size status" + "\n")
            
            writelines = []
            
            for i in range(len(marsNCfiles)):
                        
                file_size.append(os.stat(marsNCfiles[i]).st_size/(1024*1024))
                
                if file_size[i] > 3:
                    writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
                    + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
                else:
                    writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
                    + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB error"))
                    
            for i in range(len(writelines)):
                logfile.write(writelines[i] + "\n")
                
            logfile.close()  
            
            exec(open("lib/wnd.py").read())
        
        except:
            pass
            
    if last == "error" + "\n":
        years = int(lastline.split("_")[1].split("-")[0])
        months = int(lastline.split("_")[1].split("-")[1])
        days = int(lastline.split("_")[1].split("-")[2].split(".")[0])
        
        second =((datetime.datetime(years, months, days)-datetime.datetime(1970,1,1)).total_seconds())
        
        try: 
            newsecond = second
            newdate = datetime.datetime.fromtimestamp(newsecond,datetime.timezone.utc).strftime("%Y-%m-%d")
            
            wind(newdate)
      
            marsNCfiles = glob.glob(globals()["marsNC_wd"] + "/*.nc")
            file_size = []
            
            
            logfile=open(globals()["log_wd"] + "/marsNC.log","w+")
            
            logfile.write("createdate createtime filename size status" + "\n")
            
            writelines = []
            
            for i in range(len(marsNCfiles)):
                        
                file_size.append(os.stat(marsNCfiles[i]).st_size/(1024*1024))
                
                if file_size[i] > 3:
                    writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
                    + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
                else:
                    writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
                    + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB error"))
                    
            for i in range(len(writelines)):
                logfile.write(writelines[i] + "\n")
                
            logfile.close()  
    
            exec(open("lib/wnd.py").read())
        
        except:
            pass
    
    log.close()
      
    # marsNCfiles = glob.glob(globals()["marsNC_wd"] + "/*.nc")
    # file_size = []
    
    
    # logfile=open(globals()["log_wd"] + "/marsNC.log","w+")
    
    # logfile.write("createdate createtime filename size status" + "\n")
    
    # writelines = []
    
    # for i in range(len(marsNCfiles)):
                
    #     file_size.append(os.stat(marsNCfiles[i]).st_size/(1024*1024))
        
    #     if file_size[i] > 3:
    #         writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) 
    #         + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB done"))
    #     else:
    #         writelines.append(str(datetime.datetime.fromtimestamp(os.path.getctime(marsNCfiles[i]),datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
    #         + " "+ str(marsNCfiles[i].split("\\")[1] + " " + str(round(file_size[i],2)) + "MB error"))
            
    # for i in range(len(writelines)):
    #     logfile.write(writelines[i] + "\n")
        
    # logfile.close()  
    
    # now = ((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds())
    
    # later = newsecond+36000
    
    # laterdate = datetime.datetime.fromtimestamp(later,datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
     
    import time
    
    # print("\n Next try will be start at " + str(laterdate))
    
    # time.sleep(later-now)
    
    gc.collect()
    
    time.sleep(7200)
    
    pass
               


