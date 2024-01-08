import pandas as pd
import json

import pandas as pd
import csv
from gensim.models.doc2vec import Doc2Vec
import gensim.downloader as api
from gensim.parsing.preprocessing import preprocess_string, remove_stopwords



with open('test_videodatainfo.json') as json_data:
    data = json.load(json_data)
    df = pd.DataFrame(data['sentences'])
    #print(df.head())
    print(df['caption'])
    

with open('train_val_videodatainfo.json') as json_data:
    data = json.load(json_data)
    df = pd.DataFrame(data['sentences'])
    #print(df.head())
    
    
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
        
        