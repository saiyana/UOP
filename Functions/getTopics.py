from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def getTweetsForSummary(H, W, featureNames, tweets, noOfTopWords, noOfTopDocuments):
    summaryList = []
    topicsList = []
    for topicId, topic in enumerate(H):
        eachTopicList = []
        newEachTopicList = []
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
        newEachTopicList = remove_values_from_list(newEachTopicList, 'chasebank')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'chase')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'customer')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'chasesupport')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'help')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'bank')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'morgan')
        newEachTopicList = remove_values_from_list(newEachTopicList, 'jp')
        newEachTopicList = remove_values_from_list(newEachTopicList, "'")
        newEachTopicList = remove_values_from_list(newEachTopicList, '"')

        topicsList.append(newEachTopicList[0])

        topDocIndices = np.argsort(W[:, topicId])[::-1][0:noOfTopDocuments]
        tweetList = ""
        for docIndex in topDocIndices:
            tweetList = tweetList + tweets[docIndex] + '. '
        summaryList.append(tweetList)

    return [topicsList, summaryList]

def getlists(obj):
    tweeters=[]
    tweets=[]
    for i in range(0,len(obj)):
        tweeters.append(obj[i]['name'])
        tweets.append(obj[i]['tweet'])
    return [tweeters,tweets]

def getTopics(obj):
    [tweeters,tweets]=getlists(obj)
    noOfFeatures = 2000
    noTopics=5

    # NMF
    tfidfVectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=noOfFeatures, stop_words='english')
    tfidf = tfidfVectorizer.fit_transform(tweets)
    tfidfFeatureNames = tfidfVectorizer.get_feature_names()
    nmfModel = NMF(n_components=noTopics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
    nmfW = nmfModel.transform(tfidf)
    nmfH = nmfModel.components_

    # LDA
    tfVectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=noOfFeatures, stop_words='english')
    tf = tfVectorizer.fit_transform(tweets)
    tfFeatureNames = tfVectorizer.get_feature_names()
    ldaModel = LatentDirichletAllocation(n_components=noTopics, max_iter=5, learning_method='online',
                                         learning_offset=50., random_state=0).fit(tf)
    ldaW = ldaModel.transform(tf)
    ldaH = ldaModel.components_

    noOfTopWords = 15
    noOfTopDocuments = 15
    [topicsListNMF, summaryListNMF] = getTweetsForSummary(nmfH, nmfW, tfidfFeatureNames, tweets, noOfTopWords,
                                                          noOfTopDocuments)
    [topicsListLDA, summaryListLDA] = getTweetsForSummary(ldaH, ldaW, tfFeatureNames, tweets, noOfTopWords,
                                                          noOfTopDocuments)

    resultTopics=topicsListLDA+topicsListNMF
    resultSummary=summaryListLDA+summaryListNMF
    l = []
    m = []
    l.append(resultTopics[0])
    m.append(resultSummary[0])

    for i in range(1, len(resultTopics)):
        if resultTopics[i] in l:
            temp = l.index(resultTopics[i])
            m[temp] = m[temp] + resultSummary[i]
        else:
            l.append(resultTopics[i])
            m.append(resultSummary[i])

    res = []
    for i in range(0, len(l)):
        res.append({'name': l[i], 'phrase': m[i]})
    return res
