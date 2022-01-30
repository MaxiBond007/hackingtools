# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 19:28:45 2022

@author: edinh
"""
import threading
import time
import requests

class DirbScannerThreading ():
    def __init__(self,url):
        self.url = url
        self.reachable = []
        self.unreachable = []
        self.redirected =[]
        

    def url_checker(self,line):
        try:
            self.classification(requests.head(self.url+line).status_code, line)
  
        except requests.ConnectionError:
            self.unreachable.append(line)
        
        return 0
    
    def classification(self,code,line):
        code_family = str(code)[0]
        if code_family == '2':
            self.reachable.append(self.url+line)
            
        elif code_family == '3':
            self.redirected.append(line)
            
        elif code_family == '4':
            self.unreachable.append(line)
        
    
    def run(self, wordlist_path):
        threads = list()
        temp = open(wordlist_path,'r').read().splitlines()
        #with open(wordlist_path, "r") as wordlist_file:
        for line in temp:
            x = threading.Thread(target=self.url_checker, args=(line,))
            threads.append(x)
            #print(self.url + line)
            x.start()
                 
        for index, thread in enumerate(threads):
            thread.join()   
            
        return 0



wordlist_path = "wordlist_small.txt"
URL = "https://steverequin.com/"

StartTime = time.time()
scanner = DirbScannerThreading(URL)
scanner.run(wordlist_path)
EndTime = time.time()
print(StartTime -EndTime)
print("redirected \n")
print(scanner.redirected)
print("reachable \n")
print(scanner.reachable)
print("unreachable \n")
print(scanner.unreachable)

