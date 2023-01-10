#coding=utf-8
###############################
#   HansLimon on 2023/01/10   #
#                             #
#       for public use        #
#                             #
#     CopyLEFT Mongrokey      #
###############################
import paramiko
import sys
from win32api import MessageBox
from win32con import MB_OK

print("[Info] Initialize success")

goalfile = sys.argv[1]

filename = goalfile.split("\\")[-1]
print(f"got {filename}")
targetFile = ""# Notice: edit it on your own, this determines where the file will be created on the server

transport = paramiko.Transport(('', 22))# Example: '192.168.2.1', 22(port)

print("[Info] port connected")

transport.connect(username='', password='')

input("[Notice] Connection established, press <Enter> to continue.")

sftp = paramiko.SFTPClient.from_transport(transport)

print("[Info] SFTP command sent")

sftp.put(goalfile, targetFile)
#sftp.get(cpFile, data_file)
transport.close()

MessageBox(0, f"{goalfile} - 文件传输成功", "", MB_OK)

input("[Notice] Process finished, type <Enter> to exit.")