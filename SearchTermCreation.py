import time
import sys
import resource
import numpy
import subprocess
from libs.search import Dawg
from libs.phonetic_similarity.similarity import similarity

class Permutation:
    def __init__(self, word, weight):
        self.word = word
        self.weight = weight
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.word == other.word
        else:
            return False
    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.word <= other.word
        else:
            return False
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.word < other.word
        else:
            return False
    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.word > other.word
        else:
            return False
    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.word >= other.word
        else:
            return False
def IPAdict(word, CMU):
    d = {}
    if CMU:
        with open("/home/william/LingProj/SearchTest/cmudict_ipa.txt") as f:
            for line in f:
                if word in line:
                    (key, val) = line.split()
                    d[key] = val
        IPA = d.get(word)
        print(IPA.split("_"))
    else:
        ENG_STR_TO_ENG_IPA_CMD ='espeak -q --ipa=3 -v en "' + word + '"| sed -r "s/^\\s?(.+)\\s?$/\\1/g"| sed -E "s/[ˈˌˑ]//g"'
        IPA = subprocess.getoutput(ENG_STR_TO_ENG_IPA_CMD).strip()
        print(IPA.split("_"))
    return IPA.split("_")

def permute(word, weight):
    "All edits that are one edit away from `word`."
    letters    = {"ɐ": 18, "ɑː": 38, "f": 2, "w": 19, "ɔː": 17, "t": 10, "l": 31, "ɔɪ": 46, "aɪ": 12, "v": 22, "tʃ": 33, "j": 43, "m": 34, "əʊ": 32, "eə": 21, "ʌ": 25, "n": 8, "dʒ": 42, "ɡ": 41, "h": 28, "θ": 44, "ʊə": 45, "əl": 23, "r": 49, "aʊ": 40, "ɪ": 1, "z": 24, "a": 4, "ʊ": 15, "ʒ": 35, "ð": 26, "ʃ": 14, "ɒ": 27, "uː": 37, "ɹ": 5, "iː": 13, "ə": 11, "ɛ": 7, "eɪ": 20, "aɪə": 47, "d": 6, "ɜː": 29, "s": 9, "p": 30, "ŋ": 36, "b": 16, "aʊə": 48, "k": 3, "iə": 39}
    splits     = [(word[:i], word[i:])     for i in range(len(word) + 1)]
    replaces   = [replace(c, L, R, weight) for L, R in splits if R for c in letters]
    deletes    = [delete(L, R, weight)     for L, R in splits if R]
    inserts    = [insert(c, L, R, weight)   for L, R in splits for c in letters]
    p = replaces + deletes + inserts
    return p 
def delete(L, R, weight):
    weight += 1
    p = Permutation(L + R[1:], weight)
    return(p)
def insert(c, L, R, weight):
    weight += 1
    p = Permutation(L + [c] + R, weight)
    return(p)
def replace(c, L, R, weight):
    weight += 1 - similarity(c, R[0])**10
    p = Permutation(L + [c] + R[1:], weight)
    return(p)
def multi_permute(word):
    permutations = [Permutation(word, 0)]
    i=0
    cap = 0
    while i < len(permutations) and cap <= 10:
        permutation = permutations[i]
        if (permutation.weight < (1.5/(1 + (200*numpy.exp(-1*len(word)))))):
            ## len(word)/(2-1.5)
            ## (2/(1 + (200*numpy.exp(-1*len(word))))) Sigmoid if fancier is needed
            permutations.extend(permute(permutation.word, permutation.weight))
        else:
            cap += 1
        i += 1
    return permutations

def search_creation(TARGET):
    f = open('TestDawg.txt', 'w')
    dawg = Dawg.Dawg()
    WordCount = 0
    start = time.time()
    for permutation in multi_permute(TARGET):
        WordCount += 1
        f.write(''.join(permutation.word) + "\n" )
        dawg.insert(permutation.word)
    dawg.finish()
    f.close()
    #print("\nDawg creation took {:g} s".format(time.time()-start))
    
    EdgeCount = dawg.edgeCount()
    #print("Read {:d} words into {:d} nodes and {:d} edges".format(WordCount,
    #                                                              dawg.nodeCount(), EdgeCount))
    #print("This could be stored in as little as {:d} bytes".format(EdgeCount * 4))
    return dawg
if __name__ == "__main__":
    TARGET = IPAdict(sys.argv[1], False)
    f = open("keywords/" + sys.argv[1] + ".txt", 'w')
    for permutation in multi_permute(TARGET):
        f.write(''.join(permutation.word) + "\n" )
    f.close()
