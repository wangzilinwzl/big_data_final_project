import tweepy
import json
#from tweepy.auth import OAuthHandle
consumer_key = "LA9lLOcniFkuSp77SeBqS6JiA"  
consumer_secret = "PRQkwBGnXyf7l4uDVGi8syeDb4cHIjTejbnDx0a34QSXy2X5Ub"  
access_token = "913782248054444034-lCvaHYcFYB5J2rrvByKfsUAZJzo4QQa"  
access_token_secret = "T3WlcgcE9oxhHApJEjzJoeLObophmMSjherHMnzxxpGTk" 

# 创建认证对象
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
# 设置你的access token和access secret
auth.set_access_token(access_token, access_token_secret)  
# 传入auth参数，创建API对象
api = tweepy.API(auth)  


'''
# 待拉取微博的用户
name = "nytimes"  
# 待拉取的微博数量
tweetCount = 1

# 使用上面的参数，调用user_timeline函数
results = api.user_timeline(id=name, count=tweetCount)

fil_out = open("twit_out.txt", "w")

# 遍历所拉取的全部微博
json_str = ""
for tweet in results:  
    #fil_out.write(tweet.text)
    #print (type(tweet))
    #print (tweet)
    #json_str = json.dumps(tweet._json)
    #print(json_str)
    json_str = json.dumps(tweet._json)

json.dump(json_str, fil_out)
# 打印存在微博对象中的text字段
#print (tweet.text)


# 使用API对象获取你的时间轴上的微博，并把结果存在一个叫做public_tweets的变量中
#public_tweets = api.home_timeline()  
# 遍历所拉取的全部微博
#for tweet in public_tweets:  
   # 打印存在微博对象中的text字段
   #print (tweet.text)
'''

def get_some_tweets(screen_name):
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    

    #tweetCount
    tweetCount = 2

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=tweetCount)
    alltweets.extend(new_tweets)

    #write tweet objects to JSON
    #file = open('tweet.json', 'wb') 
    file = open('tweet.json', 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json, file, sort_keys = True, indent = 4)
    
    #close the file
    print ("Done")
    file.close()

def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    

    #tweetCount
    tweetCount = 2
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=tweetCount)
    #new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))
       
    #write tweet objects to JSON
    file = open('tweet.json', 'wb') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
    
    #close the file
    print ("Done")
    file.close()

if __name__ == '__main__':
    name = "nytimes"  
    #pass in the username of the account you want to download
    get_some_tweets(name)
    #get_all_tweets(name)