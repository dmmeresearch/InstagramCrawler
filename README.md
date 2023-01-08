# DMMEScam-Study
This is an anonymous repository with reference code for the paper "#DM-Me: Susceptibility to Direct Messaging-Based Scams" (under review).

## Getting Started

##### Crawler.py 
 The following script runs a python crawler on Instagram. The crawler performs the following steps:
 
  - It opens up a chrome window
 - Logs in on Instagram using credentials in the script
 - Searches posts by hashtags
 - Opens every post and navigates to the author's account
 - Get the information from the author's account page
 - Stores it in a database
 
 
##### Crawl_on_existing.py

The following script gets usernames from the database table and navigates to the account page. If the page is unavailable, it marks the account as dead.

#### If you wish to run the code, please follow the steps given below.

 - Please download chromedriver binary from  https://chromedriver.chromium.org/ and add it to the system path.
 
## Install Dependencies

`pip install -r requirements.txt`