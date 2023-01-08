from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import string
import time as time_
import json
from datetime import *
import re
import random
from DBOperations import *


def init(UA):
    opts = Options()
    opts.add_argument("user-agent=" + UA)

    driver = webdriver.Chrome(chrome_options=opts)

    return driver

def remove_non_numeric(s):
    if not s:
        return s

    return re.sub("[^0-9]", "", s)

def remove_non_alphabetic(s):

    if not s:
        return s

    return re.sub("[^a-zA-Z]", "", s)

def remove_non_alphanumeric_with_few_special(s):
    if not s:
        return s

    return re.sub("[^0-9a-zA-Z .]", "", s)

def remove_chars_to_sanitise(s):
    '''
    Sanitise input, get rid of malicious characters and words
    '''
    if not s:
        return s
    s=re.sub("[,|&*()_>~<+:\";'?-]"," ",s)
    # word_list=['where','insert','drop','select','update','INSERT','WHERE','DROP','SELECT','UPDATE']
    # for words in word_list:
    #     s=re.sub(rf'\s{{0,}}{words}\s{{1,}}',' ',s)
    return s


def visit(url, driver, time_wait=5):
    try:
        driver.get(url)
        time_.sleep(time_wait + random.uniform(-0.5, 0.5))

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

def login(driver, time_wait=2):
    
    # Please uncomment the next 3 lines when running Crawler.py. If running Crawl_on_exsting.py, keep them commented.
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
    buttons[0].click()
    time_.sleep(time_wait + random.uniform(-0.7, 0.17))


    uname = driver.find_elements_by_xpath(
        "//*[contains(text(), 'Phone number, username, or email')]/following-sibling::input")
    pwd = driver.find_elements_by_xpath(
        "//*[contains(text(), 'Password')]/following-sibling::input")
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")



    uname[0].send_keys('success.anon4@gmail.com')
    pwd[0].send_keys('Success@123')
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))
    buttons[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))

    # for b in buttons:
    #	b.click()
    #	time_.sleep(time_wait)


def goto_chat(driver, time_wait=5):
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
    buttons[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))

    buttons = driver.find_elements_by_xpath(
        '//*[name()="svg"][@aria-label="New Message"]/ancestor::button')
    buttons[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))


def start_chat(driver, name, time_wait=5):
    to = driver.find_elements_by_xpath("//input[contains(@name, 'queryBox')]")
    to[0].send_keys(name)
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))

    users = driver.find_elements_by_xpath("//div[contains(@class, '-qQT3')]")
    users[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))

    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
    buttons[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))


def send_text(driver, text, time_wait=2):
    txt = driver.find_elements_by_xpath(
        "//div[contains(@class, 'X3a-9')]/div/textarea")
    txt[0].send_keys(text)
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))

    send = driver.find_elements_by_xpath(
        "//div[contains(@class, 'X3a-9')]/div/following-sibling::div/button")
    send[0].click()
    time_.sleep(time_wait + random.uniform(-0.5, 0.5))


def poll(driver):
    ret = []

    texts = driver.find_elements_by_xpath(
        "//div[contains(@class, 'VUU41')]/div")

    for t in texts:
        if len(t.find_elements_by_class_name("VdURK")) > 0:
            ttype = "owner"
        elif len(t.find_elements_by_class_name('e9_tN')) > 0:
            ttype = "response"
        else:
            ttype = "time_"

        ret.append({"text": t.text, "type": ttype})

    return ret


def get_to_last_post(driver):

    try:
        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time_.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Error as error:
        print(error)
    #time_.sleep(200)

    try:
        elems = driver.find_element_by_xpath("//div[contains(@class,'Nnq7C weEfm')][last()]//div[contains(@class,'v1Nh3 kIKUG  _bz0w')][last()]//a")
        visit(elems.get_attribute("href"),driver)

    except Error as error:
        print("Error" +error)

    return

def get_username(driver):
    elems = driver.find_elements_by_xpath("//div[contains(@class, 'e1e1d')]/a")

    for e in elems:
        return e.get_attribute("href").replace("https://www.instagram.com/", "")[:-1]

