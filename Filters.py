from datasketch import MinHash,MinHashLSH
import math
import textdistance

#return length of string A
def LengthFilter(A):
    return len(A)

#prefix filter = inverted list of the first p tokens of record A, we fixed p as 3
def PrefixFilter(A):
    p = 3
    tokens = A[0:p]
    tokens = sorted(tokens)
    tokens.reverse()
    return tokens

#suffix filter = inverted list of the first p tokens of record A, we fixed p as 3
def SuffixFilter(A):
    p = 3
    tokens = A[-p:]
    tokens = sorted(tokens)
    tokens.reverse()
    return tokens

#MinHash = return the hashs of the record A
#where the number of permutation is p
#and s (the seed) controls the set of random permutations functions gerenated for MinHash
def MinHashFilter(A):
    p = 3
    mh = MinHash(num_perm=p,seed=p)
    mh.update(A.encode('utf8'))
    return list(mh.digest())

#PositionalFilter = return a number based on the following formula:
#prefix ocurrence+min(notused(|A|,|B|))>threshold
#from that we splited the usage of the filter to work the prefix validation and only in the join operation the calculation
def PositionalFilter(A):
    p = 3
    tokens = list(A[:p])
    ordered = sorted(tokens)
    ordered.reverse()
    length = len(A)-p
    return ordered,tokens,length