#take the every 30 frame in video - done
#extract the features - 
#save to the spec_video folder


import cv2
from feature_extractor import FeatureExtractor
from pathlib import Path, PureWindowsPath
import pathlib
import numpy as np
import os
import glob
from PIL import Image

video_path = "C:\\Users\\potyaga2\\Documents\\train_val_videos\\TrainValVideo\\"
fe = FeatureExtractor()
feature_path = "C:\\Users\\potyaga2\\Documents\\train_val_videos\\features\\"

for in_movie in sorted(Path(video_path).glob("*.mp4")):
    upd_path = feature_path
    input_movie = cv2.VideoCapture(str(in_movie))
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    video = PureWindowsPath(in_movie).name[:-4]

    # open url with opencv
    ret,frame = input_movie.read()
    count = 0
    frame_number = 0
    upd_path = pathlib.PurePath(feature_path, video)
    

    #print(upd_path)
    #os.mkdir(upd_path)
      
    while ret:      #take each 20 frame from video
          #print("frame number: ", frame_number)
          i = 0
        
          while i < 50:
                  ret, frame = input_movie.read()
                  i += 1
          if frame_number < length/50 and frame is not None:
              cv2.imwrite(str(upd_path) + "\\frame_{}.png".format(frame_number), frame )        
              frame_number += 1
          else:  
              break
              input_movie.release()
            
            
     
    for img_path in sorted(Path(upd_path).glob("*.png")): #extract features from pre-selected frames
        print("processing :" + str(img_path))  # e.g., ./static/img/xxx.jpg
        feature = fe.extract(img=Image.open(img_path))
        features_saved = Path(upd_path) / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
        print("processed:" + str(features_saved))
        np.save(features_saved, feature)           
            
