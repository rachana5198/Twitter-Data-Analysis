from tkinter import *

#import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
class TwitterClient(): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
   
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'doy9NycSZzfOOiyFzHcMvZP29'
        consumer_secret = 'jz0LF5xbUsFhXSTsQ1HdK0r4TI0DhpPzPmDMTWXLLmE5mItVE1'
        access_token = '1104366027628961793-INNzshj2De9RgivIdEdiy6uym9XKvy'
        access_token_secret = 'LEnKUCmMWeg1EXPAMDnRRTVBmsUUQtHKm5NHIu0QyPkpr'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets
            #print(tweets)
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))
def data():
    print(e1.get())
    # creating object of TwitterClient Class 
    api = TwitterClient()
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    # calling function to get tweets 
    tweets = api.get_tweets(query = e1.get(), count = 200) 
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets
    p=100*len(ptweets)/len(tweets)
   # print(p)
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    n=100*len(ntweets)/len(tweets)
    ltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
    print("Neutral tweets percentage: {} %".format(100*len(ltweets)/len(tweets)))
    l=100*len(ltweets)/len(tweets)
    
    Label(root, text='Positive Tweets: '+str(p)+"%").pack()
    Label(root, text='Negative Tweets: '+str(n)+"%").pack()
    Label(root, text='Neutral Tweets: '+str(l)+"%").pack()
   # Label(root, text='Positive Tweets: '+str(ptweets)).pack()
    print("\n\nPositive tweets:")
    Label(root, text='Pie Chart').pack()
    labels = 'Positive', 'Negative','Neutral'
    sizes = [p, n,l]
    colors = ['green', 'red', 'yellow']
    explode = (0, 0.1,0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    canvas = FigureCanvasTkAgg(fig1,master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    for tweet in ptweets[:10]: 
        print(tweet['text'].translate(non_bmp_map))

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text'].translate(non_bmp_map))
        
root = Tk()
frame = Frame(root) 
frame.pack() 
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM ) 
l=Label(frame, text='Enter a topic')
l.pack( side = LEFT)
print(l)
e1 = Entry(frame)
e1.pack(side = RIGHT)
#e2 = Entry(master) 
redbutton = Button(root,text="Search", command=data)
redbutton.pack() 



#e2.grid(row=1, column=1) 
mainloop()
