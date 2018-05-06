import re
from textblob import TextBlob

def getlists(obj):
    topics=[]
    summary=[]
    for i in range(0,len(obj)):
        topics.append(obj[i]['name'])
        summary.append(obj[i]['summary'])
    return [topics,summary]

def cleanTweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

def getTweetSentiment(tweet):
    analysis = TextBlob(cleanTweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def getPolarity(obj):
    [topics, summary] = getlists(obj)
    polarity=[]
    for i in range(0,len(summary)):
        polarity.append(getTweetSentiment(summary[i]))

    res = []
    for i in range(0, len(polarity)):
        res.append({'name': topics[i], 'polarity': polarity[i]})
    return res
