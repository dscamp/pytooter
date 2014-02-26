# -- encoding: utf-8 --
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "47bmTikS9WrBjKrLlRBj6A"
CONSUMER_SECRET = "boHRIxpknhHu6du7K34eazsfW4nzh6nGHCodq2YM"

OAUTH_TOKEN = "499334286-GpsM5dVu48vEANQ2hJ3238nUG60uvZx1Kj36xvSu"
OAUTH_TOKEN_SECRET = "Jb8oH8pl7sBMzj9zq3SjXprDsV2zmLaXHfQKOptKpZbn8"


def setup_oauth():
    """Authorize your app via identifier."""
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


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def get_timeline():
    oauth = get_oauth()
    r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=srbaker&count=20", auth=oauth)
    results = r.json()
    tweets = dict()
    for post in results:
        text = post['text']
        id = post['id']
        tweets[id] = text

    lines = list()
    for key in tweets.keys():
        tweet = tweets[key]
        if "mtGox".lower() in tweet.lower():
             s =  "key: "
             s += str(key)
             s += ", tweet: "
             s += tweets[key]
             s += "\n"
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
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        tweet = get_timeline()
        write_to_file(tweet)
        #print_to_console(tweet)


