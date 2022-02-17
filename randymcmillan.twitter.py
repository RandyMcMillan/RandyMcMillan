#!/usr/bin/env python3
# https://github.com/geduldig/TwitterAPI
import sys
import os
import requests
import shutil
import importlib
from importlib.resources import read_text
import time
import blockcypher
import pyjq
os.environ['PYTHONPATH']
sys.path.append('.')
sys.path.append("/usr/local/lib/python3.7/site-packages")
from TwitterAPI import TwitterAPI

def moveBlockTime():
    try:
        shutil.move(os.getcwd()+"/BLOCK_TIME", os.getcwd()+"/OLD_BLOCK_TIME")
    except:
        f = open("BLOCK_TIME", "w")
        f.write("" + 0 + "\n")
        f.close()

def getMillis():
    global millis
    millis = int(round(time.time() * 1000))
    return millis

def getSeconds():
    global seconds
    seconds = int(round(time.time()))
    return seconds

def blockTime():
    try:
        global block_time
        block_time = blockcypher.get_latest_block_height(coin_symbol='btc')
        global block_height
        block_height = repr(block_time)
        f = open("BLOCK_TIME", "w")
        f.write("" + block_height + "\n")
        f.close()
        return block_time
    except:
        return 0
        pass

def BTC_UNIX_TIME():
    global BTC_UNIX_TIME
    BTC_UNIX_TIME = str(blockTime())+":"+str(getSeconds())
    return BTC_UNIX_TIME

def getData(filename):
    f = open(filename)
    global data
    data = f.read()
    f.close()
    return data

def tweetBlockTime(block_time):
    if (block_time != obt):
        # r = api.request('statuses/update', {'status': block_time+":"+getSeconds })
        r = api.request('statuses/update', {'status': BTC_UNIX_TIME() })
        # print(BTC_UNIX_TIME)
        # exit()
        if (r.status_code == 200):
            print('api.request SUCCESS')
        else:
            print('api.request FAILURE')
    else:
        print('tweetBlockTime() FAILURE')

def getMempoolAPI(url,DATA):
    # print(url)
    with open(DATA, 'wb') as f:
        r = requests.get(url, stream=True)
        f.writelines(r.iter_content(1024))
        response = getData(DATA)
        # print(getData(DATA))
        # print(response)

def searchBitcoin():
    r = api.request('search/tweets', {'q':'bitcoin'})
    for item in r:
        print(item)

BLOCK_TIP_HEIGHT        = os.path.expanduser('./BLOCK_TIP_HEIGHT')
DIFFICULTY              = os.path.expanduser('./DIFFICULTY')
OLD_BLOCK_TIME          = os.path.expanduser('./OLD_BLOCK_TIME')
ACCESS_TOKEN_SECRET     = os.path.expanduser('./twitter_access_tokens/access_token_secret.txt')
ACCESS_TOKEN            = os.path.expanduser('./twitter_access_tokens/access_token.txt')
CONSUMER_API_KEY        = os.path.expanduser('./twitter_access_tokens/consumer_api_key.txt')
CONSUMER_API_SECRET_KEY = os.path.expanduser('./twitter_access_tokens/consumer_api_secret_key.txt')

cak  = getData(CONSUMER_API_KEY)
cask = getData(CONSUMER_API_SECRET_KEY)
at   = getData(ACCESS_TOKEN)
ats  = getData(ACCESS_TOKEN_SECRET)
obt  = getData(OLD_BLOCK_TIME)

api  = TwitterAPI(cak,cask,at,ats)

getMempoolAPI('https://mempool.space/api/v1/difficulty-adjustment', DIFFICULTY)
getMempoolAPI('https://mempool.space/api/blocks/tip/height',        BLOCK_TIP_HEIGHT)
# searchBitcoin()
# print(blockTime())
# print(getMillis())
# print(getSeconds())
tweetBlockTime(blockTime())

