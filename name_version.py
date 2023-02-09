# from operator import contains
# import selenium
# import pprint
# from selenium import webdriver
# import pandas as pd
# import numpy as np
# import requests as r
# import nltk
# import ssl
# import pprint
# from nltk.tokenize import sent_tokenize, word_tokenize
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download('punkt')
# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# sid = SentimentIntensityAnalyzer()
# from sklearn.feature_extraction.text import CountVectorizer
# import random; random.seed(53)
# import undetected_chromedriver as uc
# import time
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import WebDriverException
# import pprint
# import json
# import itertools
# import pandas as pd
# import regex as re
# from contextlib import suppress
# import os
# import datetime as dt
# from datetime import date,datetime,timedelta
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import ActionChains
# from datetime import timedelta
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
#
# # chrome_options = Options()
# # chrome_options.add_argument("--window-size=1920,1080")
# print("josh is the man")
# # TODAY_TIME = dt.datetime.now()
# # TODAY_DATE = dt.datetime.now().strftime("%m-%d-%Y")
# # regex_pattern = r'Reply\d{0,}'
# # date_patern_regex = r'(\d{2}|\d{1})\s(March|April|May|June|July|August|September|October|November|December|January|February),\s\d{4}'
# # date_patern_regex_2 = r'\d{1,2}\sM'
# # date_patern_regex_3 = r'\d{1,2}\sH'
# # date_patern_regex_4 = r'\d{1,2}\sS'
# # date_patern_regex_w = r'\d{0,}w\sago'
# # date_patern_regex_d = r'\d{0,}d\sago'
# # date_patern_regex_h = r'\d{0,}h\sago'
# # date_patern_regex_y = r'\d{0,}y\sago'
# # date_patern_regex_s = r'\d{0,}s\sago'
# # date_patern_regex_all = r'\d{0,}(s|w|y|d|m|h)'
#
#
#
#
# # def time_converter(col):
# #     time_ = ''
# #     if col is None:
# #         time_ = TODAY_TIME
# #     elif bool(re.search(date_patern_regex_2,col)) == True:
# #         match = ''.join(re.findall(date_patern_regex_2,col))
# #         match = int(match.replace('M',''))
# #         time_ = TODAY_TIME-timedelta(minutes=match)
# #     elif bool(re.search(date_patern_regex_4,col)) == True:
# #         match = ''.join(re.findall(date_patern_regex_4,col))
# #         match = int(match.replace('S',''))
# #         time_ = TODAY_TIME-timedelta(seconds=match)
# #     elif bool(re.search(date_patern_regex_3,col)) == True:
# #         match = ''.join(re.findall(date_patern_regex_3,col))
# #         match = int(match.replace('H',''))
# #         time_ = TODAY_TIME-timedelta(hours=match)
# #     elif bool(re.search(date_patern_regex,col))==True:
# #         time_ = pd.to_datetime(re.search(date_patern_regex,col)[0])
# #     elif 'Just Now' in col:
# #         time_ = TODAY_TIME
# #     elif '1 day ago' in col:
# #         col = int(col.replace('1 day ago','24'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '2 days ago' in col:
# #         col = int(col.replace('2 days ago','48'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '3 days ago' in col:
# #         col = int(col.replace('3 days ago','72'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '4 days ago' in col:
# #         col = int(col.replace('4 days ago','96'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '5 days ago' in col:
# #         col = int(col.replace('5 days ago','120'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '6 days ago' in col:
# #         col = int(col.replace('6 days ago','144'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif '7 days ago' in col:
# #         col = int(col.replace('7 days ago','168'))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif bool(re.search(date_patern_regex_w,col)) == True:
# #         col = ''.join(re.findall(date_patern_regex_w,col))
# #         col = col.replace('ago','')
# #         col = int(col.replace('w',''))
# #         time_ = TODAY_TIME-timedelta(weeks=col)
# #     elif bool(re.search(date_patern_regex_s,col)) == True:
# #         col = ''.join(re.findall(date_patern_regex_s,col))
# #         col = col.replace('ago','')
# #         col = int(col.replace('s',''))
# #         time_ = TODAY_TIME-timedelta(seconds=col)
# #     elif bool(re.search(date_patern_regex_d,col)) == True:
# #         col = ''.join(re.findall(date_patern_regex_d,col))
# #         col = col.replace('ago','')
# #         col = int(col.replace('d',''))
# #         time_ = TODAY_TIME-timedelta(days=col)
# #     elif bool(re.search(date_patern_regex_h,col)) == True:
# #         col = ''.join(re.findall(date_patern_regex_h,col))
# #         col = col.replace('ago','')
# #         col = int(col.replace('h',''))
# #         time_ = TODAY_TIME-timedelta(hours=col)
# #     elif bool(re.search(date_patern_regex_y,col)) == True:
# #         col = ''.join(re.findall(date_patern_regex_y,col))
# #         col = col.replace('ago','')
# #         col = int(col.replace('y',''))
# #         time_ = TODAY_TIME-timedelta(days=col*365)
# #     return time_
#
# # def get_votes(col):
# #     col = re.findall(regex_pattern,col)
# #     col =  ''.join(col)
# #     col = col.replace('Reply','')
# #     return col
#
# # nltk.download('stopwords')
# # stopwords = nltk.corpus.stopwords.words('english')
# # ps = nltk.PorterStemmer()
# #tokenize,stem, and remove stop words from text
# # def cleanText(text):
# #     text = "".join([word.lower() for word in text if word not in string.punctuation])
# #     tokens = re.split('\W+', text)
# #     text = [ps.stem(word) for word in tokens if word not in stopwords]
# #     return text
# # #word count function
# # def word_count(string):
# #     split = string.split()
# #     count = len(split)
# #     return count
# # #count emojis
# # def count_emojis(string):
# #     em_count = len(re.findall(r'[^\w\s,.]', string))
# #     return em_count
# # #count hashtags
# # def count_hashtags(string):
# #     em_count = len(re.findall(r'[\#]', string))
# #     return em_count
# # #count mentions
# # def count_mentions(string):
# #     em_count = len(re.findall(r'[\@]', string))
#
# # def text_analyzer(df):
# #     #feature creation{Word Count|character count|emoji count|link count}
# #     df['Comment'] = df['Comment'].astype('str')
# #     df['word_count'] = df['Comment'].apply(word_count)
# #     df['character_count'] = [len(each) for each in df['Comment']]
# #     df['link_count'] = df['Comment'].str.count(r'(http)')
# #     df['emoji_count'] = df['Comment'].apply(count_emojis)
# #     df['hashtag_count'] = df['Comment'].apply(count_hashtags)
# #     df['mention_count'] = df['Comment'].apply(count_mentions)
# #     #create other features including word count+sentiment based features
# #     sid = SentimentIntensityAnalyzer()
# #     df['polarity_pos'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['pos'])
# #     df['polarity_neg'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['neg'])
# #     df['polarity_neu'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['neu'])
# #     df['polarity_compound'] = df['Comment'].apply(lambda x: sid.polarity_scores(x)['compound'])
# #     return df
#
# pat_1 = r'(\d{0,}\.\d{0,}K|\d{0,}\d{0,}K)'
# pat_2 = r'\d{0,}'
#
# #######LOG INTO WSJ############
# # driver = webdriver.Chrome('./chromedriver',options=chrome_options)
# # driver.get('https://sso.accounts.dowjones.com/login?state=hKFo2SAyaEVBbUlxVVlqV0w5blRIVnFGYWtNSlpCYmwwaXJUd6FupWxvZ2luo3RpZNkgTkV4djhHWVJKZl9KX0ZVNVVSMTJzR0FXZDI3bC1BaE-jY2lk2SA1aHNzRUFkTXkwbUpUSUNuSk52QzlUWEV3M1ZhN2pmTw&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid%20createTimestamp&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=8b0c1450-b8a6-4f08-88de-8ee4c1e877e5&ui_locales=en-us-x-wsj-215-2&mars=-1&ns=prod%2Faccounts-wsj#!/signin')
# # search = driver.find_element_by_class_name("username")
# # time.sleep(5)
# # search.send_keys("hey@josh.ua")
# # driver.find_element_by_xpath('//*[@id="basic-login"]/div[1]/form/div[2]/div[6]/div[1]/button[2]').click()
# # time.sleep(5)
# # password = driver.find_element_by_id("password-login-password")
# # password.send_keys("livelovelaugh1")
# # time.sleep(5)
# # button =  driver.find_element_by_xpath('//*[@id="password-login"]/div/form/div/div[5]/div[1]/button')
# # button.click()
# # time.sleep(20)
#
# ##############GET ALL pages on WSJ###############################
# # head_links = []
# # header_links = driver.find_elements_by_class_name("style--section-link--2rDVp5ht")
# #
# # for header in header_links:
# #     head_links.append(header.get_attribute("href"))
# # head_links = list(set(head_links))
# # for i in head_links:
# #     print(i)
# # print(f'scraper visting \n {len(head_links)} links ')
# # ##############GET ALL LINKS TO CONVERSATIONS###############################
# # head_links_count = len(head_links)
# # head_links_marker = 0
# # for i in head_links:
# #     nav_section_name = i
# #     driver.get(i)
# #     head_links_marker+=1
# #     links_list = []
# #     elems = driver.find_elements_by_xpath("//a[@href]")
# #     try:
# #         for elem in elems:
# #             if str(elem.get_attribute('href')).startswith("https://www.wsj.com/articles"):
# #                 links_list.append(elem.get_attribute('href'))
# #                 for linky in list(set(links_list)):
# #                     print(nav_section_name,"::::",linky)
# #         print(f"We are scraping a total of {len(list(set(links_list)))} links from {i}")
# #         marker = len(list(set(links_list)))
# #     except:
# #         print(nav_section_name,"::::is broken")
# #         continue
# #     print(f'{(head_links_marker/head_links_count)} % of navigation sections scraped or {head_links_marker} of {head_links_count} links from headers')
#     ####################MAKING METADATA LISTS################################
#     conversation_list = []
#     names_list = []
#     date_list = []
#     all_data_raw_list=[]
#     ############################GRAB EACH LINK AND LET PAGE LOAD##################
#     marker_count = 0
#     #for _ in ['https://www.wsj.com/articles/elon-musk-has-just-one-twitter-board-seat-that-may-be-enough-11649419266?mod=business_minor_pos8']:
#     for _ in list(set(links_list)):
#         marker_count += 1
#         driver.get(_)
#         name_of_article = re.split(r'-\d',_.replace('https://www.wsj.com/articles','').replace('/',''))[0]
#         print(f'going to [ {name_of_article} ]' )
#         link_to_article = _
#         time.sleep(15)
#     ############################SHOWHING CONVERSATION BUTTON CLICK##############################
#         print("looker for conversations")
#         # clicker
#         # try:
#         #     clicker = driver.find_element_by_xpath('//*[@id="comments_sector"]/button')
#         #     print(1)
#         #     clicker.click()
#         # except:
#         #     try:
#         #         clicker = driver.find_element_by_xpath("//button[contains(text(),'conversation_toggle')]")
#         #         print(2)
#         #         clicker.click()
#         #     except:
#         #         try:
#         #             clicker = driver.execute_script("return document.querySelectorAll('[data-spot-im-shadow-host=\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]')[0].shadowRoot.document.querySelector(\'[class=\"conversation-caret\"\')")
#         #             print(3)
#         #             clicker.click()
#         #         except:
#         #             try:
#         #                 clicker = driver.execute_script("return document.querySelector(\'[class=\"conversation-caret\"\')"),
#         #                 print(4)
#         #                 clicker.click()
#         #             except:
#         #                 try:
#         #                     clicker = driver.find_element_by_id("conversation-container").find_elements_by_tag_name("button")[0]
#         #                     print(5)
#         #                     clicker.click()
#         #                 except:
#         #                     print(f"no comments available at this time for {name_of_article}")
#         #                     print(f'{(marker_count/marker)} % of {nav_section_name} scraped or {marker_count} of {marker} links from {nav_section_name}')
#         #                     continue
#         # counter = 0
#         # time.sleep(4)
#         # #######################SHOWING MORE BUTTON BEING CLICKED######################### (30 button clicks should capture most of the data)
#         # for i_button in range(0,30):
#         #     print(f"iterating through range {i_button}")
#         #     try:
#         #         counter_targ = 0
#         #         target = driver.execute_script("return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
#         #         while target.is_displayed():
#         #             target.click()
#         #             time.sleep(10)
#         #             counter +=1
#         #             print(f'button clicked {counter} times')
#         #             target = driver.execute_script("return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
#         #             break
#         #     except:
#         #         continue
#
#         # #########################GETTING EVERY USERNAME DATA########################################
#         # unique_names = []
#         # # names_raw = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\\\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]\')[0].shadowRoot.querySelectorAll(\"[class=\'Button__contentWrapper--11-2-8\'\")")[6:50000]
#         # names_raw = driver.execute_script("return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[class=\'Typography__text--11-2-8 Typography__t4--11-2-8 Typography__l6--11-2-8 src-components-Username-index__wrapper src-components-Username-index__truncated src-components-Username-index__button\'\")")
#         # for i in names_raw:
#         #     unique_names.append(i.get_attribute("textContent"))
#         # unique_names = list(set(unique_names))
#         # names_raw = list(set(names_raw))
#         #
#         # name_of_poster_list = []
#         # post_count_list = []
#         # like_count_list =[]
#         # individual_comment_list = []
#         # time_of_individual_comment_list = []
#         # posted_or_replied_list = []
#         # replied_to_list = []
#         # article_posted_to_list = []
#         # username_list = []
#         # article_links_list = []
#         #
#         # for names in names_raw:
#         #     time.sleep(10)
#         #     print("scraping individual")
#         #     ActionChains(driver).move_to_element(names).click().perform()
#         #     time.sleep(5)
#         #     #if the name is not already in the name of poster list else quit loop and go back to beggining
#         #     if driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-TopMenu-TopMenu__username--lcVW5\"]\')[0].textContent") not in name_of_poster_list:
#         #         name_of_poster = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-TopMenu-TopMenu__username--lcVW5\"]\')[0].textContent")
#         #         user_name_of_poster = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"Typography__text--11-2-13 Typography__t5--11-2-13 Typography__l5--11-2-13 src-components-UserDetails-UserDetails__usernameWrapper--24Mlg\"]\')[0].textContent")
#         #         print(f'new name added to list {name_of_poster} scraping profile')
#         #         post_count = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-Navbar-Navbar__Label--2os_g\"]\')[0].textContent")
#         #         print(post_count)
#         #         like_count = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-DetailText-DetailText__DetailText--mSHwD src-components-DetailText-DetailText__DetailText_Grey--2-p-_ src-components-DetailText-DetailText__nowrap--Hwniw\"\')[0].textContent")
#         #         like_count = like_count.replace('Likes received','')
#         #         if bool(re.search(pat_1,like_count)) == True:
#         #             like_refiged = int(np.ceil(float(like_count.replace('K',''))*1000))
#         #             print(like_refiged)
#         #         elif bool(re.search(pat_2,like_count)) == True:
#         #             like_refiged  = int(np.ceil(float(like_count)))
#         #         ####appending like count and name of posted #####################
#         #         like_count_list.append(like_refiged)
#         #         name_of_poster_list.append(name_of_poster)
#         #         username_list.append(user_name_of_poster)
#         #
#         #         #Posts (4K)
#         #         ####cleaning posts into a numeric interger#####
#         #         post_count = post_count.replace('Posts','').replace('(','').replace(')','')
#         #         if bool(re.search(pat_1,post_count)) == True:
#         #             post_refiged = int(np.ceil(float(post_count.replace('K',''))*1000))
#         #             print(post_refiged)
#         #         elif bool(re.search(pat_2,post_count)) == True:
#         #             post_refiged  = int(np.ceil(float(post_count)))
#         #             print(post_refiged)
#         #         ##appending to post count list
#         #         post_count_list.append(post_refiged)
#         #
#         #             ######scrolling to bottum of page based on post range##############
#         #         scroll_counter = 0
#         #         scroll_height = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__container--\"\')[0].scrollHeight")
#         #         for i in range(0,post_refiged//6):
#         #             scroll_counter +=1
#         #             driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper--\"\')[0].scrollIntoView(false)")
#         #             spinner  = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Spinner__spinner--\"\')[0]")
#         #             try:
#         #                 if spinner.is_displayed() == True:
#         #                     time.sleep(.5)
#         #                     driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper--\"\')[0].scrollIntoView(true)")
#         #                     print("Scrolling done clicker readmores 1")
#         #                     print(f"counter at {round(scroll_counter/(post_refiged//6)*100,2)} % of scrolls complete or {scroll_counter} out")
#         #
#         #                     read_more_buttons = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMoreButton--\"]\')")
#         #                     for button in read_more_buttons:
#         #                         button.click()
#         #                         print("clickin read mores 1")
#         #
#         #                     print("read more 1's done readmores 2")
#         #                     read_more_buttons_2 = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMore--\"]\')")
#         #                     for button in read_more_buttons_2:
#         #                         button.click()
#         #                         print("clickin read mores 2")
#         #
#         #                     # time.sleep(.4)
#         #                     # driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"Modal__focusLockWrapper--11-2-9\"\')[0].window.scrollBy(0,-250)")
#         #                 else:
#         #                     time.sleep(.5)
#         #                     print(f"counter at {round(scroll_counter/(post_count//6)*100,2)} % of scrolls complete")
#         #
#         #                     read_more_buttons = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMoreButton--\"]\')")
#         #                     for button in read_more_buttons:
#         #                         button.click()
#         #                         print("clickin read mores 1 _no loading needed")
#         #
#         #                     print("read more 1's done readmores 2")
#         #                     read_more_buttons_2 = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMore--\"]\')")
#         #                     for button in read_more_buttons_2:
#         #                         button.click()
#         #                         print("clickin read mores 2 no loading needed")
#         #             except:
#         #                 continue
#         #         time.sleep(2)
#         #
#         #         ####################clicking read more buttons for an individuals post################################
#         #         try:
#         #             print("Getting meta replies data for individual")
#         #             replied_to_web = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__Metadata--\"\')")
#         #             for replies in replied_to_web:
#         #                 replied_to_list.append(replies.get_property('textContent'))
#         #                 # print(replied_to_list)
#         #
#         #             print("Getting meta comments data for individual")
#         #             individual_comment_web = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__TextWrapper--\"\')")
#         #             for comment in individual_comment_web:
#         #                 individual_comment_list.append(comment.get_property('textContent'))
#         #                 # print(individual_comment_list)
#         #
#         #             print("Getting the article user replied or posted for individual")
#         #             replied_to_article_web = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Typography__text--\"\')")
#         #             for article in replied_to_article_web:
#         #                 article_posted_to_list.append(article.get_property('textContent'))
#         #
#         #             link_of_articles = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ExtractWrapper--\"\')")
#         #             for link_of_article in link_of_articles:
#         #                 article_links_list.append(link_of_article.get_attribute("href"))
#         #
#         #         except:
#         #             continue
#         #             # print(article_posted_to_list)
#         #         #######wrap in dataframe for individual##################
#         #         zipped_indi = list(itertools.zip_longest(replied_to_list,individual_comment_list,article_posted_to_list,article_links_list))
#         #         print("lists have been zipped")
#         #         indi_df = pd.DataFrame(zipped_indi,columns=['Replied_To','Comment','Article_Name','link'])
#         #         print("clearing metadata lists")
#         #         replied_to_list.clear()
#         #         individual_comment_list.clear()
#         #         article_posted_to_list.clear()
#         #         indi_df['Post_or_Reply'] = np.where(indi_df['Replied_To'].str.findall('Replied to'),"Reply","Post")
#         #         date_patern_regex_all = r'\d{0,}(s|w|y|d|m|h)'
#         #         indi_df['Replied_To_Name'] = indi_df['Replied_To'].str.replace(r'Replied to','').str.replace(r'Posted','').str.replace('ago','').str.replace(date_patern_regex_all,'')
#         #         indi_df['Replied_To_Time'] = indi_df['Replied_To'].apply(lambda x :time_converter(x))
#         #         indi_df['Date Scraped'] = TODAY_DATE
#         #         indi_df['Name'] = name_of_poster
#         #         indi_df['Username'] = user_name_of_poster
#         #         indi_df['Origonal Article Scraped From'] = name_of_article
#         #         # indi_df = indi_df.drop('Replied_To', axis=1, inplace=True)
#         #         indi_df = text_analyzer(indi_df)
#         #
#         #         print(indi_df)
#         #         path = f'/Users/samsavage/Desktop/WSJ New/user_data/{TODAY_DATE}'
#         #         if os.path.exists(path) == False:
#         #             os.mkdir(path)
#         #         indi_df.to_csv(f'{path}/{TODAY_DATE}_{name_of_poster}.csv')
#         #         ###########clost tab and move on##################
#         #         time.sleep(1)
#         #         #go to top of page
#         #         driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper\"\')[0].scrollIntoView(true)")
#         #         #click out of page
#         #         driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Button__circle-icon--\"\')[0].click()")
#         #         print("exiting")
#         #
#         #     else:
#         #         print("name already in the og list skipping name")
#         #         driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"closeButton--\"\')[0].click()")
#         #
#         #     poster_stats = list(itertools.zip_longest(username_list,name_of_poster_list,like_count_list,post_count_list))
#         #     user_stat_df = pd.DataFrame(poster_stats,columns=['Username','Name of Poster','Like Count','Post Count'])
#         #     path2 = f'/Users/samsavage/Desktop/WSJ New/user_data/{TODAY_DATE}'
#         #     if os.path.exists(path2) == False:
#         #         os.mkdir(path2)
#         #     user_stat_df.to_csv(f'{path2}/{TODAY_DATE}_user_data.csv')
