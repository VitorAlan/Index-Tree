from Filters import PrefixFilter, SuffixFilter
import math

#identifies the best filters for each attribute of the dataset and their respective proeficiency
#and also the prefix proeficiency
#recieves as input the dataset and the limiar of attributes to be selected
def UnsupervisedFilterSelection(dataset,limiar):
    #these are the output vectors
    configuration = []
    filters_proeficiency = []
    prefix_proeficiency = []
    
    #filter list and index of high prune power filters (it will depend on filters available to usage)
    filters = ["PrefixFilter", "SuffixFilter", "MinHashFilter", "PositionalFilter"]
    filters_index = 1
    
    #assimilating the number of features of the dataset
    attributes = len(dataset[0])
    
    #these auxiliar lists are initially used to keep informations necessary to further calculations
    prefix_aux_list = [[] for a in range(attributes)]
    suffix_aux_list = [[] for a in range(attributes)]
    length_aux_list = [[] for a in range(attributes)]
    unique_aux_list = [[] for a in range(attributes)]
    
    #this value limitates the number of MinHash and Positional Filters that can be employed
    filter_threshold = max(1,math.floor(limiar*0.1))
    
    #auxiliar list to record uniqueness values for each attribute filters
    prefix_list = []
    suffix_list = []
    length_list = []
    unique_list = []
    
    #lists to record normalized filters impact
    normalized_prefix_list = []
    normalized_suffix_list = []
    normalized_length_list = []
    normalized_unique_list = []
    
    #variables to record the mean of influence of each filter over the attributes
    prefix_mean = 0
    suffix_mean = 0
    length_mean = 0
    unique_mean = 0
    
    #vector with relative values of each filter for all attributes
    relative_values = []
    
    #MinHash and Positional Filters which surpassed the threshold
    surpassed_filters = 0
    
    #this will generate metrics that will be used to evaluate the filters in each attribute
    for a in range(len(dataset)):
        for b in range(attributes):
            prefix = PrefixFilter(dataset[a][b])
            suffix = SuffixFilter(dataset[a][b])
            length = len(dataset[a][b])
            #where we are appending unique characters to each vector
            for c in range(len(prefix)):
                if(prefix[c] not in prefix_aux_list[b]):
                    prefix_aux_list[b].append(prefix[c])
                if(suffix[c] not in suffix_aux_list[b]):
                    suffix_aux_list[b].append(prefix[c])
                if(length not in length_aux_list[b]):
                    length_aux_list[b].append(length)
                if(dataset[a][b] not in unique_aux_list[b]):
                    unique_aux_list[b].append(dataset[a][b])
    
    #validating that we do not considered any duplicated value in each subset of the filters sets
    #then we record the length of those set of values to infer their influence over each attribute
    for a in range(attributes):
        prefix_list.append(len(set(prefix_aux_list[a])))
        suffix_list.append(len(set(suffix_aux_list[a])))
        length_list.append(len(set(length_aux_list[a])))
        unique_list.append(len(set(unique_aux_list[a])))

    #normalizing the values
    for a in range(attributes):
        normalized_prefix_list.append((prefix_list[a]-min(prefix_list))/(max(prefix_list)-min(prefix_list)))
        normalized_suffix_list.append((suffix_list[a]-min(suffix_list))/(max(suffix_list)-min(suffix_list)))
        normalized_length_list.append((length_list[a]-min(length_list))/(max(length_list)-min(length_list)))
        normalized_unique_list.append((unique_list[a]-min(unique_list))/(max(unique_list)-min(unique_list)))
    
    #recording the mean of the impact of each filter
    prefix_mean = sum(normalized_prefix_list)/attributes
    suffix_mean = sum(normalized_suffix_list)/attributes
    length_mean = sum(normalized_length_list)/attributes
    unique_mean = sum(normalized_unique_list)/attributes
    
    #obtaining the relative value of each filter compared to their mean (higher relative values infer that the filters are suitable for the attribute)
    for a in range(attributes):
        temporary = []
        temporary.append(normalized_prefix_list[a]/prefix_mean)
        temporary.append(normalized_suffix_list[a]/suffix_mean)
        temporary.append(1-(normalized_unique_list[a]/unique_mean))
        temporary.append(((normalized_length_list[a]/length_mean)+(normalized_prefix_list[a]/prefix_mean))/2)
        relative_values.append(temporary)
        prefix_proeficiency.append(temporary[0])
        
    #filster selection of filters to the configuration
    for a in range(attributes):
        max_value = 0
        index = 0
        for b in range(len(relative_values[a])):
            if(relative_values[a][b]>max_value):
                max_value = relative_values[a][b]
                index = b
        if(index>filters_index):
            surpassed_filters += 1
        configuration.append(filters[index])
        filters_proeficiency.append(max_value)
        
           
        
    #identify if there are any high prune power over the threshold value and change it for the free usage filter with the highest impact
    if(surpassed_filters > filter_threshold):
        #identify the number of filters that will be change
        surpassed_filters -= filter_threshold
        #loop to change the surpassed filter with achieve the lowest impact
        while(0<surpassed_filters):
            min_value = max(filters_proeficiency)
            min_index = 0
            #not every attribute will be in need to change so we employ this variable to lock only surpassed filters be changed
            keep_value = True
            for a in range(len(configuration)):
                #the fixed indexs in this sectuin depends of the filters available at the beginning of this code
                if(configuration[a] == "MinHashFilter"):
                    if(min_value>relative_values[a][2]):
                        min_value = relative_values[a][2]
                        min_index = a
                        keep_value = False
                if(configuration[a] == "PositionalFilter"):
                    if(min_value>relative_values[a][3]):
                        min_value = relative_values[a][3]
                        min_index = a
                        keep_value = False
            if not keep_value:
                configuration[min_index] = filters[relative_values[min_index].index(max(relative_values[min_index][:2]))]
                filters_proeficiency[min_index] = max(relative_values[min_index][:2])
                surpassed_filters -= 1  
    
    #Output of our algorithm
    return configuration, filters_proeficiency, prefix_proeficiency