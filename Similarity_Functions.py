import textdistance
from abydos import distance

#All functions presented execute the similarity between all attributes of the pair of multi-attributes entities

#A and B are entities and t is an integer threshold
def HammingDistanceFunction(A,B,t):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.hamming(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#A and B are entities and t is an integer threshold
def LevenshteinDistanceFunction(A,B,t, filters_vector,features):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.levenshtein(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#Normalized version of Levenshtein Distance
#A and B are entities and t is a normalized threshold 
def NormalizedLevenshteinDistanceFunction(A,B,t):
    norm = 0
    for i in range(len(A)):
        sim = textdistance.levenshtein(A[i],B[i])
        norm += (len(max(A[i],B[i],key=len))-sim)/len(max(A[i],B[i],key=len))
    norm = norm/len(A)
    return (A, B, norm)

#A and B are entities and t is a normalized threshold 
def JaccardFunction(A,B,t):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.jaccard(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#A and B are entities and t is a normalized threshold  
def CosineFunction(A,B,t):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.cosine(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#Sorensen and dice similarity function
#A and B are entities and t is a normalized threshold 
def SorensenCoefficient(A,B,t, filters_vector,features):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.sorensen(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#A and B are entities and t is a normalized threshold 
def JaroFunction(A,B,t):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.jaro(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#A and B are entities and t is a normalized threshold
def BraunBlanquetFunction(A,B,t):
    sim = 0
    BraunBlanquet = distance.BraunBlanquet()
    for i in range(len(A)):
        sim += BraunBlanquet.sim(A[i],B[i])
    sim = sim/len(A)
    return (A, B, sim)

#A and B are entities and t is a normalized threshold
def OverlapFunction(A,B,t, filters_vector,features):
    sim = 0
    for i in range(len(A)):
        sim += textdistance.overlap(A,B)
    sim = sim/len(A)
    return (A, B, sim)