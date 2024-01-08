# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:58:41 2023

@author: potyaga2
"""
import numpy as np
from PIL import Image
#from feature_extractor import FeatureExtractor
from pathlib import Path

main_path = "C:\\Users\\potyaga2\\Documents\\Custom\\python_scripts\\project\\"

filter_feat_arr = [] 
archive_feat_arr = []
features_list = []
res_lst = []
path = main_path + "found_files.txt"
with open(path) as features_file:
    lines = features_file.readlines()
    for line in lines:
         features_list.append(main_path+"templates\\static\\flickr30k_images\\features\\" + line[:-5] + ".npy")
        
    #read file names from file - done
    #add to list - done
    #extract features from file
    #compare distance between filter and files in list
    #print(features_list)
    i = 0
    title = "3971903221.jpg"
    filter_path = (main_path+"templates\\static\\flickr30k_images\\features\\" + title[:-4] + ".npy")
    for i in features_list:
        try:
             archive_feat_arr = np.load(i) 
        except FileNotFoundError:
            continue
        filter_feat_arr = np.load(filter_path)
        dists = np.linalg.norm( archive_feat_arr-filter_feat_arr, axis=0)  # L2 distances to features
        ids = np.argsort(dists)[:10]  # Top 30 results
         #scores = [(dists[id], img_paths[id]) for id in ids]
        if dists < 1.41:
            spl = i.split('\\')
            fin = spl[11][:-4] + ".jpg"
            res_lst.append(fin)
print(res_lst)
         
        #i +=1