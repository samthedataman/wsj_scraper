from operator import contains
import selenium 
import pprint
from selenium import webdriver
import pandas as pd
import numpy as np
import requests as r
import nltk
import pprint
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from sklearn.feature_extraction.text import CountVectorizer
import random; random.seed(53)
import undetected_chromedriver as uc
import time
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import pprint
import json
import itertools  
import regex as re
from contextlib import suppress
import os
import datetime as dt 
from datetime import date,datetime,timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")


TODAY_TIME = dt.datetime.now()
TODAY_DATE = dt.datetime.now().strftime("%m-%d-%Y")
regex_pattern = r'Reply\d{0,}'
date_patern_regex = r'(\d{2}|\d{1})\s(March|April|May|June|July|August|September|October|November|December|January|February),\s\d{4}'
date_patern_regex_2 = r'\d{1,2}\sM'
date_patern_regex_3 = r'\d{1,2}\sH' 
date_patern_regex_4 = r'\d{1,2}\sS' 


def time_converter(col):
    if col is None:
        time_ = TODAY_TIME
    elif bool(re.search(date_patern_regex_2,col)) == True:
        match = ''.join(re.findall(date_patern_regex_2,col))
        match = int(match.replace('M',''))
        time_ = TODAY_TIME-timedelta(minutes=match)
    elif bool(re.search(date_patern_regex_4,col)) == True:
        match = ''.join(re.findall(date_patern_regex_4,col))
        match = int(match.replace('S',''))
        time_ = TODAY_TIME-timedelta(seconds=match)
    elif bool(re.search(date_patern_regex_3,col)) == True:
        match = ''.join(re.findall(date_patern_regex_3,col))
        match = int(match.replace('H',''))
        time_ = TODAY_TIME-timedelta(hours=match)
    elif bool(re.search(date_patern_regex,col))==True:
         time_ = pd.to_datetime(re.search(date_patern_regex,col)[0])
    elif 'Just Now' in col:
        time_ = TODAY_TIME
    elif '1 day ago' in col:
        col = int(col.replace('1 day ago','24'))
        time_ = TODAY_TIME-timedelta(hours=col)
    elif '2 days ago' in col:
        col = int(col.replace('2 days ago','48'))
        time_ = TODAY_TIME-timedelta(hours=col)       
    elif '3 days ago' in col:
        col = int(col.replace('3 days ago','72'))
        time_ = TODAY_TIME-timedelta(hours=col)       
    elif '4 days ago' in col:
        col = int(col.replace('4 days ago','96'))
        time_ = TODAY_TIME-timedelta(hours=col)
    elif '5 days ago' in col:
        col = int(col.replace('5 days ago','120'))
        time_ = TODAY_TIME-timedelta(hours=col)
    elif '6 days ago' in col:
        col = int(col.replace('6 days ago','144'))
        time_ = TODAY_TIME-timedelta(hours=col)
    elif '7 days ago' in col:
        col = int(col.replace('7 days ago','168'))
        time_ = TODAY_TIME-timedelta(hours=col)        
    return time_
    
