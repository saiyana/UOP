import editdistance
import io
import itertools
import networkx as nx
import nltk
import os

document=""
summaryResult=[]
phrasesResult=[]

def getlists(obj):
    topics=[]
    summary=[]
    for i in range(0,len(obj)):
        topics.append(obj[i]['name'])
        summary.append(obj[i]['phrase'])
    return [topics,summary]

def getSummary(obj):
    setupEnvironment()
    [topics,summary]=getlists(obj)
    for i in summary:
        document=i;
        summary = extractSentences(document)
        phrases = extractKeyPhrases(document)
        summaryResult.append(summary)
        phrasesResult.append(phrases)

    res = []
    for i in range(0, len(summaryResult)):
        res.append({'name': topics[i], 'summary': summaryResult[i]})
    return res

def setupEnvironment():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

def filterForTags(tagged,tags=['NN','JJ','NNP']):
    return [item for item in tagged if item[1] in tags]

def normalize(tagged):
    return [(item[0].replace('.',''), item[1]) for item in tagged]

def uniqueEverseen(iterable,key=None):
    seen=set()
    seenAdd=seen.add
    if key is None:
        for element in [x for x in iterable if x not in seen]:
            seenAdd(element)
            yield element
    else:
        for element in iterable:
            k=key(element)
            if k not in seen:
                seenAdd(k)
                yield element

def buildGraph(nodes):
    gr=nx.Graph()
    gr.add_nodes_from(nodes)
    nodePairs=list(itertools.combinations(nodes,2))

    for pair in nodePairs:
        firstString=pair[0]
        secondString=pair[1]
        levDistance=editdistance.eval(firstString,secondString)
        gr.add_edge(firstString,secondString,weight=levDistance)

    return gr

def extractKeyPhrases(text):
    wordTokens=nltk.word_tokenize(text)
    tagged=nltk.pos_tag(wordTokens)
    textList=[x[0] for x in tagged]
    tagged=filterForTags(tagged)
    tagged=normalize(tagged)

    uniqueWordSet=uniqueEverseen([x[0] for x in tagged])
    wordSetList=list(uniqueWordSet)

    graph=buildGraph(wordSetList)
    calculatedPageRank=nx.pagerank(graph,weight='weight')
    keyPhrases=sorted(calculatedPageRank,key=calculatedPageRank.get,reverse=True)

    oneThird=len(wordSetList)//3
    keyPhrases=keyPhrases[0:oneThird+1]

    modifiedKeyPhrases=set([])
    dealtWith=set([])
    i=0
    j=1
    while j<len(textList):
        first=textList[i]
        second=textList[j]
        if first in keyPhrases and second in keyPhrases:
            keyPhrases=first+' '+second
            modifiedKeyPhrases.add(keyPhrases)
            dealtWith.add(first)
            dealtWith.add(second)
        else:
            if first in keyPhrases and first not in dealtWith:
                modifiedKeyPhrases.add(first)
            if j==len(textList)-1 and second in keyPhrases and second not in dealtWith:
                modifiedKeyPhrases.add(second)

        i=i+1
        j=j+1
    return modifiedKeyPhrases

def extractSentences(text,summaryLength=100,cleanSentences=True,language='english'):
    sentDetector=nltk.data.load('tokenizers/punkt/'+language+'.pickle')
    sentenceTokens=sentDetector.tokenize(text.strip())
    graph=buildGraph(sentenceTokens)
    calculatedPageRank=nx.pagerank(graph,weight='weight')
    sentences=sorted(calculatedPageRank,key=calculatedPageRank.get,reverse=True)
    summary=' '.join(sentences)
    summaryWords=summary.split()
    summaryWords=summaryWords[0:summaryLength]
    dotIndices=[idx for idx, word in enumerate(summaryWords) if word.find('.')!=-1]
    if cleanSentences and dotIndices:
        lastDot=max(dotIndices)+1
        summary=' '.join(summaryWords[0:lastDot])
    else:
        summary=' '.join(summaryWords)

    return summary

