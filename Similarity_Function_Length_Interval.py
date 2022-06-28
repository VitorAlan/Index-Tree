import math

def Similarity_Function_Length_Interval(Similarity_Function, A, Threshold):
    similarity_functions_list = ["HammingDistanceFunction","LevenshteinDistanceFunction", "NormalizedLevenshteinDistanceFunction",
                                 "JaccardFunction", "CosineFunction", "SorensenFunction", "DiceFunction", "JaroFunction", "BraunBlanquetFunction", "OverlapFunction"]
    index = similarity_functions_list.index(Similarity_Function)
    lower_interval_list = [len(A)-Threshold, len(A)-Threshold, Threshold*len(A), Threshold*len(A), (Threshold**2)*len(A), (Threshold/(2-Threshold))*len(A), (Threshold/(2-Threshold))*len(A), abs(3*Threshold-2)*len(A), Threshold*len(A), len(A)-Threshold]
    upper_interval_list = [len(A)+Threshold, len(A)+Threshold, len(A)/Threshold, len(A)/Threshold, len(A)/(Threshold**2), ((2-Threshold)/Threshold)*len(A), ((2-Threshold)/Threshold)*len(A), len(A)/abs(3*Threshold-2), len(A)/Threshold, len(A)+Threshold]
    interval = [a for a in range(math.floor(lower_interval_list[index]),math.ceil(upper_interval_list[index])+1)]
    return interval
