import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Authentication 

consumer_key = "LA9lLOcniFkuSp77SeBqS6JiA"  
consumer_secret = "PRQkwBGnXyf7l4uDVGi8syeDb4cHIjTejbnDx0a34QSXy2X5Ub"  
access_token = "913782248054444034-lCvaHYcFYB5J2rrvByKfsUAZJzo4QQa"  
access_token_secret = "T3WlcgcE9oxhHApJEjzJoeLObophmMSjherHMnzxxpGTk" 

# Geographic location
GEOBOX_NYC = [-74.1687, 40.5722, -73.8062, 40.9467]
#TAGS = ['NFL', 'NBA', 'MLB']
TAGS = []
allTweets = []

tweetCount = 0
max_tweet_count = 30


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
        if tweetCount >= max_tweet_count:
            return False
        return True

    '''
    def on_data(self, data):
        #print (data)
        print("Data")
        return True
    '''

    def on_error(self, status):
        print ("Error Status")
        print (status)

def dump_all_tweets_text(allTweets, fileName = 'all_tweets_text.txt'):
    file = open(fileName, 'w') 
    print ("Writing tweet objects to JSON text please wait...")
    for status in allTweets:
        #json.dump(status._json, file, sort_keys = True, indent = 4)
        #file.write(json)
        #js_obj = json.loads(status._json)
        js_obj = status._json
        #print(js_obj['text'])
        file.write(js_obj['text'] + '\n')
        #print(js_obj['text'])
    file.close()

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
    stream.filter(locations = GEOBOX_NYC, track=TAGS, languages=["en"])

    print (len(allTweets))
    dump_all_tweets_text(allTweets)

