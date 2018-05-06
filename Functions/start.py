# 4 functions
import getTweets
import getTopics
import getSummary
import getPolarity
import installPackages

#To install packages locally
installPackages.installPackages()

#Returns tweets: [{'name','tweet'}]
tweetsObj=getTweets.getTweets('jpmorgan')

#Returns topics: [{'name','phrase'}]
topicsObj=getTopics.getTopics(tweetsObj)

#Returns summary: [{'name','summary'}]
summaryObj=getSummary.getSummary(topicsObj)

#Returns polarity: [{'name',''polarity'}]
polarityObj=getPolarity.getPolarity(summaryObj)
