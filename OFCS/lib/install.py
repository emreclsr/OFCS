# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 22:31:36 2020

@author: HP
"""
# import os


# os.system("dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")




import win32com.shell.shell as shell
commands = 'dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart'
shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)