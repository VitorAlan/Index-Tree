#Feature selector according to filters proeficiency
def Feature_Selector(filters, filters_proeficiency, limiar):
    # variables that will be used as ouput of the function
    #returns a vector of best features based on filters proeficinecy and its proeficiency
    feature_list = []
    filters_list = []
    
    #selecting the best features
    for a in range(limiar):
        feature_list.append(filters_proeficiency.index(max(filters_proeficiency)))
        filters_proeficiency[feature_list[-1]] = -9999
        filters_list.append(filters[feature_list[-1]])
    
    #output of the function
    return filters_list, feature_list

    