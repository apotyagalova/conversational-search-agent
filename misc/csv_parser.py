import pandas as pd
import gensim.downloader as api
from gensim.parsing.preprocessing import remove_stopwords
import csv


main_path = "C:\\Users\\potyaga2\\Documents\\Custom\\python_scripts\\project\\"

word_vectors = api.load("glove-wiki-gigaword-100")
print("loaded")

# def similarity_movies(query, df):
#     i = 1
#     res = []
#     while i < 40460:
#         tmp = remove_stopwords(df['Capture'][i])
#         splt = tmp.split(' ')
#         query_rm = remove_stopwords(query)
#         query_spl = query_rm.split(' ')
#         try:
#             sims = word_vectors.n_similarity(splt, query_spl)
#             if sims > 0.90:
#                 res.append(df['Title'][i])
                 
#         except KeyError:
#             i +=1
#         i +=1
#     return res

def test_f(x):
    print(x)
    return remove_stopwords(x)




df_input_nan = pd.read_csv(main_path + 'image_dataset.csv')
df_input = df_input_nan.dropna()
#print(df_input.head())

#print(df_input.loc[0,'Capture'])
#print(df_input.index.tolist())
#labels = [str(remove_stopwords(df_input['Capture'][i])) for i in df_input.index.tolist()]
#labels = [remove_stopwords(df_input['Capture'][i]) for i in df_input.index.tolist()]
#df_input.insert(2, "Labels", labels, allow_duplicates=True)
#df_input.to_csv("demo.csv", index_label=None)


query_1 = 'dog is playing'
title_1 = '1000268201_693b08cb0e'



lst = df_input.loc[df_input['Title']==title_1]['Labels'].to_list() 
i = 0
spl = []
# for i in range(len(lst)):
#     spl += lst[i].split(' ')
# res = [*set(spl)] #all labels for the predefined image
# print("labels:", res)
# i = 0 
# tmp_lst = []
# res_lst = []
# for i in range(len(df_input.index)):
#         try:
#                spl = df_input['Labels'][i].split(' ')
#                sims = word_vectors.n_similarity(res, spl)
#                if sims > 0.91:
#                     tmp_lst.append(df_input['Title'][i])
#                res_lst = [*set(tmp_lst)] 
#         except KeyError:
#                i +=1
    
# print(res_lst)
csv_file = open(main_path + 'results_30k.csv')
reader = csv.DictReader(csv_file)

fieldnames = reader.fieldnames + ['Labels']
print(reader.fieldnames)
with open('results_30k_upd.csv', 'w') as f:
    writer = csv.writer(f) #this is the writer object
    #print(writer.fieldnames)
    for row in reader:
            tmp = remove_stopwords(row['Capture'])
            splt = tmp.split(' ')
            i = 0
            #print(splt)
            writer.writerow(splt + ";")
            # for i in range(1,len(splt)-1):
            #       writer.writerow('Labels') # this will list out the names of the columns which are always the first entrries
            #       writer.writerow(splt[i] + ";")   #this is the data
            #       row['Labels'].append(splt[i])
            #       #row['Labels'].append(";")
                 
            #      # print(splt[i])
            #       i += 1
       
        
   
#print(similarity_movies(query_1, df_input))
