# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import numpy as np
import random
import json
import os

import numpy as np
from PIL import Image
#from feature_extractor import FeatureExtractor
from pathlib import Path


import pandas as pd
import csv
from gensim.models.doc2vec import Doc2Vec
import gensim.downloader as api
from gensim.models import Word2Vec, KeyedVectors
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords


main_path = "C:\\Users\\potyaga2\\Documents\\scripts\\project\\"
word_vectors = KeyedVectors.load("C:\\Users\\potyaga2\\Documents\\scripts\\project\\actions\\glove-wiki-gigaword-100.model")
video_feature_path = "C:\\Users\\potyaga2\\Documents\\train_val_videos\\features\\"




sims_upd = []
images_path = "http://localhost:8000/"
def similarity_dataset(query, df):
        i = 1
        res = []
        #print('started')
        while i < df.size: #change
            try:
                tmp = remove_stopwords(str(df['Capture'][i]))
                splt = tmp.split(' ')
                query_rm = remove_stopwords(query)
                query_spl = query_rm.split(' ')
            
                sims = word_vectors.n_similarity(splt, query_spl)
                if sims > 0.9:
                    res.append(df['Title'][i])
                     
            except KeyError:
                i +=1
            i +=1
        return res

def similarity_labels(query, df):
        i = 1
        res = []
        #print('started')
        while i < df.size: #change
            try:
                tmp = df['Labels'][i]
                splt = tmp.split(' ')
                query_rm = remove_stopwords(str(query))
                query_spl = query_rm.split(' ')
            
                sims = word_vectors.n_similarity(splt, query_spl)
                if sims > 0.92:
                    res.append(df['Title'][i])
                     
            except KeyError:
                i +=1
            i +=1
        return res
    
    
def similarity_video_dataset(query, df):
        i = 1
        res = []
        #print('started')
        while i < df.size: #change
            try:
                tmp = remove_stopwords(str(df['caption'][i]))
                splt = tmp.split(' ')
                query_rm = remove_stopwords(query)
                query_spl = query_rm.split(' ')
            
                sims = word_vectors.n_similarity(splt, query_spl)
                if sims > 0.9:
                    res.append(df['video_id'][i])
                     
            except KeyError:
                i +=1
            i +=1
        return res

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello! I am your image search assitant. Please, enter your search query.")

        return []





class ActionMovieSearch(Action):

    def name(self) -> Text:
        return "action_movie_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userMessage = tracker.get_slot("query")
        #current_slots=tracker.current_slot_values())		
        # use model to find the movie
        # search_query = preprocess_string(userMessage)
        
        # Load dataset to get movie titles
        #df = pd.read_csv(main_path + 'video_dataset.csv', usecols=['Title', 'Capture', 'Labels'])
        with open('test_videodatainfo.json') as json_data:
            data = json.load(json_data)
            df = pd.DataFrame(data['sentences'])
            sims = similarity_video_dataset(userMessage, df)
            sims_upd = [*set(sims)]
            
        with open('train_val_videodatainfo.json') as json_data:
            data = json.load(json_data)
            df = pd.DataFrame(data['sentences'])    
            sims_1 = similarity_video_dataset(userMessage, df)
            sims_upd_1 = [*set(sims_1)]
		
        #movies = [df['Title'].iloc[s[0]] for s in sims[:5]]

        botResponse = f"I found the following videos: {sims_upd}, {sims_upd_1}."
        #print('sentence entity taken',sentence)
        dispatcher.utter_message(text=botResponse)
       
        
        with open('found_files_video.txt','w') as tfile:
            tfile.write('\n'.join(sims_upd))
            tfile.write('\n')
            tfile.write('\n'.join(sims_upd_1))
        

        return []
    
class ActionImageSearch(Action):

    def name(self) -> Text:
        return "action_image_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userMessage = tracker.get_slot("query")
        #current_slots=tracker.current_slot_values())		
        # use model to find the movie
        #search_query = preprocess_string(userMessage)
        # Get first 5 matches
        # Load dataset to get movie titles
        df = pd.read_csv(main_path + 'results_30k_upd.csv', usecols=['Title', 'Capture', 'Labels'])
        sims = similarity_dataset(userMessage, df)
        sims_upd = [*set(sims)]
		
        #movies = [df['Title'].iloc[s[0]] for s in sims[:5]]

        botResponse = f"I found the following images: {sims_upd}."
        #print('sentence entity taken',sentence)
        dispatcher.utter_message(text=botResponse)
       
        
        with open('found_files.txt','w') as tfile:
            tfile.write('\n'.join(sims_upd))
        

        return []

