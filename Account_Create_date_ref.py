from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import string
import time
import json
import re
import random
from DBOperations import *


def init(UA):
    opts = Options()
    opts.add_argument("user-agent=" + UA)
    #opts.add_experimental_option("detach", True)

    driver = webdriver.Chrome(chrome_options=opts)

    return driver

def visit(url, driver, timewait=2):
    try:
        driver.get(url)
        time.sleep(timewait + random.uniform(-0.2, 0.2))

    except:
        print("[Error] Cannot browse to " + url)
        driver.close()
        return False

    data = filter(lambda x: x in string.printable, driver.page_source)

    if not data:
        print("[Error] Empty response from " + url)
        driver.close()
        return False

    return True

def visit_for_start_date(url, driver, timewait=2):
    try:
        driver.get(url)
        time.sleep(timewait + random.uniform(-0.2, 0.2))

    except:
        print("[Error] Cannot browse to " + url)
        driver.close()
        return False

    data = filter(lambda x: x in string.printable, driver.page_source)

    if not data:
        print("[Error] Empty response from " + url)
        driver.close()
        return False

    return True

def get_account_creation_date(driver):
    elems = driver.find_element_by_xpath("//div[contains(@class,'k_Q0X NnvRN')]/a/time")  
    print(elems.get_attribute("datetime"))
        






def login(driver, timewait=2):
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
    buttons[0].click()
    time.sleep(timewait + random.uniform(-0.2, 0.2))
    # for b in buttons:
    #	b.click()
    #	time.sleep(timewait)

    uname = driver.find_elements_by_xpath(
        "//*[contains(text(), 'Phone number, username, or email')]/following-sibling::input")
    pwd = driver.find_elements_by_xpath(
        "//*[contains(text(), 'Password')]/following-sibling::input")
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")

    uname[0].send_keys('success.anon1@gmail.com')
    pwd[0].send_keys('Success123')

    time.sleep(timewait + random.uniform(-0.2, 0.2))

    buttons[0].click()
    time.sleep(timewait + random.uniform(-0.2, 0.2))
    # for b in buttons:
    #	b.click()
    #	time.sleep(timewait)


def get_username(driver):
    elems = driver.find_elements_by_xpath("//div[contains(@class, 'e1e1d')]/a")

    for e in elems:
        return e.get_attribute("href").replace("https://www.instagram.com/", "")[:-1]



def get_to_last_post(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    #time.sleep(200)
    
    try:
        elems = driver.find_element_by_xpath("//div[contains(@class,'Nnq7C weEfm')][last()]//div[contains(@class,'v1Nh3 kIKUG  _bz0w')][last()]//a") 
        print(elems.get_attribute("href"))
        visit(elems.get_attribute("href"),driver)
    except Error as error:
        print("Error" +error)
    
    return    
        

def savefile(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


def start_crawl():
    max_page = 20			# Maximum number of crawled pages in the Investor tag
    max_follow = 10		# Maximum number of retrieved follower/following
    uinfo = {}
    timestamp = int(time.time())
    print("starting crawl")
    driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")

    # Login
    try:
        visit("https://instagram.com", driver)
        login(driver)

    except:
        print("Cannot log in")
        driver.quit()
        return

    try:
        visit("https://www.instagram.com/thismomflips/", driver)
        get_to_last_post(driver)
        account_creation_date=get_account_creation_date(driver)


    #     content = extract_account_description(driver)
    #     num_of_followers = extract_num_of_followers(driver)
    #     num_of_following = extract_num_of_following(driver)
    #     full_name = extract_full_name(driver)

    #     print('Full name: {} #followers: {} #following: {}'.format(
    #         full_name, num_of_followers, num_of_following))
    except Error as error:
        print(error)
 


start_crawl()

# URL for getting posts => https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables={"id":"296102572","first":12}

