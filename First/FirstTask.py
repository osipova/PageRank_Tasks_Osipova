# -*- coding: utf8 -*-

import numpy as np
from bs4 import BeautifulSoup
import urllib.request as urllib
import re

#function to get links
def check(item):  
    try:
        html_page = urllib.urlopen(item)
        soup = BeautifulSoup(html_page, "html.parser")
        result = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http(s)?://")}):
            s = link.get('href')
            #check that link is not picture 
            if not s.endswith('.jpg') and not s.endswith('.png') and not s.endswith('.gif') and not s.endswith(
                    '.jpeg') and not s.endswith('.pdf'):  
                result.append(s)
        return result
    except:
        return -1

#root site
sites = ["http://kpfu.ru/"] 
#array links
a = np.zeros((1, 1), dtype=np.uint8)

i = 0  #number of site in queue
len_sites = len(sites) #Number of sites
full = False #queue

while i < len_sites:
    #get all links in page  
    all_new = check(sites[i])  
    #amount of links > 0
    if type(all_new) is list and len(all_new): 
        set_new = set(all_new)
        old = set_new & set(sites) #elements which are in queue

        if full or len_sites > 100: #if amount of links > 100 then do not add new links
            full = True

            if not len(old): #if not in query 
                sites.remove(sites[i]) #remove link from array 
                a = np.delete(a, i, 1)
            else:
                for j in old:
                    a[i, sites.index(j)] = 1  
                a = np.append(a, np.zeros([1, len(a[0])], dtype=np.uint8), 0)  #add string to matrix 
                i += 1
        else:
            new = set_new - set(sites)  #elemants which are not in query

            if not len(new) and not len(old):  
                sites.remove(sites[i]) 
                a = np.delete(a, i, 1)
            #add new links
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

    len_sites = len(sites)  #update amount of elements
    print('{}/{}'.format(i, len_sites))  #cheking progress
print (sites)
a = np.delete(a, (-1), axis=0)  
np.fill_diagonal(a, 0)
np.savetxt('matrix.txt', a, fmt='%d')

