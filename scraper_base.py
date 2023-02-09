#!/usr/bin/env python3.9
import enum
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from selenium import webdriver
import pandas as pd
import nltk
import ssl
import random
import time
import itertools
import os
import datetime as dt
from selenium.webdriver.chrome.options import Options
from datetime import timedelta
import warnings
from dotenv import load_dotenv
import regex as re
from scraper_utils import log
import sys
import inspect


class ScraperState(enum.Enum):
    perform_login = 1
    get_nav_links = 2
    get_section_sublinks = 3
    process_page = 4
    # create_master_csv = 5
    done = 200


class Scraper(object):
    state = ScraperState.perform_login
    continue_from_state = None
    header_links = []
    header_links_index = 0
    section_sublink_index = 0
    article_csv_save_count = 0
    current_section_sublinks = []
    # current_section_sublinks = ['https://www.wsj.com/articles/elon-musk-has-just-one-twitter-board-seat-that-may-be-enough-11649419266?mod=business_minor_pos8']
    #current_section_sublinks = ['https://www.wsj.com/articles/who-can-afford-napa-valley-11650647489?mod=wsjhp_columnists_pos1', 'https://www.wsj.com/articles/elon-musk-has-just-one-twitter-board-seat-that-may-be-enough-11649419266?mod=business_minor_pos8']
    driver = None
    time_today = None
    date_w_time_today = None
    # articles_csv_path = None
    # master_csv_path = None
    s3 = None
    bucket_name = None
    nltk_stopwords = None
    nltk_porter_stemmer = None
    current_article_link = None
    num_times_article_retry = 0
    max_article_retries = 1

    def __init__(self):
        random.seed(53)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download('punkt')
        nltk.download('vader_lexicon')
        load_dotenv()
        if os.getenv("should_upload_to_s3", 'False').lower() in ('true', '1', 'yes', 'y', 't'):
            import boto3
            self.s3 = boto3.client('s3')
            self.bucket = os.getenv('s3_bucket_name')

        log("setting up CSV output paths")
        self.time_today = dt.datetime.now()
        self.date_w_time_today = self.time_today.strftime("%m-%d-%Y_%H-%M-%S")
        # self.articles_csv_path = f"{os.getenv('articles_csv_output_path')}/{self.date_w_time_today}"
        # if not os.path.exists(self.articles_csv_path):
        #     os.mkdir( self.articles_csv_path)

        # self.master_csv_path = f"{os.getenv('master_csv_output_path')}/{self.date_w_time_today}"
        # if not os.path.exists(self.master_csv_path):
        #     os.mkdir(self.master_csv_path)

        # log(f"Local path to article CSVs is {self.articles_csv_path}")
        # log(f"Local path to master CSV is {self.master_csv_path}")
        nltk.download('stopwords')
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.porter_stemmer = nltk.PorterStemmer()

        self._create_new_chromedriver()

    def _create_new_chromedriver(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

        # chromedriver setup
        # for list of possible options see https://peter.sh/experiments/chromium-command-line-switches/
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")  # allows more usage of computer resources
        chrome_options.add_argument("--disable-dev-shm-usage")  # allows offloading in memory data to disk if necessary
        if os.getenv("should_run_headless", 'False').lower() in ('true', '1', 'yes', 'y', 't'):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--enable-automation")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"')
            log("running headless")
        else:
            log("running with GUI")

        self.driver = webdriver.Chrome(os.getenv('chromedriver_path'), options=chrome_options)
        self.driver.set_page_load_timeout(30)  # if a page takes longer than 30s to load, something went wrong

    # word count function
    def _word_count(self, text):
        return len(text.split())

    # count emojis
    def _count_emojis(self, text):
        return len(re.findall(r'[^\w\s,.]', text))

    # count hashtags
    def _count_hashtags(self, text):
        return len(re.findall(r'[\#]', text))

    # count mentions
    def _count_mentions(self, text):
        return len(re.findall(r'[\@]', text))

    def time_converter(self, col):
        date_patern_regex = r'(\d{2}|\d{1})\s(March|April|May|June|July|August|September|October|November|December|January|February),\s\d{4}'
        date_patern_regex_2 = r'\d{1,2}\sM'
        date_patern_regex_3 = r'\d{1,2}\sH'
        date_patern_regex_4 = r'\d{1,2}\sS'
        date_patern_regex_w = r'\d{0,}w\sago'
        date_patern_regex_d = r'\d{0,}d\sago'
        date_patern_regex_h = r'\d{0,}h\sago'
        date_patern_regex_y = r'\d{0,}y\sago'
        date_patern_regex_s = r'\d{0,}s\sago'
        # date_patern_regex_all = r'\d{0,}(s|w|y|d|m|h)'
        time_ = ''
        if col is None:
            time_ = self.time_today
        elif bool(re.search(date_patern_regex_2, col)):
            match = ''.join(re.findall(date_patern_regex_2, col))
            match = int(match.replace('M', ''))
            time_ = self.time_today - timedelta(minutes=match)
        elif bool(re.search(date_patern_regex_4, col)):
            match = ''.join(re.findall(date_patern_regex_4, col))
            match = int(match.replace('S', ''))
            time_ = self.time_today - timedelta(seconds=match)
        elif bool(re.search(date_patern_regex_3, col)):
            match = ''.join(re.findall(date_patern_regex_3, col))
            match = int(match.replace('H', ''))
            time_ = self.time_today - timedelta(hours=match)
        elif bool(re.search(date_patern_regex, col)):
            time_ = pd.to_datetime(re.search(date_patern_regex, col)[0])
        elif 'Just Now' in col:
            time_ = self.time_today
        elif '1 day ago' in col:
            col = int(col.replace('1 day ago', '24'))
            time_ = self.time_today - timedelta(hours=col)
        elif '2 days ago' in col:
            col = int(col.replace('2 days ago', '48'))
            time_ = self.time_today - timedelta(hours=col)
        elif '3 days ago' in col:
            col = int(col.replace('3 days ago', '72'))
            time_ = self.time_today - timedelta(hours=col)
        elif '4 days ago' in col:
            col = int(col.replace('4 days ago', '96'))
            time_ = self.time_today - timedelta(hours=col)
        elif '5 days ago' in col:
            col = int(col.replace('5 days ago', '120'))
            time_ = self.time_today - timedelta(hours=col)
        elif '6 days ago' in col:
            col = int(col.replace('6 days ago', '144'))
            time_ = self.time_today - timedelta(hours=col)
        elif '7 days ago' in col:
            col = int(col.replace('7 days ago', '168'))
            time_ = self.time_today - timedelta(hours=col)
        elif bool(re.search(date_patern_regex_w, col)):
            col = ''.join(re.findall(date_patern_regex_w, col))
            col = col.replace('ago', '')
            col = int(col.replace('w', ''))
            time_ = self.time_today - timedelta(weeks=col)
        elif bool(re.search(date_patern_regex_s, col)):
            col = ''.join(re.findall(date_patern_regex_s, col))
            col = col.replace('ago', '')
            col = int(col.replace('s', ''))
            time_ = self.time_today - timedelta(seconds=col)
        elif bool(re.search(date_patern_regex_d, col)):
            col = ''.join(re.findall(date_patern_regex_d, col))
            col = col.replace('ago', '')
            col = int(col.replace('d', ''))
            time_ = self.time_today - timedelta(days=col)
        elif bool(re.search(date_patern_regex_h, col)):
            col = ''.join(re.findall(date_patern_regex_h, col))
            col = col.replace('ago', '')
            col = int(col.replace('h', ''))
            time_ = self.time_today - timedelta(hours=col)
        elif bool(re.search(date_patern_regex_y, col)):
            col = ''.join(re.findall(date_patern_regex_y, col))
            col = col.replace('ago', '')
            col = int(col.replace('y', ''))
            time_ = self.time_today - timedelta(days=col * 365)
        return time_

    def _analyze_comment(self, dataframe):
        # feature creation{Word Count|character count|emoji count|link count}
        dataframe['Comment'] = dataframe['Comment'].astype('str')
        dataframe['word_count'] = dataframe['Comment'].apply(self._word_count)
        dataframe['character_count'] = [len(comment) for comment in dataframe['Comment']]
        dataframe['link_count'] = dataframe['Comment'].str.count(r'(http)')
        dataframe['emoji_count'] = dataframe['Comment'].apply(self._count_emojis)
        dataframe['hashtag_count'] = dataframe['Comment'].apply(self._count_hashtags)
        dataframe['mention_count'] = dataframe['Comment'].apply(self._count_mentions)
        # create other features including word count+sentiment based features
        sid = SentimentIntensityAnalyzer()
        dataframe['polarity_pos'] = dataframe['Comment'].apply(lambda x: sid.polarity_scores(x)['pos'])
        dataframe['polarity_neg'] = dataframe['Comment'].apply(lambda x: sid.polarity_scores(x)['neg'])
        dataframe['polarity_neu'] = dataframe['Comment'].apply(lambda x: sid.polarity_scores(x)['neu'])
        dataframe['polarity_compound'] = dataframe['Comment'].apply(lambda x: sid.polarity_scores(x)['compound'])
        return dataframe

    def _get_votes(self, col):
        regex_pattern = r'Reply\d{0,}'
        col = re.findall(regex_pattern, col)
        col = ''.join(col)
        col = col.replace('Reply', '')
        return col

    # tokenize,stem, and remove stop words from text
    def _cleanText(self, text, ps, stopwords):
        text = "".join([word.lower() for word in text if word not in string.punctuation])
        tokens = re.split('\W+', text)
        text = [ps.stem(word) for word in tokens if word not in stopwords]
        return text

    def _save_article_to_csv(self, all_raw_data, raw_dates, raw_names, raw_texts):
        log("Packaging data")
        start = time.perf_counter()
        conversation_list = [text.get_attribute('innerHTML') for text in raw_texts]
        names_list = [name.get_property('textContent') for name in raw_names]
        date_list = [str(date.get_property('textContent')).replace('hours ago', 'H').replace('hour ago', 'H').replace('minutes ago', 'M').replace('seconds ago', 'S').replace('minute ago', 'M').replace('Just Now', '1 M') for date in raw_dates]
        all_data_raw_list = [str(datum.get_property('textContent')) for datum in all_raw_data]
        end = time.perf_counter()
        log(f"Time to create lists {end - start}")
        zipped = list(itertools.zip_longest(date_list, conversation_list, names_list, all_data_raw_list))
        dataframe = pd.DataFrame(zipped, columns=['Date_Posted', 'Comment', 'Username', 'Upvotes'])
        dataframe['Upvotes'] = dataframe['Upvotes'].apply(lambda x: self._get_votes(x))
        dataframe['Date_Posted'] = dataframe['Date_Posted'].apply(lambda x: self._time_converter(x))
        dataframe['date_retrieved'] = self.time_today
        article_name = re.split(r'-\d', self.current_article_link.replace('https://www.wsj.com/articles', '').replace('/', ''))[0]
        dataframe['article_name'] = article_name
        dataframe['link'] = self.current_article_link
        # if len(self.header_links) > 0:
        #     dataframe['sections'] = self.header_links[self.header_links_index]
        # else:
        #     dataframe['sections'] = 'test mode'
        dataframe['sections'] = self.header_links[self.header_links_index]
        dataframe = self._analyze_comment(dataframe)
        log(f"text metadata has been added with columns {dataframe.columns}")
        filename = f'{self.articles_csv_path}/{self.date_w_time_today}_{article_name}.csv'

        # creates csv locally
        dataframe.to_csv(filename)

        # s3 uploading
        if os.getenv("should_upload_to_s3", 'False').lower() in ('true', '1', 'yes', 'y', 't'):
            self.s3.upload_file(Filename=filename, Bucket=self.bucket, Key=filename)

    # def _create_master_csv(self):
    #     file_cats = []
    #     directory_contents = os.listdir(self.articles_csv_path)
    #     log(f"Concatenating {len(directory_contents)} files for master CSV")
    #     for file in directory_contents:
    #         try:
    #             df = pd.read_csv(f'{self.articles_csv_path}/{file}')
    #             file_cats.append(df)
    #         except Exception as e:
    #             log(e)
    #             continue
    #     master_df = pd.concat(file_cats)
    #     master_df = master_df.drop_duplicates()
    #     master_filename = f"{self.master_csv_path}/MasterCSV_{self.date_w_time_today}.csv"
    #     master_df.to_csv(master_filename)
    #     if os.getenv("should_upload_to_s3", 'False').lower() in ('true', '1', 'yes', 'y', 't'):
    #         self.s3.upload_file(Filename=master_filename, Bucket=self.bucket, Key=master_filename)
    #     log("Master CSV saved!")
    #     self.state = ScraperState.done

    def _handle_global_error(self, error):
        error_str = str(error)
        log(f"script error: {error_str}")
        if re.search('crash', error_str, re.IGNORECASE):
            log("attempting recovery from page crash")
            self._create_new_chromedriver()
            self._login()
        elif re.search('invalid session id', error_str, re.IGNORECASE):
            log("Attempting recover from invalid session id")
            self._create_new_chromedriver()
            self._login()
        elif re.search('list index out of range', error_str, re.IGNORECASE):
            log("quitting due to login issue like password failed")
            sys.exit()
        elif re.search('maximum recursion depth exceeded', error_str, re.IGNORECASE):
            log(f"max recursion depth exceeded with depth {len(inspect.stack(0))}/{sys.getrecursionlimit()}")
            sys.exit()
        elif re.search('timed out', error_str, re.IGNORECASE):
            log(f"page timed out, logging in and continuing")
            self._login()
        elif re.search('Connection aborted', error_str, re.IGNORECASE):
            log('connection aborted: shutting down now to not spam network and cool off')
            sys.exit()
        elif re.search('Max retries exceeded', error_str, re.IGNORECASE):
            log('Max retries exceed: shutting down now to not spam network and cool off')
            sys.exit()

    def run(self):
        try:
            while self.state != ScraperState.done:
                if self.state == ScraperState.perform_login:
                    self._login()
                elif self.state == ScraperState.get_nav_links:
                    self._get_nav_links()
                elif self.state == ScraperState.get_section_sublinks:
                    self._get_nav_page_sub_links()
                elif self.state == ScraperState.process_page:
                    self._process_page()
                # elif self.state == ScraperState.create_master_csv:
                #     self._create_master_csv()
        except Exception as e:
            self._handle_global_error(e)
            time.sleep(10)
            self.run()