def get_account_creation_date(driver):
    elems = driver.find_element_by_xpath("//div[contains(@class,'k_Q0X I0_K8  NnvRN')]/a/time")
    try:
        d=datetime.strptime(elems.get_attribute("datetime"),"%Y-%m-%dT%H:%M:%S.%fZ")
    except Error as error:
        print(error)

    return str(d)

def extract_number_of_posts(driver):

    try:
        element = driver.find_element_by_xpath("(//span[contains(@class, 'g47SY')])[1]")
    except:
        try:
            element=driver.find_element_by_xpath("(//div[contains(@class, 'error-container -cx-PRIVATE-ErrorPage__errorContainer -cx-PRIVATE-ErrorPage__errorContainer__')])/h2")
        except:
            try:
                element = driver.find_element_by_xpath("(//h2[contains(@class,'MCXLF')])")
            except:
                element = driver.find_element_by_xpath("(//h2[contains(@class,'_7UhW9      x-6xq    qyrsm KV-D4          uL8Hv     l4b0S    ')])")


    if element.text != 'Sorry, this page isn\'t available.' and element.text != 'Error':
        return element.text
    elif 'Sorry, this page isn\'t available.' in element.text :
        return "error"
    else:
        return "blocked error"

def extract_follows(driver):
    followers = []
    elems = driver.find_elements_by_xpath("//div[contains(@class, 'd7ByH')]/a")

    for e in elems:
        followers.append(e.get_attribute("title"))

    return followers


def extract_account_description(driver):
    try:
        element=driver.find_element_by_xpath("//div[contains(@class, '-vDIg')]")
        if element:
            return element.text
        return ""
    except:
        print('could not retrieve account info')
        return ""



def extract_num_of_followers(driver):
    try:
        element = driver.find_element_by_xpath(
            "(//span[contains(@class, 'g47SY')])[2]")
        if element:
            return element.text
        return ""
    except:
        print('could not retrieve number of followers')
        return ""


def extract_num_of_following(driver):
    try:
        element = driver.find_element_by_xpath(
            "(//span[contains(@class, 'g47SY')])[3]")
        if element:
            return element.text

        return ""
    except:
        print('could not retrieve number of following')
        return ""


def extract_full_name(driver):
    try:
        element = driver.find_element_by_xpath(
            "//h1[contains(@class, 'rhpdm')]")
        if element:
            s = element.text
            s = remove_non_alphanumeric_with_few_special(s)
            return s
        return ""
    except:
        print('Cannot not get full name')
        return ""


def savefile(filename, content):
    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

