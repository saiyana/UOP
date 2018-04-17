from __future__ import division
from sklearn import neighbors
from sklearn import svm
from sklearn import cross_validation
from sklearn import preprocessing as pr
from sklearn import metrics
import numpy as np
import nltk
import operator

def getStopWordList(stopWordListFileName):
    stopWords = []
    stopWords.append('at_user')
    stopWords.append('url')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

def loadSlangs(filename):
    slangs={}
    fi=open(filename,'r')
    line=fi.readline()
    while line:
        l=line.split(r',%,')
        if len(l) == 2:
            slangs[l[0]]=l[1][:-2]
        line=fi.readline()
    fi.close()
    return slangs

def loadAfinn(filename):
    f=open(filename,'r')
    afinn={}
    line=f.readline()
    nbr=0
    while line:
        nbr+=1
        l=line[:-1].split('\t')
        afinn[l[0]]=float(l[1])/4 # Normalizing
        line=f.readline()
    return afinn

def createEmoticonDictionary(filename):
    emo_scores = {'Positive': 0.5, 'Extremely-Positive': 1.0, 'Negative':-0.5,'Extremely-Negative': -1.0,'Neutral': 0.0}
    emo_score_list={}
    fi = open(filename,"r")
    l=fi.readline()

    while l:
        l=l.replace("\xc2\xa0"," ")
        li=l.split(" ")
        l2=li[:-1]
        l2.append(li[len(li)-1].split("\t")[0])
        sentiment=li[len(li)-1].split("\t")[1][:-1]
        score=emo_scores[sentiment]
        l2.append(score)
        for i in range(0,len(l2)-1):
            emo_score_list[l2[i]]=l2[len(l2)-1]
        l=fi.readline()
    return emo_score_list

def getWordFeatures(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    result=[]
    for k in wordlist.keys():
        result.append([k,wordlist[k]])
    return result

def sortList(x):
    return list(reversed(sorted(x, key=operator.itemgetter(1))))

def getTweetWords(tweet):
    all_words = []
    sTweet=tweet.split()
    return sTweet

def ngramText(filename):
    textWords=[]
    f=open(filename,"r")
    line=f.readline()
    while line:
        textWords.extend(getTweetWords(line))
        line=f.readline()
    f.close()
    return textWords

def mostFreqList(filename,k):
    d=getWordFeatures(ngramText(filename))
    l=sortList(d)
    m=[w[0] for w in l[0:k]]
    return m

nNeighbors=10
kernalFunction='linear'
cParameter=0.2
unigramSize=3000

stopWords = getStopWordList('./Resources/stopWords.txt')
slangs = loadSlangs('./Resources/internetSlangs.txt')
afinn = loadAfinn('./Resources/afinn.txt')
emoticonDict = createEmoticonDictionary("./Resources/emoticon.txt")
positive = mostFreqList('./TrainingDataset/positive1.csv', unigramSize)
negative = mostFreqList('./TrainingDataset/negative1.csv', unigramSize)
neutral = mostFreqList('./TrainingDataset/neutral1.csv', unigramSize)

for w in positive:
    if w in negative + neutral:
        positive.remove(w)

for w in negative:
    if w in positive + neutral:
        negative.remove(w)

for w in neutral:
    if w in negative + positive:
        neutral.remove(w)

m = min([len(positive), len(negative), len(neutral)])
positive = positive[0:m - 1]
negative = negative[0:m - 1]
neutral = neutral[0:m - 1]


def loadMatrix(posfilename, neufilename, negfilename, poslabel, neulabel, neglabel):
    vectors = []
    labels = []
    f = open(posfilename, 'r')
    kpos = 0
    kneg = 0
    kneu = 0
    line = f.readline()
    while line:
        try:
            kpos += 1
            z = mapTweet(line, afinn, emoticonDict, positive, negative, neutral, slangs)
            vectors.append(z)
            labels.append(float(poslabel))
        except:
            None
        line = f.readline()
    f.close()

    f = open(neufilename, 'r')
    line = f.readline()
    while line:
        try:
            kneu = kneu + 1
            z = mapTweet(line, afinn, emoticonDict, positive, negative, neutral, slangs)
            vectors.append(z)
            labels.append(float(neulabel))
        except:
            None
        line = f.readline()
    f.close()

    f = open(negfilename, 'r')
    line = f.readline()
    while line:
        try:
            kneg = kneg + 1
            z = mapTweet(line, afinn, emoticonDict, positive, negative, neutral, slangs)
            vectors.append(z)
            labels.append(float(neglabel))
        except:
            None
        line = f.readline()
    f.close()
    return vectors, labels

def start():
    X, Y = loadMatrix('./TrainingDataset/positive1.csv', './TrainingDataset/neutral1.csv', './TrainingDataset/negative1.csv', '4', '2','0')
    print X
    print Y
if __name__ == "__main__":
    start()