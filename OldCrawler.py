from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import string
import time
import json
import re
import random

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

# Allows for few special characters like " " and "."
def remove_non_alphanumeric_with_few_special(s):
	if not s:
		return s

	return re.sub("[^0-9a-zA-Z .]", "", s)

def visit(url, driver, timewait=5):
	try:
		driver.get(url)
		time.sleep(timewait + random.uniform(-0.5, 0.5))

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

def login(driver, timewait=5):
	buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
	buttons[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))
	#for b in buttons:
	#	b.click()
	#	time.sleep(timewait)

	uname = driver.find_elements_by_xpath("//*[contains(text(), 'Phone number, username, or email')]/following-sibling::input")
	pwd = driver.find_elements_by_xpath("//*[contains(text(), 'Password')]/following-sibling::input")
	buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")

	uname[0].send_keys('success.anon1@gmail.com')
	pwd[0].send_keys('Success123')

	time.sleep(timewait + random.uniform(-0.5, 0.5))

	buttons[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))
	#for b in buttons:
	#	b.click()
	#	time.sleep(timewait)

def goto_chat(driver, timewait=5):
	buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
	buttons[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))

	buttons = driver.find_elements_by_xpath('//*[name()="svg"][@aria-label="New Message"]/ancestor::button')
	buttons[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))

def start_chat(driver, name, timewait=5):
	to = driver.find_elements_by_xpath("//input[contains(@name, 'queryBox')]")
	to[0].send_keys(name)
	time.sleep(timewait + random.uniform(-0.5, 0.5))

	users = driver.find_elements_by_xpath("//div[contains(@class, '-qQT3')]")
	users[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))

	buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
	buttons[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))

def send_text(driver, text, timewait=2):
	txt = driver.find_elements_by_xpath("//div[contains(@class, 'X3a-9')]/div/textarea")
	txt[0].send_keys(text)
	time.sleep(timewait + random.uniform(-0.5, 0.5))

	send = driver.find_elements_by_xpath("//div[contains(@class, 'X3a-9')]/div/following-sibling::div/button")
	send[0].click()
	time.sleep(timewait + random.uniform(-0.5, 0.5))

def poll(driver):
	ret = []

	texts = driver.find_elements_by_xpath("//div[contains(@class, 'VUU41')]/div")

	for t in texts:
		if len(t.find_elements_by_class_name("VdURK")) > 0:
			ttype = "owner"
		elif len(t.find_elements_by_class_name('e9_tN')) > 0:
			ttype = "response"
		else:
			ttype = "time"

		ret.append({"text": t.text, "type": ttype})

	return ret

def start_chat():
	driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")
	
	visit("https://instagram.com", driver)
	login(driver)
	visit("https://www.instagram.com/direct/inbox/", driver)
	goto_chat(driver)
	start_chat(driver, "rogersmithanon2")

	#main loop
	while(True):
		#send_text(driver, "Hello World")
		messages = poll(driver)
		time.sleep(5 + random.uniform(-0.5, 0.5))

		print messages

#start_chat()

def get_username(driver):
	elems = driver.find_elements_by_xpath("//div[contains(@class, 'e1e1d')]/a")

	for e in elems:
		return e.get_attribute("href").replace("https://www.instagram.com/", "")[:-1]

def extract_follows(driver):
	followers = []
	elems = driver.find_elements_by_xpath("//div[contains(@class, 'd7ByH')]/a")

	for e in elems:
		followers.append(e.get_attribute("title"))

	return followers

def extract_account_description(driver):
	return driver.find_element_by_xpath("//div[contains(@class, '-vDIg')]").text

def extract_num_of_followers(driver):
	try:
		element = driver.find_element_by_xpath("(//span[contains(@class, 'g47SY')])[2]")
		if element:
			return element.text
		return ""
	except:
		print('could not retrieve number of followers')
		return ""

def extract_num_of_following(driver):
	try:
		element = driver.find_element_by_xpath("(//span[contains(@class, 'g47SY')])[3]")
		if element:
			return element.text

		return ""
	except:
		print('could not retrieve number of following')
		return ""

