import random
import time
import math
import pandas as pd
import Unsupervised_Filter_Selection
from Index_Tree import *
from Feature_Selector import *
import datetime

while(True):
    file_name = str(input("Insert the name and format of the dataset. E.g.: steam_app_data.csv\n"))
    try:
        file = pd.read_csv(file_name)
        break
    except:
        print("There is not any file with this name of document type")
    
#Getting all records from the dataset file
D = []
line = "initial"
index = 0
while(line!="" and line!="\n" and line!="" and line!=[]):
    try:
        line = list(file.iloc[index])
    except:
        break
    if(line!="" and line!="\n" and line!="" and line!=[]):
        for i in range(len(line)):
            line[i] = str(line[i])
        D.append(line)
    index += 1

#maximum possible tree level
limit = len(D[0])

#initial condition and level for the tree
key = ""
height = 0

#selecting the Similarity Function
option = 0
while(True):
    print("Choose the Similarity Function by its index, options available: 1) Hamming Distance; 2) Levenshtein Distance; 3) Normalized Levenshtein Distance; 4) Jaccard; 5) Cosine; 6) Sorensen Coefficient; 7) Jaro; 8) BraunBlanquet; 9) Overlap")
    option = str(input())
    try:
        option = int(option)
        if(option<1 or option>9):
            raise Exception("")
        break
    except:
        print("Informed value out of range of options\n")
function_list = ["HammingDistanceFunction","LevenshteinDistanceFunction","NormalizedLevenshteinDistanceFunction","JaccardFunction","CosineFunction","SorensenCoefficient","JaroFunction","BraunBlanquetFunction","OverlapFunction"]
similarity_function = function_list[option-1]

#lower bound threshold
threshold = 0
if(option<3):
    threshold_type = "integer" 
else:
    threshold_type = "normalized"
while(True):
    print("Insert the {} threshold value".format(threshold_type))
    threshold = input()
    if(option<3):
        try:
            threshold = int(threshold)
            if(threshold>=0):
                break
            else:
                raise Exception("")
        except:
            print("Invalid threshold value")
    else:
        try:
            threshold = float(threshold)
            if(threshold>=0 and threshold<=1):
                break
            else:
                raise Exception("")
        except:
            print("Invalid threshold value")

#defining the base dataset
base_dataset = []
size = 0
while(True):
    try:
        size = int(input("Insert the number of records that will be extracted of "+file_name+", maximum of "+str(len(D))+"\n"))
        if(size<=0 or size>len(D)):
            raise Exception("")
        break
    except:
        print("Invalid value informed")
entities_index = random.sample(range(len(D)),size)
for i in range(size):
    base_dataset.append(D[entities_index[i]])

#defining the approach  that will be executed    
limiar = limit
filter_list = []
feature_list = []
while(True):
    execution_option = str(input("Press 1 to Prefix Index Tree, 2 to Reduced Prefix Index Tree, 3 to Adaptive Index Tree, 4 to Reduced Adaptive Index Tree, and  0 to cancel operation\n"))
    if(execution_option == "0"):
        exit(0)
    elif(execution_option == "1"):
        feature_list = [i for i in range(limit)]
        filter_list = ["PrefixFilter" for i in range(limit)]
        break
    elif(execution_option == "2"):
        print("Insert the desired number of features, maximum of {}".format(limit))
        limiar = input()
        try:
            limiar = int(limiar)
            prefix_list = ["PrefixFilter" for i in range(limit)]
            q,w,prefix_proficiency = Unsupervised_Filter_Selection.UnsupervisedFilterSelection(base_dataset, limiar)
            filter_list, feature_list = Feature_Selector(prefix_list, prefix_proficiency, limiar)
            break
        except:
            print("Invalid value")
    elif(execution_option == "3"):
        feature_list = [i for i in range(limit)]
        filter_list, filter_proficiency, q = Unsupervised_Filter_Selection.UnsupervisedFilterSelection(base_dataset, limiar)
        break  
    elif(execution_option == "4"):
        print("Insert the desired number of features, maximum of {}".format(limit))
        limiar = input()
        try:
            limiar = int(limiar)
            filters,filters_proficiency,prefix_proficiency = Unsupervised_Filter_Selection.UnsupervisedFilterSelection(base_dataset, limiar)
            filter_list, feature_list = Feature_Selector(filters, filters_proficiency, limiar)
            break
        except:
            print("Invalid value")
    else:
        print("Invalid option")

#getting the foreign dataset entities
while(True):
    foreign_file_name = str(input("Insert the name and format of the foreign dataset, it must have the same number of attributes as the base dataset. E.g.: steam_app_data.csv\n"))
    try:
        foreign_file = pd.read_csv(foreign_file_name)
        break
    except:
        print("There is not any file with this name of document type")
        
#Getting all records from the foreign dataset file
F = []
line = "initial"
index = 0
while(line!="" and line!="\n" and line!="" and line!=[]):
    try:
        line = list(foreign_file.iloc[index])
    except:
        break
    if(line!="" and line!="\n" and line!="" and line!=[]):
        for i in range(len(line)):
            line[i] = str(line[i])
        F.append(line)
    index += 1    

#checking if F and D have the same number of attributes
if(len(F[0]) != len(D[0])):
    print("The number of attributes of the base and foreign datasets does not match")

else:
    #defining the foreign dataset
    foreign_dataset = []
    size = 0
    while(True):
        try:
            size = int(input("Insert the number of records that will be extracted of "+foreign_file_name+", maximum of "+str(len(F))+"\n"))
            if(size<=0 or size>len(F)):
                raise Exception("")
            break
        except:
            print("Invalid value informed")
    entities_index = random.sample(range(len(F)),size)
    for i in range(size):
        foreign_dataset.append(F[entities_index[i]])
    
    #Execution of Similarity Join
    print("Execution")
    initial_construction_time = time.time()
    Tree = IndexTree(height, key, limiar, filter_list, feature_list)
    Tree.Insert_Dataset(base_dataset)
    final_construction_time = time.time()
    initial_similarity_join_time = time.time()
    pairs = Tree.Similarity_Join(foreign_dataset, threshold, similarity_function)
    final_similarity_join_time = time.time()
    
    #Results, we present the amount of similar pairs not the pairst
    #However, if desired to see the pairs, edit line 189
    print("Construction time: "+str(round((final_construction_time-initial_construction_time),2)))
    print("Similarity Join spent time: "+str(round((final_similarity_join_time-initial_similarity_join_time),2)))
    print("Number of identified similar pairs",str(len(pairs)))    