def get_votes(col):
    col = re.findall(regex_pattern,col)
    col =  ''.join(col)
    col = col.replace('Reply','')
    return col

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()
#tokenize,stem, and remove stop words from text
def cleanText(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text
#word count function
def word_count(string):
    split = string.split()
    count = len(split)
    return count
#count emojis
def count_emojis(string):
    em_count = len(re.findall(r'[^\w\s,.]', string))
    return em_count
#count hashtags
def count_hashtags(string):
    em_count = len(re.findall(r'[\#]', string))
    return em_count
#count mentions
def count_mentions(string):
    em_count = len(re.findall(r'[\@]', string))

def text_analyzer(df):
    #feature creation{Word Count|character count|emoji count|link count}
    df['Comment'] = df['Comment'].astype('str')
    df['word_count'] = df['Comment'].apply(word_count)
    df['character_count'] = [len(each) for each in df['Comment']]
    df['link_count'] = df['Comment'].str.count(r'(http)')
    df['emoji_count'] = df['Comment'].apply(count_emojis)
    df['hashtag_count'] = df['Comment'].apply(count_hashtags)
    df['mention_count'] = df['Comment'].apply(count_mentions)
    #create other features including word count+sentiment based features
    sid = SentimentIntensityAnalyzer()
    df['polarity_pos'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['pos'])
    df['polarity_neg'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['neg'])
    df['polarity_neu'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['neu'])
    df['polarity_compound'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['compound'])
    return df

#######LOG INTO WSJ############
driver = webdriver.Chrome('./chromedriver',options=chrome_options)
driver.get('https://sso.accounts.dowjones.com/login?state=hKFo2SAyaEVBbUlxVVlqV0w5blRIVnFGYWtNSlpCYmwwaXJUd6FupWxvZ2luo3RpZNkgTkV4djhHWVJKZl9KX0ZVNVVSMTJzR0FXZDI3bC1BaE-jY2lk2SA1aHNzRUFkTXkwbUpUSUNuSk52QzlUWEV3M1ZhN2pmTw&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid%20createTimestamp&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=8b0c1450-b8a6-4f08-88de-8ee4c1e877e5&ui_locales=en-us-x-wsj-215-2&mars=-1&ns=prod%2Faccounts-wsj#!/signin')
search = driver.find_element_by_class_name("username")
time.sleep(5)
search.send_keys("samuel.savage@uconn.edu")
driver.find_element_by_xpath('//*[@id="basic-login"]/div[1]/form/div[2]/div[6]/div[1]/button[2]').click()
time.sleep(5)
password = driver.find_element_by_id("password-login-password")
password.send_keys("0ldSp!ce")
time.sleep(5)
button =  driver.find_element_by_xpath('//*[@id="password-login"]/div/form/div/div[5]/div[1]/button') 
button.click()
time.sleep(20)

##############GET ALL pages on WSJ###############################
head_links = []
header_links = driver.find_elements_by_class_name("style--section-link--2rDVp5ht")

for header in header_links:
    head_links.append(header.get_attribute("href"))
print(f'scraper visting \n {len(head_links)} links ')
##############GET ALL LINKS TO CONVERSATIONS###############################

for i in head_links:
    nav_section_name = i
    driver.get(i)
    print(i)
    links_list = []
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if str(elem.get_attribute('href')).startswith("https://www.wsj.com/articles"):
            links_list.append(elem.get_attribute('href'))
    print(f"We are scraping a total of {len(links_list)} links")

    #####################MAKING METADATA LISTS################################
    conversation_list = []
    names_list = []
    date_list = []
    all_data_raw_list=[]
    ############################GRAB EACH LINK AND LET PAGE LOAD##################

    for _ in list(set(links_list)):
        driver.get(_)
        name_of_article = re.split(r'-\d',_.replace('https://www.wsj.com/articles','').replace('/',''))[0]
        print(f'going to [ {name_of_article} ]' )
        link_to_article = _
        time.sleep(15)
    ############################SHOWHING CONVERSATION BUTTON CLICK##############################
        
        print("looker for conversations")
        # clicker
        try:
            clicker = driver.find_element_by_xpath('//*[@id="comments_sector"]/button')
            print(1)
            clicker.click()
        except:
            try:
                clicker = driver.find_element_by_xpath("//button[contains(text(),'conversation_toggle')]")
                print(2)
                clicker.click()
            except:
                try:
                    clicker = driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.document.querySelector(\'[class=\"conversation-caret\"\')")
                    print(3)
                    clicker.click()
                except:
                    try:
                        clicker = driver.execute_script("return document.querySelector(\'[class=\"conversation-caret\"\')"),
                        print(4)
                        clicker.click()
                    except:
                        try:
                            clicker = driver.find_element_by_id("conversation-container").find_elements_by_tag_name("button")[0]
                            print(5)
                            clicker.click()
                        except:
                            print("variable clicker could not be set")
                            pass
        counter = 0
        time.sleep(4)
        #######################SHOWING MORE BUTTON BEING CLICKED######################### (30 button clicks should capture most of the data)
        try:
            counter_targ = 0
            target = driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
            while target.is_displayed():
                target.click()
                time.sleep(20)
                counter +=1
                print(f'button clicked {counter} times')
                target = driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
                break 
        except:
            continue
        #####################EXPANDING REPLYS############################################    
        try:
            replies = driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.querySelectorAll(\"[data-open-web-class='conversation-message-show-replies']\")")
        except:
                continue
        for reply in replies:
            try:
                reply.click()
                print("finding replies")
            except:
                continue 
        #######################EXPANDING SEE MORE (LONER COMMENTS)###############    
        try:
            see_more =  driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class='message-text'] > span\")")
        except:
            continue    
        for s in see_more:
            try:
                s.click()
            except:
                continue
        
        time.sleep(5)
        #########v######################GETTING METADATA##################################    
        names_raw = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\\\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]\')[0].shadowRoot.querySelectorAll(\"[class=\'Typography__text--11-1-17 Typography__t4--11-1-17 Typography__l6--11-1-17 src-components-Username-index__wrapper src-components-Username-index__truncated src-components-Username-index__button\'\")")
        time.sleep(2)
        texts_raw =  driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class='message-text']\")")
        time.sleep(2)
        date_raw = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\\\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]\')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class=\'message-timestamp\'\")")
        time.sleep(2)
        all_data_raw = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\\\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]\')[0].shadowRoot.querySelectorAll(\"[class=\'components-MessageLayout-index__message-container\'\")")
        ####################TRY PRINTING SAMPLE DATA######################
        try:
            print(len(names_raw))
            print(len(texts_raw))
            print(len(date_raw))
            print(len(all_data_raw))
        except:
            continue
        ####################APPENDING DATA TO LISTS##################################
        for raw in all_data_raw:
            all_data_raw_list.append(str(raw.get_property('textContent')))
        print(all_data_raw_list)    
        for hour in date_raw:
            date_list.append(str(hour.get_property('textContent')).replace('hours ago','H').replace('hour ago','H').replace('minutes ago','M').replace('seconds ago','S').replace('minute ago','M').replace('Just Now','1 M'))
        print(date_list)
        for name in names_raw:
            names_list.append(name.get_property('textContent'))
        print(names_list)     
        for i in texts_raw:
            conversation_list.append(i.get_attribute('innerHTML'))
        print(conversation_list)
        zipped = list(itertools.zip_longest(date_list,conversation_list,names_list,all_data_raw_list))
        df = pd.DataFrame(zipped,columns=['Date_Posted','Comment','Username','Upvotes'])
        df['Upvotes'] = df['Upvotes'].apply(lambda x: get_votes(x))
        print(name_of_article,'===',link_to_article)
        for i in df['Date_Posted']:
            print(i)
        df['Date_Posted'] = df['Date_Posted'].apply(lambda x : time_converter(x))
        df['date_retrieved'] = TODAY_DATE
        df['article_name'] = name_of_article
        df['link'] = link_to_article
        df['sections'] = nav_section_name
        df = text_analyzer(df)
        print(df.columns) 
        path = f'/Users/samsavage/Desktop/Urban Dictionary/WSJ Data/{TODAY_DATE}'
        if os.path.exists(path) == False:
            os.mkdir(path)
        df.to_csv(f'{path}/{TODAY_DATE}_{name_of_article}.csv')
        all_data_raw_list.clear()
        date_list.clear()
        names_list.clear()
        conversation_list.clear()
        names_raw.clear()
        texts_raw.clear()
        date_raw.clear()
        all_data_raw.clear()

##############read meta data to master file##################################
path = f'/Users/samsavage/Desktop/Urban Dictionary/WSJ Data/{TODAY_DATE}'
file_cats =[]
for file in os.listdir(path):
    try:
        df = pd.read_csv(f'{path}/{file}')
        print("apending file")
    except:
        continue
    file_cats.append(df)
    master_df = pd.concat(file_cats)
master_df = master_df.drop_duplicates()
master_df.to_csv(f"{path}/MasterCSV_{TODAY_DATE}.csv")

##############################################################################
