#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shelve
import xp_loader #imports libtcodpy by itself
import gzip

files = os.listdir('/xp2shelve/')
 
for item in files: 
    if '.xp' in item:
        print item        
        xp_file = gzip.open(item)
        raw_data = xp_file.read()
        xp_file.close()
        
        xp_data = xp_loader.load_xp_string(raw_data)
        
        key = item[:-3]
        print 'Stored in "output" as ',key
    
        file = shelve.open('output', 'c')
        file[key] = xp_data 
        file.close()
       