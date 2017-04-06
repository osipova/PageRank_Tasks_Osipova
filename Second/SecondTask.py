# -*- coding: utf8 -*-

import numpy as np
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import time

#first task
def check(item):  
    try:
        html_page = urllib.urlopen(item)
        soup = BeautifulSoup(html_page, "html.parser")
        result = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http(s)?://")}):
            s = link.get('href')
            if not s.endswith('.jpg') and not s.endswith('.png') and not s.endswith('.gif') and not s.endswith(
                    '.jpeg') and not s.endswith('.pdf'): 
                result.append(s)
        return result
    except:
        return -1

t = time.perf_counter()
sites = ["http://kpfu.ru/"]
a = np.zeros((1, 1), dtype=np.uint8)

i = 0  
len_sites = len(sites)  
full = False 

while i < len_sites:  
    all_new = check(sites[i])

    if type(all_new) is list and len(all_new):  
        set_new = set(all_new)
        old = set_new & set(sites) 

        if full or len_sites > 100: #if amount of links > 100 then do not add new links
            full = True

            if not len(old):  
                sites.remove(sites[i])  
                a = np.delete(a, i, 1)
            else:
                for j in old:
                    a[i, sites.index(j)] = 1 
                a = np.append(a, np.zeros([1, len(a[0])], dtype=np.uint8), 0) 

                i += 1
        else:
            new = set_new - set(sites) 

            if not len(new) and not len(old):  
                sites.remove(sites[i]) 
                a = np.delete(a, i, 1)
            else:
                a = np.append(a, np.zeros([len(a), len(new)], dtype=np.uint8),
                              1)  

                for j in old: 
                    a[i, sites.index(j)] = 1

                for j in range(len_sites, len_sites + len(new)):
                    a[i, j] = 1

                sites += new  
                a = np.append(a, np.zeros([1, len(a[0])], dtype=np.uint8), 0) 
                i += 1
    else:
        sites.remove(sites[i])  
        a = np.delete(a, i, 1)

    len_sites = len(sites)  
    print('{}/{}'.format(i, len_sites))  

a = np.delete(a, (-1), axis=0) 
np.fill_diagonal(a, 0)
#end first task

P = np.zeros(a.shape) #PageRank array

len_a = len(a)
#print ("len_a=", len_a)

#filling array by alghoritm 
for i in range(len_a):
    #print("i=", i)
    s = sum(a[i])
    #print ("s=", s)
    if s > 0:
        #print(True)
        for j in range(len_a):
            #print("j=", j)
            P[j, i] = 1 / s if a[i, j] == 1 else 0
            #print ("P=",P[j, i])
    else:
        #print(False)
        for j in range(len_a):
            #print("j=", j)
            P[j, i] = 1 / len_a
            #print ("P=",P[j, i])
            #print(sites[i])
#print (P)            
np.savetxt('matrix.txt', a, fmt='%d')
np.savetxt('p.txt', P, fmt='%10.5f')

#filling x by alghoritm 
k = 100  #Iterations
x = np.array([1 / len_a for i in range(len_a)])  
while k >= 0:  
    x = P @ x
    k -= 1

#sort by rang
sort = x.argsort()
print(list(reversed([sites[i] for i in sort])))
print(list(reversed([x[i] for i in sort])))
print('------------------------------')
    
print("Work time of program:")   
print(time.perf_counter() - t)