from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np

def displayTopics(H,W,featureNames,tweets,noOfTopWords,noOfTopDocuments):
    for topicId,topic in enumerate(H):
        print "\nTopic %d:" % (topicId)
        print " ".join([featureNames[i]
                        for i in topic.argsort()[:-noOfTopWords-1:-1]])
        topDocIndices=np.argsort(W[:,topicId])[::-1][0:noOfTopDocuments]
        for docIndex in topDocIndices:
            print tweets[docIndex]

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def getTweetsForSummary(H,W,featureNames,tweets,noOfTopWords,noOfTopDocuments):
    summaryList=[]
    topicsList=[]
    for topicId,topic in enumerate(H):
        eachTopicList=[]
        newEachTopicList=[]
        for i in topic.argsort()[:-noOfTopWords - 1:-1]:
            eachTopicList.append(featureNames[i])

        for i in eachTopicList:
            j = i.encode('ascii', 'ignore')
            newEachTopicList.append(j)

        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpmorgan')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'chase')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpmc')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpm')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpmchase')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpmorgans')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jpmorganchase')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jp')

        topicsList.append(newEachTopicList[0])

        topDocIndices=np.argsort(W[:,topicId])[::-1][0:noOfTopDocuments]
        tweetList=""
        for docIndex in topDocIndices:
            tweetList=tweetList+tweets[docIndex]+'. '
        summaryList.append(tweetList)

    return [topicsList,summaryList]

def start(tweeters,tweets):
    noOfFeatures=2000
    noTopics=input("Number of topics: ")

    #NMF
    tfidfVectorizer=TfidfVectorizer(max_df=0.95,min_df=2,max_features=noOfFeatures,stop_words='english')
    tfidf=tfidfVectorizer.fit_transform(tweets)
    tfidfFeatureNames=tfidfVectorizer.get_feature_names()
    nmfModel=NMF(n_components=noTopics,random_state=1,alpha=.1,l1_ratio=.5,init='nndsvd').fit(tfidf)
    nmfW=nmfModel.transform(tfidf)
    nmfH=nmfModel.components_

    #LDA
    tfVectorizer=CountVectorizer(max_df=0.95,min_df=2,max_features=noOfFeatures,stop_words='english')
    tf=tfVectorizer.fit_transform(tweets)
    tfFeatureNames=tfVectorizer.get_feature_names()
    ldaModel=LatentDirichletAllocation(n_components=noTopics,max_iter=5,learning_method='online',learning_offset=50.,random_state=0).fit(tf)
    ldaW=ldaModel.transform(tf)
    ldaH=ldaModel.components_

    noOfTopWords=15
    noOfTopDocuments=15
    #displayTopics(nmfH,nmfW,tfidfFeatureNames,tweets,noOfTopWords,noOfTopDocuments)
    #displayTopics(ldaH,ldaW,tfFeatureNames,tweets,noOfTopWords,noOfTopDocuments)
    [topicsListNMF,summaryListNMF]=getTweetsForSummary(nmfH,nmfW,tfidfFeatureNames,tweets,noOfTopWords,noOfTopDocuments)
    [topicsListLDA,summaryListLDA]=getTweetsForSummary(ldaH,ldaW,tfFeatureNames,tweets,noOfTopWords,noOfTopDocuments)
    
if __name__=="__main__":
    start()