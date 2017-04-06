# -*- coding: utf8 -*-

import numpy as np
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import time

#function to get links
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
sites = ["http://kpfu.ru/"]  #root link
links = []

i = 0 #number of site in queue
len_sites = len(sites)  #Number of sites
full = False  #queue

while i < len_sites:  
    all_new = check(sites[i])  #get list of links

    if type(all_new) is list and len(all_new):  
        set_new = set(all_new)
        old = (set_new & set(sites)) - {sites[i]}  #cheking that elements are in queue

        if full or len_sites > 100: #if amount of links > 100 then do not add new links
            full = True

            if not len(old):  #nothing add
                sites.remove(sites[i]) #remove from queue
                for l in links:
                    if i in l:
                        l.remove(i)
            else:
                old_indices = [sites.index(i) for i in old]
                links.append(old_indices)

            i += 1
        else:
            new = set_new - set(sites) #elements which are not in queue

            if not len(new) and not len(old):  #if nothing add
                sites.remove(sites[i]) #remove from queue
                for l in links:
                    if i in l:
                        l.remove(i)
            else:
                # adding indexes to sparse matrix
                old_indices = [sites.index(i) for i in old]
                links.append(old_indices+list(range(len_sites, len_sites + len(new) + 1)))

                sites += new  #add to queue
                i += 1
    else:
        sites.remove(sites[i]) 
        for l in links:
            if i in l:
                l.remove(i)

    len_sites = len(sites) #update amount of elements
    print('{}/{}'.format(i, len_sites))  #cheking progress

for ind, l in enumerate(links): #remove links to itself
    if ind in l:
        l.remove(ind)

len_links = len(links)

#PageRank array
P = np.zeros((len_links, len_links))

#filling array by alghoritm
for i in range(len_links): 
    s = len(links[i])
    if s > 0:
        for j in range(len_links):
            P[j, i] = 1 / s if j in links[i] else 0
    else:
        for j in range(len_links):
            P[j, i] = 1 / len_links
        #print(sites[i])

np.savetxt('p.txt', P, fmt='%10.5f')

k = 100 #Iterations
x = np.array([1 / len_links for i in range(len_links)]) 

#filling x by alghoritm 
while k >= 0:  
    x = P @ x
    k -= 1

sort = x.argsort()  
print(list(reversed([sites[i] for i in sort])))
print(list(reversed([x[i] for i in sort])))

print("Work time of program:")   
print(time.perf_counter() - t)