def filter_labels(title, df):
   lst = df.loc[df['Title']==str(title)]['Labels'].to_list() #select the labels
   i = 0
   spl = []
   for i in range(len(lst)):
       spl += lst[i].split(' ')
   res = [*set(spl)] #all labels for the predefined image

   i = 0 
   tmp_lst = []
   res_lst = []
   for i in range(len(df.index)):
        try:
               spl = str(df['Labels'][i]).split(' ')
               sims = word_vectors.n_similarity(res, spl)
               if sims > 0.95:
                    tmp_lst.append(df['Title'][i])
               res_lst = [*set(tmp_lst)] 
        except KeyError:
               i +=1
   return res_lst

def filter_content(title, flag):
   filter_feat_arr = [] 
   archive_feat_arr = []
   features_list = []
   res_lst = []
   if flag == 1:
       path = main_path + "found_files.txt"
   else:
       path = main_path + "found__filtered_files.txt"
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
   spl_title = title.split('.')[0]
   
      
   filter_path = (main_path+"templates\\static\\flickr30k_images\\features\\" + spl_title + ".npy")
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
   return res_lst
    
def filter_video_content(title, flag):
  
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
             features_list.append(video_feature_path + line.strip('\n') )
        
    #read file names from file - done
    #add to list - done
    #extract features from file
    #compare distance between filter and files in list
    #print(features_list)
    spl_title = title.split('.')[0]
    
    filter_path = (main_path + "templates\\static\\flickr30k_images\\features\\" + spl_title + ".npy")
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
            if dists < 1.29:
                 #print(dists)
                 spl = itera.split('\\')
                 fin = spl[6]
                 res_lst.append(fin)
    fin_lst = [*set(res_lst)]
    print(fin_lst)
    return fin_lst


class ActionAskClarify1(Action):
    def name(self):
            return "action_ask_clarify_1"
    async def run(self, dispatcher, tracker, domain):
          
            message = "I could suggest you this:" #text with suggestion
            userMessage = tracker.get_slot("query")
            tmp = remove_stopwords(str(userMessage))#parse input, find the separate words
            df = pd.read_csv(main_path + 'results_30k_upd.csv', usecols=['Title', 'Capture', 'Labels'])
            sims = similarity_dataset(tmp, df)  #search among the tags
            #save two first images
            #suggest in buttons
            dispatcher.utter_message(text=message)
            #choice with buttons
            sims_upd = [*set(sims)]
            i = random.randint(0, 4)
            j = random.randint(5, 9)
            filter_path0 = images_path +  sims_upd[i]  
            filter_path1 = images_path +  sims_upd[j] 
            
            with open('filters.txt','w') as tfile:
                tfile.write(str(sims_upd[i]))
                tfile.write('\n')
                tfile.write(str(sims_upd[j]))



            # data = {
            # "payload": 'cardsCarousel',
            #  "data": [
            #       {
            #         "image": filter_path0,
            #          "title": sims_upd[0]
            #        },
            #        {
            #         "image": filter_path1,
            #          "title": sims_upd[1]
            #         },
            #     ]
            # }

            # dispatcher.utter_message(json_message=data)

            
            
            # dispatcher.utter_message(buttons = [
            # {"title": sims_upd[0],
            #   "payload" : "/choice1"
             
            # },
            # {"title": sims_upd[1],
            #   "payload" : "/choice2"
            # }
            # ])
           # dispatcher.utter_message(attachment=data)
            covid_resources = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "image filter",
                    "subtitle": "select it",
                    "image_url": filter_path0,
                    "buttons": [{
                        "title": sims_upd[i],
                        "url": filter_path0,
                        "type": "web_url"
                    },
                        {
                            "title": "select",
                            "type": "postback",
                            "payload": "/choice1"
                        }
                    ]
                },
                    {
                        "title": "image filter",
                        "subtitle": "select it",
                        "image_url": filter_path1,
                        "buttons": [{
                            "title": sims_upd[j],
                            "url": filter_path1,
                            "type": "web_url"
                        },
                            {
                                "title": "select",
                                "type": "postback",
                                "payload": "/choice2"
                            }
                        ]
                    },
                 
                ]
            }
        }

            dispatcher.utter_message(attachment=covid_resources)
           
           
            #np.save("info", sims_upd )
            
           
            return []
    
