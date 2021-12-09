"""
27.09.2020
Grafik çizen kod
Emre Çalışır
M.Burak Soran

All right reserved. C 2020
"""

#%% Modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import os
import matplotlib as mpl
os.environ['PROJ_LIB'] = r"C:\anaconda3\Lib\site-packages\mpl_toolkits\basemap"

from mpl_toolkits.basemap import Basemap
import matplotlib.tri as tri
import datetime
import gc
import matplotlib.image as image
import matplotlib.patheffects as pe
from tqdm import tqdm



outlog = pd.read_csv(globals()["log_wd"]+"/output.log", sep=" ")

files = list(outlog["filename"])

date = files[-1].split("_")[1].split(".")[0]


ncfile = globals()["out_wd"] + "\\" + files[-1]

nc = Dataset(ncfile,"r")

lat = np.asarray(nc.variables["latitude"][:])
long = np.asarray(nc.variables["longitude"][:])
hs = np.asarray(nc.variables["hs"][:])
dirr = np.asarray(nc.variables["theta0"][:])
time = np.asarray(nc.variables["time"][:])

dirr[dirr == -32768] = np.nan


shape = (1960,760)

os.mkdir(globals()["gra_wd"] + "\\" + date) 

mask = np.loadtxt(globals()["main_wd"] + "\\mask760x1960.mask")


# gc.enable()

xi =np.linspace(min(long),max(long),shape[0])
yi =np.linspace(min(lat),max(lat),shape[1])


loop= tqdm(total = time.shape[0], position=0, leave=False)
for i in range(time.shape[0]):
    
    

    triang = tri.Triangulation(long, lat)
    interpolator = tri.LinearTriInterpolator(triang, hs[i])
    Xi, Yi = np.meshgrid(xi, yi)
    h = interpolator(Xi, Yi)
    
    hm = h+mask
    
    hm[hm > 90000] = np.nan
    
    
    interpolator = tri.LinearTriInterpolator(triang, dirr[i])
    d = interpolator(Xi, Yi)
    
    dm = d+mask
    
    dm[dm > 90000] = np.nan
    
    Dir_x = np.cos(np.radians(dm))
    Dir_y = np.sin(np.radians(dm))
    
    
    
    fig = plt.figure(figsize=(25,13), dpi= 100)

    plt.rcParams['axes.facecolor'] = 'slategrey'
    
    m = Basemap(projection='cyl', \
            llcrnrlat=29, urcrnrlat=48, \
            llcrnrlon=-7, urcrnrlon=42, \
            lat_ts=None, \
            resolution='i')
    
    m.bluemarble(scale=1)
    
    m.drawcountries(color='dimgray', linewidth=3, zorder=0.9)

    

    # m.drawcoastlines(color='w', linewidth=1.5, zorder=0.9)  # add coastlines
    
    
    
    # m.fillcontinents(color='w', zorder=0.8, lake_color="w")
    
    # im = image.imread(globals()["bin_wd"] + "/uu_logo.png")
    
    # plt.imshow(im, aspect='auto', extent=(-4, 0, 43, 47), zorder=1)
    
    x = 0
    y = 0
    for x in range(0,Dir_x.shape[0],30):  
        for y in range(0,Dir_x.shape[1],50): 
            
            
            lenght = (Dir_x[x][y]**2 + Dir_y[x][y]**2)**0.5
            xx = (Dir_x[x][y]/lenght)*1.2
            yy = (Dir_y[x][y]/lenght)*1.2
    
            plt.quiver(xi[y], yi[x], xx, yy, zorder=0.7, scale=90,
                       width=0.0015, headwidth=5, headlength=3, headaxislength=3, color="w")
    
    mini = 0
    maxi = np.nanmax(hs)+0.2
    
    data_range = np.arange(mini,maxi,0.05)
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    plt.contourf(xi, yi, hm, data_range, cmap="jet",zorder=0.6, norm=norm)
    
        
    plt.annotate("Coastal Engineering Team / Bursa Uludag University", (18.5, 29.5), fontsize=26, color="w", weight="bold",
                 ha='center', va='center',path_effects=[pe.withStroke(linewidth=4, foreground="k")])
    
    currenttime = datetime.datetime.fromtimestamp(time[i], datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    plt.title(str(currenttime) + " UTC Significant Wave Height (m) & Wave Direction", fontsize=26)
    
    
    plt.xticks(np.arange(-6, 43, step=2), fontsize=20)
    plt.yticks(np.arange(29, 49, step=2), fontsize=20)
    
    plt.xlabel("Longitude", fontsize=20)
    plt.ylabel("Latitude", fontsize=20)
    
    
    fig.tight_layout()
    
    cbar_ax1 = fig.add_axes([0.07, 0.03, 0.88, 0.03])
    
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    
    cb1 = mpl.colorbar.ColorbarBase(cbar_ax1, cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal',format="%.2f")
    cbar_ax1.tick_params(labelsize=20)
    
    
    
    
    

     
    plt.savefig(globals()["gra_wd"] + "\\" + date + "\\" + str(i) + ".png")
    
    # plt.savefig(r"D:\OFCStest\graphics\2020-10-22test/" + str(i) + ".png")
    
    # gc.collect()

    plt.close()
    fig.clear()
    fig.clf()
    
    # del xi, yi, triang,interpolator, d, dm, h, hm, fig, m, x, y



    loop.set_description("Make Some Graph.....".format(i))
    loop.update(1)
loop.close()    
    
exec(open("lib/video.py").read())

gc.collect()
#  mask oluşturma

# mask = np.zeros((760,1960))

# for e in range(mask.shape[0]):
#     for f in range(mask.shape[1]):
#         if m.is_land(Xi[e,f],Yi[e,f]) == True:
#             mask[e,f] = 999999
#         else:
#             mask[e,f] = 0
        
#         print(str(e) +" "+ str(f) +" done.")
        
# np.savetxt("mask760x1960.mask", mask, fmt="%.0f")









