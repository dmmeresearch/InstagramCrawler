from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from collections import defaultdict
import string
import time as time_
import json
from datetime import *
import re
import random
from DBOperations import *
from Debug import *
import locale
import os
import sys
from Debug import *
import shutil
import pandas as pd



def crawl_for_live():


    uinfo = {}
    timestamp = int(time_.time())
    username_live_list=db_get_uname_alive_check() #get username already present in db

    # username_list = []
    # for row in username_live_list:
    #     username_list.append(row[0])
    # print(len(username_list))
    # print(username_list.index('jerryceevibes'))
    # exit(0)


    # with open('All_Usernames.txt', 'w') as f:
    #     for item in username_live_list:
    #         f.write("{}\n".format(item))
    # exit(0)

    print("starting crawl on existing accounts for checking if active")
    # driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")
    #driver = init("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")
    driver = init("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    # Login
    try:
        visit("https://instagram.com", driver)
        login(driver)

    except:
        print("Cannot log in")
        driver.quit()
        return

    recent_crawl_date=db_get_current_timeStamp()
    recent_crawl_date = recent_crawl_date.strftime('%Y-%m-%d %H:%M:%S')
    print(recent_crawl_date)
    died_on_date=""
    for row in username_live_list[250:]:

        uname=row[0]
        p=""
        is_alive=row[1]
        creation_date=row[2]
        num_of_posts=""
        num_followers=""
        followers = []
        followings = []
        if is_alive == 1:
            try:
                visit("https://www.instagram.com/" + uname, driver)
                p=extract_number_of_posts(driver)
            except:
                print("Cannot get user information for this username "+str(uname))
                continue
            if p == "error":
                print(uname)
                died_on_date=recent_crawl_date
                is_alive=0
            elif p == "blocked error":
                print("Instagram temporarily blocked our crawling. Use another account to login.")
                break
            elif p[0].isdigit():
                died_on_date=""
                num_followers= extract_num_of_followers(driver)
                num_of_posts = p
            uinfo[uname] = {"died_on_date":died_on_date,"Account_Creation_date":creation_date,"is_alive":is_alive,"recent_crawl_date":recent_crawl_date,'num_of_posts':num_of_posts,'num_followers':num_followers}
            savefile("parse_" + str(timestamp), json.dumps(uinfo))

    driver.quit()

    db_update_timestamp("parse_" + str(timestamp))
    crawl_calculate_lifetime()
    crawl_update_current_lifetime_version2()

def finding_accounts_with_small_lifelime():

    usernames_with_life_attributes = db_get_uname_with_small_lifetime()
    for row in usernames_with_life_attributes[2500:]:
        if row[1] is not None:
            print(row)



def crawl_suspicious_followers():
    '''
    get the followers information in a file of the suspicious followers in the db
    '''
    uinfo = {}
    file_already_list=[]
    timestamp = int(time_.time())
    username_followers_id_sus_list=db_get_uname_followers_id_check()#get username already present in db
    uname_filename_list=db_get_filenames()
    for filenames in uname_filename_list:
        uname=filenames[1].rsplit('_',1)[0]
        file_already_list.append(uname)

    print("starting crawl on suspicios account's followers")
    driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")
    # Login
    try:
        visit("https://instagram.com", driver)
        login(driver)

    except:
        print("Cannot log in")
        driver.quit()
        return

    for row in username_followers_id_sus_list:
        uname=row[0]
        if uname not in file_already_list:
            num_followers=row[1]
            ucode=row[2]
            is_suspicious=row[3]
            print(uname)
            print(num_followers)
            if num_followers[-1] == 'k':
                num_followers=num_followers[:-1]
                num_followers=float(num_followers) * 1000
                num_followers=str(int(num_followers))
            user_followers_file = uname+"_" + str(timestamp)
            followers = []
            followings = []
            # Current_Date_Formatted = datetime.datetime.today().strftime ('%d%m%Y')
            if is_suspicious == 1:
                locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
                num_followers=locale.atoi(num_followers)
                if num_followers < 9999:
                    length = num_followers//50 # because query gets only 50 followers
                    print("length "+ str(length) )
                    followers_left = int(num_followers) % 50
                    print(type(followers_left))
                    print("left "+ str(followers_left))
                    try:
                        visit("https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:50}",driver)
                        jsdump = re.findall("{.*}", driver.page_source)[0]
                        savefile("dump_"+str(timestamp), jsdump)
                        jsparse = json.loads(jsdump)
                        try:
                            posts = jsparse["data"]["user"]["edge_followed_by"]["edges"]
                            end_cursor = jsparse["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                            main_dict = traverse_query_json(posts,user_followers_file,{})
                        except:
                            print(uname+" cannot be extracted")
                            continue

                        for i in range(1,length):
                            visit("https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:50,%22after%22:%22"+end_cursor+"%22}",driver)
                            jsdump = re.findall("{.*}", driver.page_source)[0]
                            savefile("dump_"+str(timestamp), jsdump)
                            jsparse = json.loads(jsdump)
                            try:
                                posts = jsparse["data"]["user"]["edge_followed_by"]["edges"]
                                end_cursor = jsparse["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                                print(len(posts))
                                print(end_cursor)
                                main_dict=traverse_query_json(posts,user_followers_file,main_dict)
                            except:
                                print(uname+" cannot be extracted")
                                break


                        if length != 0:
                            visit("https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:"+str(followers_left)+",%22after%22:%22"+end_cursor+"%22}",driver)
                            jsdump = re.findall("{.*}", driver.page_source)[0]
                            savefile("dump_"+str(timestamp), jsdump)
                            jsparse = json.loads(jsdump)
                            try:
                                posts = jsparse["data"]["user"]["edge_followed_by"]["edges"]
                                main_dict=traverse_query_json(posts,user_followers_file,main_dict)
                            except:
                                print(uname+" cannot be extracted")
                                break
                    except:
                        print("Cannot get Followers information")
                    savefile("Suspicious_Followers/"+user_followers_file,json.dumps(main_dict))
        else:
            print("File already present")
            continue

    driver.quit()


def crawl_suspicious_following_followers():
    '''
    Crawling followings of most suspicious followers
    '''
    uinfo = {}
    file_already_list=[]
    timestamp = int(time_.time())
    # mostCommonlist={'corevalueone':'33435617917','izeeshanaslam':'7231706490', 'alex_carlin_':'36776251742', 'moneybillionaires':'32807558521', 'businessgrinddaily':'36660498932', 'bit.coinbliz':'31222226641', 'incomethirsty':'35889071694', 'incomepython':'36345782994', 'theoneofive':'34630789098', 'begininvesting':'34128598391', 'billionaire_entrepreneurr':'31244008600', 'flynancial':'12160570243', 'thedononwallsreet':'36834735439', 'primetime_trading':'38044736051','_thetradershub_':'37345915280'}
    mostCommonlist={'_thetradershub_':'37345915280'}
    print("starting crawl on suspicious account's followers following")
    driver = init("Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36")
    # Login
    try:
        visit("https://instagram.com", driver)
        login(driver)

    except:
        print("Cannot log in")
        driver.quit()
        return

    for uname in mostCommonlist:
        print(uname)
        user_followers_file = uname+"_" + str(timestamp)
        ucode=mostCommonlist[uname]
        try:
            visit("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:50}",driver)
            jsdump = re.findall("{.*}", driver.page_source)[0]
            savefile("dump_"+str(timestamp), jsdump)
            jsparse = json.loads(jsdump)
            num_followings=jsparse["data"]["user"]["edge_follow"]["count"]
            length = num_followings//50 # because query gets only 50 followers
            print("length "+ str(length) )
            followers_left = int(num_followings) % 50
            print(type(followers_left))
            print("left "+ str(followers_left))
            try:
                posts = jsparse["data"]["user"]["edge_follow"]["edges"]
                end_cursor = jsparse["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
                main_dict = traverse_query_json(posts,user_followers_file,{})
            except:
                print(uname+" cannot be extracted")
                continue

            for i in range(1,length):
                visit("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:50,%22after%22:%22"+end_cursor+"%22}",driver)
                jsdump = re.findall("{.*}", driver.page_source)[0]
                savefile("dump_"+str(timestamp), jsdump)
                jsparse = json.loads(jsdump)
                try:
                    posts = jsparse["data"]["user"]["edge_follow"]["edges"]
                    end_cursor = jsparse["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
                    main_dict=traverse_query_json(posts,user_followers_file,main_dict)
                except:
                    print(uname+" cannot be extracted")
                    break

            if length != 0:
                visit("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={%22id%22:%22"+ucode+"%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:"+str(followers_left)+",%22after%22:%22"+end_cursor+"%22}",driver)
                jsdump = re.findall("{.*}", driver.page_source)[0]
                savefile("dump_"+str(timestamp), jsdump)
                jsparse = json.loads(jsdump)
                try:
                    posts = jsparse["data"]["user"]["edge_follow"]["edges"]
                    main_dict=traverse_query_json(posts,user_followers_file,main_dict)
                except:
                    print(uname+" cannot be extracted")
                    break
        except:
            print("Cannot get Followers information")
        savefile("Suspicious_Following_Followers/"+user_followers_file,json.dumps(main_dict))

    driver.quit()


def traverse_query_json(posts,user_followers_file,main_dict):
    uinfo={}
    print(len(posts))
    for p in posts:
        followers_id = p["node"]["id"]
        followers_username = p["node"]["username"]
        followers_fullname = p["node"]["full_name"]
        followers_is_private = p["node"]["is_private"]
        followers_is_verified = p["node"]["is_verified"]
        try:
            pass
            #print("Followers- FullName={} Username={} is_private={} is_verified={}".format(followers_fullname,followers_id,followers_is_private,followers_is_verified))
        except:
            print("Can't print")
        uinfo[followers_username]={"followers_id":followers_id ,"followers_username": followers_username,"followers_fullname":followers_fullname,"followers_is_private":followers_is_private,"followers_is_verified": followers_is_verified}
        main_dict.update(uinfo)
    return main_dict

def crawl_calculate_lifetime():
    '''
    calculate lifetime of the dead accounts
    '''
    print("Updating lifetime of dead accounts in the db")
    uinfo = {}
    timestamp = int(time_.time())
    username_live_create_died_list=db_uname_alive_create_died()

    for row in username_live_create_died_list:
        if row[3] is not None:
            uname=row[0]
            creation_date=row[1]
            died_date=row[2]
            creation_date=datetime.strptime(creation_date,'%Y-%m-%d %H:%M:%S')
            p=died_date-creation_date
            uinfo[uname] = {'lifetime':str(p)}
            savefile("parse_" + str(timestamp), json.dumps(uinfo))
    if os.path.exists("parse_" + str(timestamp)):
         db_update_lifetime("parse_" + str(timestamp))

def crawl_update_current_lifetime():
    '''
    update current lifetime
    '''
    uinfo = {}
    timestamp = int(time_.time())
    username_live_create_current_list=db_uname_alive_create_current()
    #get username already present in db
    #username_live_list=['cassandra_fx_trading','ericgloria_tradeplatform','feetphotos4dolars']

    for row in username_live_create_current_list:
        uname=row[0]
        creation_date=row[1]
        creation_date=datetime.strptime(creation_date,'%Y-%m-%d %H:%M:%S')
        recent_crawl_date=row[2]
        p=recent_crawl_date-creation_date
        uinfo[uname] = {'current_lifetime':str(p)}
        savefile("parse_" + str(timestamp), json.dumps(uinfo))
    db_update_current_lifetime("parse_" + str(timestamp))

def crawl_update_current_lifetime_version2():
    '''
    Fix code for crawl_update_current_lifetime()
    Updates lifetime of live accounts
    For each user
        get first row of username,
        get account creation date from first row
        get all rows for this user_name
        for each row
            set current lifetime= first crawl date of that row - account creation date of first row
            update current lifetime for this row by its ID
    '''
    # adding account creation date with respect to users to all records
    # uinfo = {}
    # timestamp = int(time_.time())
    # username_live_create_current_list=db_uname_alive_create_current()
    # for row in username_live_create_current_list:
    #     uname=row[0]
    #     creation_date=row[1]
    #     print(uname)
    #     print(creation_date)
    #     uinfo[uname]={'Account_Creation_date':creation_date}
    #     savefile("parse_" + str(timestamp), json.dumps(uinfo))
    # db_update_account_creation_date("parse_" + str(timestamp))


    #updating current lifetime by first_crawl_date-creation_date and updating w.r.t id
    print("Updating lifetime of alive accounts")
    uinfo = {}
    timestamp = int(time_.time())
    id_account_crawl_uname=db_get_id_account_first_dates()
    for row in id_account_crawl_uname:
        id=row[0]
        if row[1] is None:
            continue
        else:
            creation_date=row[1]
            first_crawl_date=row[2]
            creation_date=datetime.strptime(creation_date,'%Y-%m-%d %H:%M:%S')
            # first_crawl_date=datetime.strptime(first_crawl_date,'%Y-%m-%d %H:%M:%S')
            p=first_crawl_date-creation_date
            uinfo[id] = {'current_lifetime':str(p)}
            savefile("parse_" + str(timestamp), json.dumps(uinfo))
    # print(uinfo)
    if os.path.exists("parse_" + str(timestamp)):
        db_update_current_lifetime_version_2("parse_" + str(timestamp))


def crawl_sanitize_postCap_AccountDesc():
    '''
    Sanitize post caption and account description from sql injection
    '''
    uinfo = {}
    timestamp = int(time_.time())
    uname_post_acc_desc_list=db_get_postCap_desc()
    for row in uname_post_acc_desc_list[:200]:
        uname=row[0]
        post_caption=row[1]
        account_desc=row[2]
        # print(uname)
        # print(post_caption)
        # print(account_desc)
        post_caption=remove_chars_to_sanitise(post_caption)
        account_desc=remove_chars_to_sanitise(account_desc)
        # print(uname)
        # print(post_caption)
        # print(account_desc)
        uinfo[uname] = {'Post_Caption':post_caption,'account_desc':account_desc}
        savefile("parse_" + str(timestamp), json.dumps(uinfo))

    db_fix_saninitised_input("parse_" + str(timestamp))



def main():

    crawl_for_live()
    # finding_accounts_with_small_lifelime()
    # crawl_calculate_lifetime()
    # crawl_update_current_lifetime_version2()
    # crawl_suspicious_followers()
    # crawl_update_filenames()
    # crawl_sanitize_postCap_AccountDesc()
    # crawl_common_followers()
    # crawl_mark_suspicious_followers()
    # crawl_suspicious_following_followers()
    # crawl_all_common_followers_following()
    # all_dead_accounts_pics_to_a_folder()
    # get_data_all_final()
    # move_pics_to_its_hashtag_to_a_folder()
    pass


def crawl_update_filenames():
    '''
    Synchronises local filenames with followers file in the db
    '''
    uinfo={}
    timestamp = int(time_.time())
    uname_filename_list=db_get_filenames() # to check if file name already present in the table
    basepath = 'Suspicious_Followers/'
    with os.scandir(basepath) as entries:
        for entry in entries:
            uname=(entry.name).rsplit('_',1)[0]
            matching = [s for s in uname_filename_list if uname in s]
            if entry.is_file() and matching==[]:
                uinfo[uname]={"File_with_Followers_info":entry.name}
                savefile("parse_" + str(timestamp), json.dumps(uinfo))
            else:
                print("Already Present")
    try:
        db_update_followers_filename("parse_" + str(timestamp))
    except:
        print("Nothing to add to the Table")


def crawl_common_followers():
    '''
    Crawl exsiting follower files associated with usernames to check for common followers
    '''
    # common_followers_dict={}
    common_followers_dict = defaultdict(list)
    timestamp = int(time_.time())
    # uname_filename_list=db_get_filenames()
    basepath = 'Suspicious_Followers/'
    fileList = os.listdir(basepath)
    for file in fileList:
        uname=file.rsplit('_',1)[0]
        with open("Suspicious_Followers/"+str(file)) as json_file:
            content=json.load(json_file)
            for key in content:
                common_followers_dict[key].append(uname)
    savefile("commom_followers" + str(timestamp), json.dumps(common_followers_dict))

    length_dict = {key: len(value) for key, value in common_followers_dict.items()}
    t={k: v for k, v in sorted(length_dict.items(), key=lambda item: item[1])}
    for x in list(reversed(list(t)))[0:15]:
        print ("{} : {} ".format(x,  t[x]))
    p=list(reversed(list(t)))[0:15]
    print(p)

def crawl_common_followers_following():
    '''
    We got top 15 followers that are common and got their following
    '''
    # common_followers_dict={}
    common_followers_dict = defaultdict(list)
    timestamp = int(time_.time())
    # uname_filename_list=db_get_filenames()
    basepath = 'Suspicious_Following_Followers/'
    fileList = os.listdir(basepath)
    for file in fileList:
        uname=file.rsplit('_',1)[0]
        with open("Suspicious_Following_Followers/"+str(file)) as json_file:
            content=json.load(json_file)
            for key in content:
                common_followers_dict[key].append(uname)
    savefile("commom_followers_following" + str(timestamp), json.dumps(common_followers_dict))

    length_dict = {key: len(value) for key, value in common_followers_dict.items()}
    t={k: v for k, v in sorted(length_dict.items(), key=lambda item: item[1])}
    for x in list(reversed(list(t)))[0:15]:
        print ("{} : {} ".format(x,  t[x]))
    p=list(reversed(list(t)))[0:15]
    print(p)

def crawl_all_common_followers_following():
    '''
    Compared following of top suspicious followers with all the unique usernames in the db
    '''
    # common_followers_dict={}
    common_followers_dict = defaultdict(list)
    timestamp = int(time_.time())
    username_list=db_get_list_of_username()
    basepath = 'Suspicious_Following_Followers/'
    fileList = os.listdir(basepath)
    for file in fileList:
        uname=file.rsplit('_',1)[0]
        with open("Suspicious_Following_Followers/"+str(file)) as json_file:
            content=json.load(json_file)
            for key in content:
                if key in username_list:
                    common_followers_dict[uname].append(key)

    # savefile("all_commom_followers_following" + str(timestamp), json.dumps(common_followers_dict))

    length_dict = {key: len(value) for key, value in common_followers_dict.items()}
    t={k: v for k, v in sorted(length_dict.items(), key=lambda item: item[1])}
    for x in list(reversed(list(t)))[0:15]:
        print ("{} : {} ".format(x,  t[x]))
    p=list(reversed(list(t)))[0:15]
    print(p)


def crawl_mark_suspicious_followers():
    '''
    Marked Suspicious followers based on criteria..right now avg no. of post/avg lifetime=2
    '''
    uinfo={}
    timestamp = int(time_.time())
    uname_filename_alivelife=db_get_uname_Alive_lifetime()
    for row in uname_filename_alivelife:
        uname=row[0]
        current_life=row[1]
        num_of_posts=row[2]
        num_followers=row[3]
        if num_followers[-1] == 'k':
            num_followers=num_followers[:-1]
            num_followers=float(num_followers) * 1000
            num_followers=str(int(num_followers))
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
        num_followers = locale.atoi(num_followers)
        num_of_posts = locale.atoi(num_of_posts)
        if current_life:
            p=StringToTimedelta(current_life)
            days_current_Life= timedelta(**p)
            if (days_current_Life.days) == 0:
                d=1
            else:
                d=days_current_Life.days
            check_sus_no_posts=num_of_posts / d
            check_sus_no_followers = num_followers // d
            if check_sus_no_followers >= 2 :
                # or check_sus_no_posts >= 0.47
                uinfo[uname]={"suspicious_followers":1}
                savefile("parse_" + str(timestamp), json.dumps(uinfo))
                print(uname)

    try:
        db_update_suspicious_followers_value("parse_" + str(timestamp))
    except:
        print("Nothing to add")


def all_dead_accounts_pics_to_a_folder():
    file1 = open('dead_account_0207.txt', 'r')
    names = file1.readlines()
    for name in names:
        file_path= "../../Screenshots_SOUPS/"+name[:-1]+".png"
        copy_to_path = "../../dead_accounts_pics/"+name[:-1]+".png"
        if os.path.isfile(file_path):
            shutil.copy(file_path,copy_to_path)
        else:
            continue

def move_pics_to_its_hashtag_to_a_folder():

    hashtag="#growfollowers"
    username_live_list=db_get_uname_by_hashtags_used(hashtag) #get username already present in db with a hashtag
    with open(str(hashtag) + "_users.txt", 'w') as f:
        for item in username_live_list:
            f.write("{}\n".format(item))

    copy_to_path = "../../Screenshots_SOUPS/" + hashtag

    if os.path.exists(copy_to_path):
        pass
    else:
        os.mkdir(copy_to_path)


    file1 = open(str(hashtag) + "_users.txt", 'r')
    names = file1.readlines()
    for name in names:
        name = name.split(",", 1)[0][2:-1]
        file_path= "../../Screenshots_SOUPS/"+name+".png"
        copy_hashtag_folder_path = copy_to_path +"/" +name+".png"
        if os.path.isfile(file_path):
            shutil.copy(file_path,copy_hashtag_folder_path)
        else:
            continue

def get_data_all_final():
    data = db_get_data_final_with_unique_accounts()
    df = pd.DataFrame(data, columns =['user_name','Post_Caption','full_name','num_followers','num_following','account_desc','first_crawl_date','is_alive','died_on_date','num_of_posts','suspicious_followers','recent_crawl_date','is_potential_scammer','lifetime','current_lifetime','id'])
    df.to_csv (r'/Users/Alok Chandrawal/Documents/Research/Feb_19_all_accounts.csv', index = False, header=True)


main()