def savefile_old(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def StringToTimedelta(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: float(val) for key, val in m.groupdict().items()}

def start_crawl():
    max_page = 40	# Maximum number of crawled pages in the Investor tag
    max_follow = 15		# Maximum number of retrieved follower/following
    uinfo = {}
    user_in_json=[]
    time_stamp = int(time_.time())
    username_list=db_get_list_of_username() #get username already present in db
    #print(username_list)
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

    # Get max_page worth of posts from the Investor tage
    try:
        visit(
            'https://www.instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={%22tag_name%22:%22marketingcoach%22,%22first%22:' + str(max_page) + '}', driver)

        jsdump = re.findall("{.*}", driver.page_source)[0]
        savefile("dump_" + str(time_stamp), jsdump)
        jsparse = json.loads(jsdump)
        posts = jsparse["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]

        # Here I retrive the "Top post." If you want normal posts use the commented one.
        #topposts = jsparse["data"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]

        # end_cursor = jsparse["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]

    except Exception as error:
        print(error)
        print("Cannot fetch DMMEFORDETAILS category")
        driver.quit()
        return
    print('Going over {} top-posts'.format(len(posts)))

    for p in posts:
        check=""
        ucode = p["node"]["shortcode"]
        uid = p["node"]["owner"]["id"]
        followers=[]
        followings=[]
        num_of_followers=''
        num_of_following=''
        num_of_posts=''
        try:
            uname_caption = p["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            uname_caption=remove_chars_to_sanitise(uname_caption)
            Post_Comments = p["node"]["edge_media_to_comment"]["count"]
            Post_Likes = p["node"]["edge_liked_by"]["count"]

        except:
            uname_caption="Can't get post info"

        try:
            visit("https://www.instagram.com/p/" + ucode, driver)
            uname = get_username(driver)
            if uname not in username_list and uname not in user_in_json:
                driver.get_screenshot_as_file("../../Screenshot_Post/"+uname+".png")
        except:
            uname="No Post Information"


        if uname != "No Post Information" and uname not in username_list:
            try:
                visit("https://www.instagram.com/" + uname, driver)
                driver.get_screenshot_as_file("../../Screenshots/"+uname+".png")
                num_of_posts = extract_number_of_posts(driver)
                #print(num_of_posts)
                content = extract_account_description(driver)
                if content:
                    content=remove_chars_to_sanitise(content)
                else:
                    content = ""
                #print(content)
                if int(num_of_posts) < 500 :
                    num_of_followers = extract_num_of_followers(driver)
                    num_of_following = extract_num_of_following(driver)
                    full_name = extract_full_name(driver)
                    if uname not in username_list and uname not in user_in_json:
                        get_to_last_post(driver)
                        # print('Full name: {} Number Of Posts:{} #followers: {} #following: {}'.format(full_name,num_of_posts, num_of_followers, num_of_following))
                        account_creation_date=get_account_creation_date(driver)
                    else:
                        account_creation_date=db_get_account_creation_date(uname)
                    print('Full name: {} Account Created:{} Number Of Posts:{} #followers: {} #following: {}'.format(full_name,account_creation_date,num_of_posts, num_of_followers, num_of_following))
                else:
                    continue
            except Exception as error:
                print("i am here because of "+str(error))
                check = "Cannot get user information"

        if uname != "No Post Information" and check != "Cannot get user information" and uname not in username_list:

            user_in_json.append(uname)
            uinfo[uname] = {"id": uid, "content": content, "full_name": full_name, "num_of_followers": num_of_followers,"num_of_posts": num_of_posts,"Post_Likes":Post_Likes,"Post_Comments":Post_Comments,
                        "num_of_following": num_of_following, "followers": followers, "following": followings,"account_creation_date":account_creation_date,"Post_Caption":uname_caption}

            savefile_old("parse_" + str(time_stamp), json.dumps(uinfo))
        else:
            check=""

    driver.quit()
    try:
        db_update_new_accounnts("parse_" + str(time_stamp))
    except:
        print("File is not present and could not be added to db")



#start_crawl()

# URL for getting posts => https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables={"id":"296102572","first":12}

def start_crawl_on_existing():		# Maximum number of retrieved follower/following
    uinfo = {}
    time_stamp = int(time_.time())
    username_list=db_get_list_of_username() #get username already present in db
    print("starting crawl on existing accounts")
    driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")
    # Login
    try:
        visit("https://instagram.com", driver)
        login(driver)

    except:
        print("Cannot log in")
        driver.quit()
        return

    for uname in username_list[180:194]:
        print(uname)
        followers = []
        followings = []
        # Visit the post and get the username of the post's owner
        # Visit the user (master) and retrieve the user's info
        try:
            visit("https://www.instagram.com/" + uname, driver)
            get_to_last_post(driver)
            account_creation_date=get_account_creation_date(driver)
            print(account_creation_date)
                # else:
                #     account_creation_date=db_get_account_creation_date(uname)
                # print('Full name: {} Account Created:{} Number Of Posts:{} #followers: {} #following: {}'.format(
                #     full_name,account_creation_date,num_of_posts, num_of_followers, num_of_following))
        except:
            # check = "Cannot get user information"
            print("Cannot get user information")
            uname=""
            account_creation_date=""
            # if uname != "No Post Information" and check != "Cannot get user information":

        uinfo[uname] = {"account_creation_date": account_creation_date}
        savefile_old("parse_" + str(time_stamp), json.dumps(uinfo))
    driver.quit()
    db_fix_account_creation_date("parse_" + str(time_stamp))



def main():

       #start_crawl_on_existing()
    start_crawl()


if __name__== "__main__":
    main()
