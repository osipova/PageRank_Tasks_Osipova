# -*- coding: utf8 -*-

import numpy as np
import time
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import multiprocessing as mp

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

i = 0

def execute(item):
    return check(item)  #get list of links

def ordered_set(inlist):
    out_list = []
    for val in inlist:
        if not val in out_list:
            out_list.append(val)
    return out_list


if __name__ == '__main__':
    t = time.perf_counter()
    
    sites = ["http://kpfu.ru/"]  #root
    new_results = sites.copy()
    links = []

    pool = mp.Pool(processes=4)
    results = []

    while len(sites) < 100: #if amount of links > 100 then do not add new links
        new_results = ordered_set(list(pool.map(execute, sites[len(results):])))
        results += new_results
        sites += [j for i in new_results for j in i if j not in sites]
    else:
        new_results = list(pool.map(execute, sites[len(results):]))
        results += new_results

    i = 0  
    len_sites = len(sites) 

    while i < len_sites: 
        if len_sites > 100:
            all_new = results[i]  

            if len(all_new):  
                old = (set(all_new) & set(sites)) - {sites[i]} 
                if not len(old):  
                    sites.remove(sites[i]) 
                    del results[i]
                    for l in links:
                        if i in l:
                            l.remove(i)
                else:
                    old_indices = [sites.index(i) for i in old]
                    links.append(old_indices)
                    i += 1
            else:
                sites.remove(sites[i])  
                del results[i]
                for l in links:
                    if i in l:
                        l.remove(i)

            len_sites = len(sites) 
            print('{}/{}'.format(i, len_sites))  #cheking progress

    for ind, l in enumerate(links): 
        if ind in l:
            l.remove(ind)

    len_links = len(links)
    P = np.zeros((len_links, len_links))  

    for i in range(len_links):  
        s = len(links[i])
        if s > 0:
            for j in range(len_links):
                P[j, i] = 1 / s if j in links[i] else 0
        else:
            for j in range(len_links):
                P[j, i] = 1 / len_links
            print(sites[i])

    k = 100  
    x = np.array([1 / len_links for i in range(len_links)])  

    while k >= 0:  
        x = P @ x
        k -= 1

    sort = x.argsort()
    print(list(reversed([sites[i] for i in sort])))
    print(list(reversed([x[i] for i in sort])))
    
    print("Work time of program:")   
    print(time.perf_counter() - t)