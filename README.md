# wsj_scraper
Do you read the Wallstreet journal like me everyday?
Do you ever comment on an article? Or read within the comments to learn about other subscriber sentiments?
If so this scraper can help you aggregate, at scale, all comment meta data on Wallstreet Journal at any given time! 

Prereqs:

1) A WSJ subscription
2) Chrome 
3) Chromedriver
4) Python / All dependencies listed in the .py file
5) Space on your hardrive to download the data


Once run, this script will create a new directory for the current day within the master directory set by the user, and then save comment data, per article within seperate csv files. The file(s) naming convention is {TODAY_DATE}_article_name.csv

A Master csv file will also be created within the day-based-directory which is an appended file of all comment data for that day for every article.
The master file naming convention is MasterCSV_{TODAY_DATE}.csv

Current Meta Data Artificats :

1) Date_Posted : Date posted by the commenter 
2) Comment : Raw comment data
3) Username	: Username of commenter
5) Upvotes	: # of Upvotes for the specific comment
6) date_retrieved	: Date Scraper retreived data
7) article_name	: Name of article scraped
8) link	: Link of Article Scraped
9) sections	: Section link of article scraped
10) word_count : Count of words in comment 
11) character_count : Count of characters in comment
12) link_count : Count of links in comment
13) emoji_count	: Count of emojis in comment
14) hashtag_count	: Count of hashtags in comment
15) mention_count	: Count of mentions in comment
16) polarity_pos : Positivite Polarity Score provided by nltk 
17) polarity_neg : Negative Polarity Score provided by nltk 
18) polarity_neu : Nuetral Polarity Score provided by nltk 
19) polarity_compound : Compound Polarity Score provided by nltk 

Future Meta Data:

1) Name Entity Recognication for politications / world leaders / places etc.
2) Reply or Original Comment Indicator

Some of the challenges within this project included:

1) WSJ exhibits different web element names/properties for the same web gui buttons seen by user
2) WSJ hides all elements within "ShadowRoot" HTML branches which make any obvoiuse scraping oppurtunities difficult
3) WSJ comments do not have datetime so downstream regex transformations were made to all date related meta data to created a ingestible datetime format
4) WSJ comment upvote contents are variable so regex was required to extract upvote data

This scraper is currently hosted locally and is being reformated in order to work via docker/ec2 instance. 

Eventually this scraper will be turned into an restAPI.

-Please reach out if you found this useful / could make suggestions or forks on future improvements!
