# -- encoding: utf-8 --
from __future__ import unicode_literals
import requests
import ConfigParser
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"



class oauth():
    def setup_oauth(self):
        # Request token
        oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
        r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(r.content)
        
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
        
        # Authorize
        authorize_url = AUTHORIZE_URL + resource_owner_key
        print 'Please go here and authorize: ' + authorize_url
        
        verifier = raw_input('Please input the verifier: ')
        oauth = OAuth1(CONSUMER_KEY,
                       client_secret=CONSUMER_SECRET,
                       resource_owner_key=resource_owner_key,
                       resource_owner_secret=resource_owner_secret,
                       verifier=verifier)
        
        # Finally, Obtain the Access Token
        r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
        credentials = parse_qs(r.content)
        token = credentials.get('oauth_token')[0]
        secret = credentials.get('oauth_token_secret')[0]
        
        return token, secret
        
        
    def get_oauth(self, consumer_key, consumer_secret, oauth_token, oauth_secret_token):
        oauth = OAuth1(consumer_key,
                       client_secret=consumer_secret,
                       resource_owner_key=oauth_token,
                       resource_owner_secret=oauth_token_secret)
        return oauth
            
class timeline:
    def get_timeline(self, oauth, user):
        the_url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=20" %user
        r = requests.get(url=the_url, auth=oauth)
        print (r.url)
        results = r.json()
        tweets = dict()
        for post in results:
            text = post['text']
            print text.encode('utf-8')
            id = post['id']
            tweets[id] = text
            
            lines = list()
            for key in tweets.keys():
                tweet = tweets[key]
                #if "i".lower() in tweet.lower():
                s =  "key: "
                s += str(key)
                s += ", tweet: "
                s += tweets[key]
                s += "\n"
                print s.encode('utf-8')
                lines.append(s)
                return lines
                    

def print_to_console(tweets):
    for tweet in tweets:
        print tweet.encode('utf-8', 'replace')
        

def write_to_file(tweets):
    with open('tweets.txt', 'w') as f:
        for tweet in tweets:
            f.write(tweet.encode('utf-8', 'replace'))


if __name__ == "__main__":


    config = ConfigParser.ConfigParser()
    config.read('keys.cfg')
    consumer_key = config.get("CONSUMER", "consumer_key")
    consumer_secret = config.get("CONSUMER", "consumer_secret")
    oauth_token = config.get("OAUTH", "oauth_token")
    oauth_token_secret = config.get("OAUTH", "oauth_token_secret")
    user_name = config.get("USER", "name")


    
    if not oauth_token:
        oauth = oauth()
        token, secret = oauth.setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = oauth().get_oauth(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
        timeline = timeline()
        tweet = timeline.get_timeline(oauth, user_name)
        write_to_file(tweet)
        #print_to_console(tweet)


