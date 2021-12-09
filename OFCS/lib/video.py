# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:26:09 2020
Emre Çalışır
M.Burak Soran

"""

#%% Modules
import cv2
import os
from natsort import natsorted
from tqdm import tqdm
import pandas as pd
import numpy as np
from PIL import Image


#%% Functions



#%%

outlog = pd.read_csv(globals()["log_wd"]+"/output.log", sep=" ")

files = list(outlog["filename"])

date = files[-1].split("_")[1].split(".")[0]



image_folder = globals()["gra_wd"] + "\\" + date
video_name = globals()["vid_wd"] + "\\" + date + "_del.mp4"

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = natsorted(images)






logo = Image.open(globals()["bin_wd"] + "/uu_logo.png")
logo = logo.resize((300,300))
# logo1 = Image.open(globals()["bin_wd"] + "/uu_logo.png")
# logo1 = logo1.resize((1200,1200))
# logo1.putalpha(100)


loop= tqdm(total = len(images), position=0, leave=False)

for i in range(len(images)):
    png = Image.open(globals()["gra_wd"] + "/" + date + "/" + images[i])
    
    png.paste(logo, (120,200), logo)
    # png.paste(logo1, (800,200), logo1)
    
    # png.show()
    
    png.save(globals()["gra_wd"] + "/" + date + "/" + images[i])
    
    loop.set_description("Logo Printing.....".format(i))
    loop.update(1)
loop.close()      








frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape


video = cv2.VideoWriter(video_name, 0, 5, (width,height))


i=0
loop= tqdm(total = len(images), position=0, leave=False)

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))
    
    
    i+=1
    loop.set_description("Preparing Video.....".format(i))
    loop.update(1)
loop.close()  


cv2.destroyAllWindows()
video.release()


 
cap = cv2.VideoCapture(video_name)
 
fourcc = cv2.VideoWriter_fourcc(*'X264')

outvideo = globals()["vid_wd"] + "\\" + date + ".mp4"


out = cv2.VideoWriter(outvideo,fourcc, 5, (1500,780))
 
while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,(1500,780),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
os.remove(video_name)