def extract_full_name(driver):
	try:
		element = driver.find_element_by_xpath("//h1[contains(@class, 'rhpdm')]")
		if element:
			s = element.text
			s = remove_non_alphanumeric_with_few_special(s)
			return s
		return ""
	except:
		print('count not get full name')
		return ""

def savefile(filename, content):
	with open(filename, 'w') as f:
		f.write(content)

def start_crawl():
	max_page = 10			# Maximum number of crawled pages in the Investor tag
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

	# Get max_page worth of posts from the Investor tage
	try:
		visit('https://www.instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={%22tag_name%22:%22investor%22,%22first%22:' + str(max_page) + '}', driver)
		jsdump = re.findall("{.*}", driver.page_source)[0]
		savefile("dump_" + str(timestamp), jsdump)

		jsparse = json.loads(jsdump)

		# Here I retrive the "Top post." If you want normal posts use the commented one.
		#topposts = jsparse["data"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]
		posts = jsparse["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]
		end_cursor = jsparse["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]

	except:
		print("Cannot fetch Investor category")
		driver.quit()
		return
	print('Going over {} top-posts'.format(len(posts)))

	for p in posts:
		ucode = p["node"]["shortcode"]
		uid = p["node"]["owner"]["id"]
		followers = []
		followings = []
		# Visit the post and get the username of the post's owner
		try:
			visit("https://www.instagram.com/p/" + ucode, driver)
			uname = get_username(driver)

		except:
			print("Cannot get post information")
			driver.quit()
			savefile("parse_" + str(timestamp), json.dumps(uinfo))
			return

		# Visit the user (master) and retrieve the user's info
		try:
			visit("https://www.instagram.com/" + uname, driver)
			content = extract_account_description(driver)
			num_of_followers = extract_num_of_followers(driver)
			num_of_following = extract_num_of_following(driver)
			full_name = extract_full_name(driver)
			print('Full name: {} #followers: {} #following: {}'.format(full_name, num_of_followers, num_of_following))
		except:
			print("Cannot get user information")
			driver.quit()
			savefile("parse_" + str(timestamp), json.dumps(uinfo))
			return

		# Get the followings
		try:
			print('skipping getting followings')
			# visit('https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={%22id%22:%22' + uid + '%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:' + str(max_follow) + '}', driver)
			# jsdump = re.findall("{.*}", driver.page_source)[0]
			# jsparse = json.loads(jsdump)
			#
			# followings = []
			#
			# for f in jsparse["data"]["user"]["edge_follow"]["edges"]:
			# 	followings.append({"id": f["node"]["id"], "uname": f["node"]["username"], "full_name": f["node"]["full_name"]})

		except:
			print("Cannot get following information")
			driver.quit()
			savefile("parse_" + str(timestamp), json.dumps(uinfo))
			return
			
		# Get the followers
		try:
			print('skipping getting followers')
			# visit('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={%22id%22:%22' + uid + '%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:' + str(max_follow) + '}', driver)
			# jsdump = re.findall("{.*}", driver.page_source)[0]
			# jsparse = json.loads(jsdump)
			#
			# followers = []
			#
			# for f in jsparse["data"]["user"]["edge_followed_by"]["edges"]:
			# 	followers.append({"id": f["node"]["id"], "uname": f["node"]["username"], "full_name": f["node"]["full_name"]})
		
		except:
			print("Cannot get follower information")
			driver.quit()
			savefile("parse_" + str(timestamp), json.dumps(uinfo))
			return

		# Save info local
		uinfo[uname] = {"id": uid, "content": content, "full_name": full_name, "num_of_followers": num_of_followers, "num_of_following": num_of_following, "followers": followers, "following": followings}
		savefile("parse_" + str(timestamp), json.dumps(uinfo))

	driver.quit()

start_crawl()

# URL for getting posts => https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables={"id":"296102572","first":12}

























