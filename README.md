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


Once run, this script will create a new directory for the current day and save comment data, per article within seperate csv files.

A Master csv file will also be created within the day-based-directory which is an appended file of all comment data for that day for every article.

Current Meta Data Artificats :

1) Date_Posted : Date posted by the commenter 
2) Comment : Raw comment data
3) Username	: Username of commenter
5) Upvotes	: # of Upvotes for the specific comment
6) date_retrieved	: Date Scraper retreived data
7) article_name	: Name of article scraped
8) link	: Link of Article Scraped
9) sections	: Section link of article scraped

Future Meta Data:

1) Sentiment/Polarity per comment
2) Sentiment/Polarity per article
3) Name Entity Recognication for politications / world leaders / places etc.
4) Comment word length
5) Reply or Original Comment Indicator

Some of the challenges within this project included:

1) WSJ exhibits different web element names/properties for the same web gui buttons seen by user
2) WSJ hides all elements within "ShadowRoot" HTML branches which make any obvoiuse scraping oppurtunities difficult
3) WSJ comments do not have datetime so downstream regex transformations were made to all date related meta data to created a ingestible datetime format
4) WSJ comment upvote contents are variable so regex was required to extract upvote data

This scraper is currently hosted locally and is being reformated in order to work via docker/ec2 instance. 

Eventually this scraper will be turned into an restAPI.

-Please reach out if you found this useful / could make suggestions or forks on future improvements!
