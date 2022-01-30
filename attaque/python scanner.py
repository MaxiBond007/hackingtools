# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 22:31:41 2021

@author: edinh
"""
from socket import *
import time
import threading
startTime = time.time()


def pingScan(hostnameIP,numberOfPortsToScan):

    print ('Starting scan on host: ', hostnameIP)
    for i in range(1, numberOfPortsToScan):
      s = socket(AF_INET, SOCK_STREAM)
      
      conn = s.connect_ex((hostnameIP, i))
      if(conn == 0) :
         print(f'Port {i}: OPEN')
      s.close()
    return 0

def newPingScan(hostnameIP,portToScan):

    #print ('Starting scan on port: ', portToScan)
    
    s = socket(AF_INET, SOCK_STREAM)
    
    conn = s.connect_ex((hostnameIP, portToScan))
    if(conn == 0) :
       print(f'Port {portToScan}: OPEN')
    s.close()
    return 0

def scanThread(numbertest):
    threads = list()
    for index in range(numbertest):
        x = threading.Thread(target=newPingScan, args=("127.0.0.1",index,))
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()
    return 0


print("running")
StartTime = time.time()
#pingScan("127.0.0.1",50)
scanThread(500)
EndTime = time.time()
print(EndTime-StartTime)

StartTime = time.time()
pingScan("127.0.0.1",10)
#scanThread(500)
EndTime = time.time()
print(EndTime-StartTime)