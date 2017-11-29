import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.ml.feature import StringIndexer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.datasets import dump_svmlight_file
from sklearn.datasets import *
import numpy as np
import os

# Authentication 

consumer_key = "LA9lLOcniFkuSp77SeBqS6JiA"  
consumer_secret = "PRQkwBGnXyf7l4uDVGi8syeDb4cHIjTejbnDx0a34QSXy2X5Ub"  
access_token = "913782248054444034-lCvaHYcFYB5J2rrvByKfsUAZJzo4QQa"  
access_token_secret = "T3WlcgcE9oxhHApJEjzJoeLObophmMSjherHMnzxxpGTk" 

# Geographic location
GEOBOX_NYC = [-74.1687, 40.5722, -73.8062, 40.9467]
allTweets = []

tweetCount = 0


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_status(self, status):
        #print(status)
        global tweetCount
        global allTweets
        print('Status')
        print(tweetCount)
        tweetCount += 1
        allTweets.append(status)
        if tweetCount >= 5:
            return False
        return True

    '''
    def on_data(self, data):
        print (data)
        #print("Data")
        return True
    '''

    def on_error(self, status):
        print ("Error Status")
        print (status)

def dump_all_tweets(allTweets, fileName = 'all_tweets.json'):
    file = open(fileName, 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in allTweets:
        json.dump(status._json, file, sort_keys = True, indent = 4)
    file.close()

if __name__ == '__main__':
    tweetCount = 0
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.filter(locations = GEOBOX_NYC)

    print (len(allTweets))
    dump_all_tweets(allTweets)
    # Dump
    #for status in allTweets:
    #    json.dump(status._json, file, sort_keys = True, indent = 2)


conf = SparkConf().setAppName("Jack").setMaster("local")
#sc.stop()
sc = SparkContext.getOrCreate(conf = conf)
spark = SparkSession.builder.appName("Python Spark SQL Example").getOrCreate()

category_list = ['business', 'entertainment', 'politics', 'sport', 'tech']
root_dir = '/home/crossluna/big_data_analytics/hw2/Q2/bbc/'
text = []
labels = []