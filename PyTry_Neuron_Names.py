#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt



# In[2]:


import Odorant_Stim_fourodors


# In[30]:


import csv
import collections

def read_connections(filename):
    #r = list(csv.reader(open('updated_erecta_all_circuitry_absolute.csv'))) #Need to get updated connectivity from Ruairi with all neurons
    #r = list(csv.reader(open('updated_melanogaster_all_circuitry_absolute.csv'))) #does this need to be changed to 'filename'?
    r = list(csv.reader(open(filename)))
        
    header = r[0]
    data = r[1:]

    conns = {}
    for row in data:
        for i, item in enumerate(row):
            if i > 0:
                pre = row[0]
                post = header[i]
                c = int(item)
                if c > 0:
                    if pre not in conns:
                        conns[pre] = {}
                    conns[pre][post] = c
                    
    ORNs_left = [name for name in header if 'ORN' in name and 'left' in name]
    ORNs_right = [name for name in header if 'ORN' in name and 'right' in name]
    uPNs_left = [name for name in header if ' uPN' in name and 'left' in name]
    uPNs_right = [name for name in header if ' uPN' in name and 'right' in name]
    mPNs_left = [name for name in header if 'mPN' in name and 'left' in name]
    mPNs_right = [name for name in header if 'mPN' in name and 'right' in name]
    Pickys_left = [name for name in header if 'icky' in name and 'left' in name]
    Pickys_right = [name for name in header if 'icky' in name and 'right' in name]

    #assert (len(ORNs_left)+len(ORNs_right)+len(uPNs_left)+len(uPNs_right)+
    #        len(mPNs_left)+len(mPNs_right)+len(Pickys_left)+len(Pickys_right) == (21*4+15*2+5*2))
                         
    Names = collections.namedtuple('Names', ['ORNs_left', 'uPNs_left', 'mPNs_left', 'Pickys_left'])
    return conns, Names(ORNs_left, uPNs_left, mPNs_left, Pickys_left)

def make_weights(conns, pre, post):
    w = np.zeros((len(post), len(pre))) #note: pre/post switched in output array for print(make_weights())
    for i, pre_n in enumerate(pre):
        for j, post_n in enumerate(post):
            if post_n in conns[pre_n]:
                w[j,i] = conns[pre_n][post_n] 
    return w

