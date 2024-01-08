import numpy as np
from PIL import Image
#from feature_extractor import FeatureExtractor
from pathlib import Path
import os


main_path = "C:\\Users\\potyaga2\\Documents\\Custom\\python_scripts\\project\\"
features_path = "C:\\Users\\potyaga2\\Documents\\train_val_videos\\features\\"
flag = 1

filter_feat_arr = [] 
archive_feat_arr = []
features_list = []
res_lst = []

if flag == 1:
       path = main_path + "found_files_video.txt"
else:
       path = main_path + "found__filtered_video_files.txt"

with open(path) as features_file:
       lines = features_file.readlines()
with open(path) as features_file:
    lines = features_file.readlines()
    for line in lines:
         features_list.append(features_path + line.strip('\n') )
        
    #read file names from file - done
    #add to list - done
    #extract features from file
    #compare distance between filter and files in list
    #print(features_list)
    i = 0
    title = "3171506111.jpg"
    filter_path = (main_path+"templates\\static\\flickr30k_images\\features\\" + title[:-4] + ".npy")
    for fold_path in features_list:
       # print(fold_path)
        #print(os.listdir(fold_path))
        for file in os.listdir(fold_path):
            if file.endswith(".npy"):
                itera = os.path.join(fold_path, file)
                
           
            try:
              archive_feat_arr = np.load(itera) 
            except FileNotFoundError:
             continue
            filter_feat_arr = np.load(filter_path)
            dists = np.linalg.norm( archive_feat_arr-filter_feat_arr, axis=0)  # L2 distances to features
            #ids = np.argsort(dists)[:10]  # Top 30 results
#           #scores = [(dists[id], img_paths[id]) for id in ids]
            if dists < 1.38:
                 spl = itera.split('\\')
                 fin = spl[6]
                 res_lst.append(fin)
print(*set(res_lst))
     
#         #i +=1