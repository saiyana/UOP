import editdistance
import io
import itertools
import networkx as nx
import nltk
import os

#document="Feedback about a product or a service or both is a very important aspect of customer satisfaction for any firm. The idea of this project is to build an application that crawls the entire web to find and analyze references to Chase and categorize the feedback given. With so much feedback it will be good to have an algorithm which takes the data of customer feedback(either by crawling web or manual input of tweets/posts on social media) and identifies the most important topics customers of chase spoke about, summarize it. As an additional feature, it can also perform sentiment analysis to give if the feedback is positive or negative on a particular product of chase. Web application that is internal to Chase to crawl the internet and find references and categorize feedback. Identify the customer friends/family through Social media (Facebook, twitter etc) and identify non-chase customers to offer various products.Web crawlers, optimization of the time and resource of the crawler. Understanding of the data analytics, pattern matching, report generations. Future enhancements, suggestion guessing and possible scenario generations. By capturing, analyzing the customers feedback, this application helps us to further refine and better the existing customer servicing."
document=""
summaryNMF=[]
summaryLDA=[]
phrasesNMF=[]
phrasesLDA=[]

def start(selectedTopicsNMF,selectedSummaryNMF,selectedTopicsLDA,selectedSummaryLDA):
    setupEnvironment()
    for i in selectedSummaryNMF:
        document=i;
        summary = extractSentences(document)
        phrases = extractKeyPhrases(document)
        summaryNMF.append(summary)
        phrasesNMF.append(phrases)

    for i in selectedSummaryLDA:
        document=i;
        summary = extractSentences(document)
        phrases = extractKeyPhrases(document)
        summaryLDA.append(summary)
        phrasesLDA.append(phrases)

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

if __name__=="__main__":
    start(NMF,LDA)