class ActionFilterByLabels(Action):
    def name(self):
            return "action_filter_by_labels"
    async def run(self, dispatcher, tracker, domain):   
    
       
        choice = []
        log_track = []
        for event in (list((tracker.events))): # latest 5 messages
                #if event.get("event") == "user": # check if the sent by user or bot
                 log_track.append(event.get("text"))
                 if event.get("text") == "/choice1" or event.get("text") == "/choice2":
                     choice = event.get("text")
                 log_track.append('\n')
                 
                 #print(choice)# check here what button string is received
        with open('logfile.txt', 'w') as f:
                print(log_track, file=f)
               
        labels = open("filters.txt", "r+")
        lines = labels.readlines()
        #np.load("info.npy", "r")  
        #print(labels[0])
        #print(labels[1])
        print(lines)
        
        
        flag = 1
        #names_list = open("found_files.txt")
        #df = pd.read_csv(main_path + 'results_30k_upd.csv', usecols=['Title', 'Capture', 'Labels'])
        text_1 = []
        if choice == "/choice1":
            text_1 = filter_content(lines[0], flag) #filter_labels(labels[0], df) #filter arrays
            print("text_1")
        if choice == "/choice2":
            text_1 = filter_content(lines[1], flag) #filter_labels(labels[1], df) #filter arrays
            print("text_2")
            
        print(choice)
        with open('found__filtered_files.txt','w') as tfile:
            tfile.write('\n'.join(text_1))
        
        botResponse = f"I may suggest the filtered image set: {text_1}"
        #print('sentence entity taken',sentence)
        dispatcher.utter_message(text=botResponse)
        
        return []
    
    
class ActionMovieFilter(Action):
    def name(self):
            return "action_movie_filter"
    async def run(self, dispatcher, tracker, domain):   
    
        dispatcher.utter_message(text="Filtered videos:")
        choice = []
        log_track = []
        for event in (list((tracker.events))): # latest 5 messages
                #if event.get("event") == "user": # check if the sent by user or bot
                 log_track.append(event.get("text"))
                 if event.get("text") == "/choice1" or event.get("text") == "/choice2":
                     choice = event.get("text")
                 log_track.append('\n')
                 
                 #print(choice)# check here what button string is received
        with open('logfile.txt', 'w') as f:
                print(log_track, file=f)
               
        labels = open("filters.txt", "r+")
        lines = labels.readlines()
        #np.load("info.npy", "r")  
        #print(labels[0])
        #print(labels[1])
        print(lines)
        
        
        flag = 1
        #names_list = open("found_files.txt")
        #df = pd.read_csv(main_path + 'results_30k_upd.csv', usecols=['Title', 'Capture', 'Labels'])
        text_1 = []
        if choice == "/choice1":
            text_1 = filter_video_content(lines[0], flag) #filter_labels(labels[0], df) #filter arrays
            print("text_1")
        if choice == "/choice2":
            text_1 = filter_video_content(lines[1], flag) #filter_labels(labels[1], df) #filter arrays
            print("text_2")
            
        print(choice)
        with open('found__filtered_video_files.txt','w') as tfile:
            tfile.write('\n'.join(text_1))
        
        botResponse = f"I may suggest the filtered video set: {text_1}"
        #print('sentence entity taken',sentence)
        dispatcher.utter_message(text=botResponse)
        
        return []
    
class ActionFilterByLabels_2(Action):
    def name(self):
            return "action_filter_by_labels_2"
    async def run(self, dispatcher, tracker, domain):   
    
        dispatcher.utter_message(text="Updated filtered images:")
        choice = []
        log_track = []
        for event in (list((tracker.events))): # latest 5 messages
                #if event.get("event") == "user": # check if the sent by user or bot
                 log_track.append(event.get("text"))
                 if event.get("text") == "/choice1" or event.get("text") == "/choice2":
                     choice = event.get("text")
                 log_track.append('\n')
                 
                 #print(choice)# check here what button string is received
        with open('logfile.txt', 'w') as f:
                print(log_track, file=f)
               
        labels = open("filters.txt", "r+")
        lines = labels.readlines()
        #np.load("info.npy", "r")  
        #print(labels[0])
        #print(labels[1])
        print(labels)
        #names_list = open("found_files.txt")
        #df = pd.read_csv(main_path + 'results_30k_upd.csv', usecols=['Title', 'Capture', 'Labels'])
        text_1 = []
        flag = 2
        if choice == "/choice1":
            text_1 = filter_content(lines[0], flag) #filter_labels(labels[0], df) #filter arrays
            print("text_1")
        if choice == "/choice2":
            text_1 = filter_content(lines[1], flag) #filter_labels(labels[1], df) #filter arrays
            print("text_2")
            
        print(choice)
        with open('found__filtered_files.txt','w') as tfile:
            tfile.write('\n'.join(text_1))
        
        botResponse = f"I may suggest the filtered image set: {text_1}"
        #print('sentence entity taken',sentence)
        dispatcher.utter_message(text=botResponse)
        
        return []