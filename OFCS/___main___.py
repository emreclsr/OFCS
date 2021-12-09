"""
24.09.2020
GUI den working directory çekecek.
Authors:
M.Burak Soran
Emre Çalışır
del (Bilal Bingölbali)

All right reserved. C 2020
"""

import os
import glob


globals()["marsNC_wd"] = r"D:/OFCStest/variables/marsNC"
globals()["wnd_wd"] = r"D:/OFCStest/variables/wnd"

globals()["swn_wd"] = r"D:/OFCStest/variables/swn"
globals()["hot_wd"] = r"D:/OFCStest/variables/hot"
globals()["log_wd"] = r"D:/OFCStest/logs"
globals()["bin_wd"] = r"D:/OFCStest/bin"
globals()["out_wd"] = r"D:/OFCStest/output"
globals()["gra_wd"] = r"D:/OFCStest/graphics"
globals()["vid_wd"] = r"D:/OFCStest/videos"
globals()["var_wd"] = r"D:/OFCStest/variables"
globals()["main_wd"] = r"D:/OFCStest"


exec(open("lib/marsNC.py").read())


