from mysql.connector import connect
import json
import time as time_
from datetime import *
import locale
import os
import sys


def db_update_new_accounnts(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    recent_crawl_date=db_get_current_timeStamp()
    recent_crawl_date =recent_crawl_date.strftime('%Y-%m-%d %H:%M:%S')
    insert_query="""INSERT INTO INVESTORS_TAG (user_name,Post_Caption,Account_Creation_date,full_name,id_on_platform,num_followers,num_following,account_desc,is_alive,num_of_posts,suspicious_followers,recent_crawl_date,Post_Likes,Post_Comments) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(p,account[p]['Post_Caption'],account[p]['account_creation_date'],account[p]['full_name'],account[p]['id'],account[p]['num_of_followers'],account[p]['num_of_following'],account[p]['content'],1,account[p]['num_of_posts'],0,recent_crawl_date,account[p]['Post_Likes'],account[p]['Post_Comments'])
                try:
                    mycursor.execute(insert_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()
    print("WORKED")

def db_fix_account_creation_date(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET Account_Creation_date = %s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['account_creation_date'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    print("working")
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()
           
def db_get_list_of_username():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    get_usernames_query="""SELECT user_name from INVESTORS_TAG"""
    #refining queries
    get_usernames_query="""SELECT distinct(user_name) from INVESTORS_TAG"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        num = list(sum(row, ()))
        mycursor.close()
        mydb.close()
        return num
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_get_uname_alive_check():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,is_alive from INVESTORS_TAG"""
    #refining serach
    get_usernames_query="""SELECT user_name,is_alive,Account_Creation_date,MIN(id) as id FROM INVESTORS_TAG GROUP BY user_name"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_get_uname_with_small_lifetime():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    #refining serach
    get_usernames_query="""SELECT user_name,lifetime,MIN(id) as id FROM INVESTORS_TAG GROUP BY user_name"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_get_uname_by_hashtags_used(hashtag):
    
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,is_alive from INVESTORS_TAG"""
    #refining serach
    
    get_usernames_query="""SELECT user_name,is_alive,Account_Creation_date,MIN(id) as id FROM INVESTORS_TAG where lower(Post_Caption) LIKE '%""" + hashtag+ """%'  GROUP BY user_name"""
    print(get_usernames_query)
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""




def db_get_account_creation_date(uname):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    query="SELECT Account_Creation_date from INVESTORS_TAG where user_name=%s"
    adr=(uname,)
    try:
        mycursor.execute(query,adr)
        row = mycursor.fetchall()
        num = list(sum(row, ()))
        num=str(num[-1])
        mycursor.close()
        mydb.close()
        return num
    
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""
    
def db_update_timestamp(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET died_on_date = %s,is_alive=%s,recent_crawl_date=%s WHERE user_name=%s"""
    insert_query="""INSERT INTO INVESTORS_TAG (user_name,Account_Creation_date,num_followers,num_of_posts,is_alive) values(%s,%s,%s,%s,%s)"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                t=account[p]['died_on_date']
                if t != "":
                    died_on_date=datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
                    print(died_on_date)
                    try:
                        update_tuple=(died_on_date,account[p]['is_alive'],account[p]['recent_crawl_date'],p)
                        mycursor.execute(update_query,update_tuple)
                        mydb.commit()
                    except:
                        print("Error Inserting record")
                else:
                    died_on_date=None
                    insert_tuple=(p,account[p]['Account_Creation_date'],account[p]['num_followers'],account[p]['num_of_posts'],account[p]['is_alive'])
                    try:
                        mycursor.execute(insert_query,insert_tuple)
                        mydb.commit()
                    except Error as error :
                        print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    print("worked")
    mycursor.close()
    mydb.close()

def db_get_uname_followers_id_check():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    get_usernames_query="""SELECT a.user_name, a.num_followers,a.id_on_platform,a.suspicious_followers FROM INVESTORS_TAG a INNER JOIN (SELECT user_name,MIN(id) as id FROM INVESTORS_TAG GROUP BY user_name ) AS b ON a.user_name = b.user_name AND a.id = b.id where suspicious_followers=1 order by a.id"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        # print(row)
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_get_filenames():
    '''
    Get username and filenames as a list from the Follower_Files table
    '''
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    get_filename_query="""SELECT user_name,File_with_Followers_info from Followers_File"""
    try:
        mycursor.execute(get_filename_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""


def db_update_followers_filename(file):
    '''
    Update followers_file with new records
    '''
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    insert_query="""INSERT INTO Followers_File(user_name,File_with_Followers_info) values(%s,%s)"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                t=account[p]['File_with_Followers_info']
                insert_tuple=(p,t)
                try:
                    mycursor.execute(insert_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()   

 
def update_db_with_crawl_live():
    basepath = '.'
    with os.scandir(basepath) as entries:
        for entry in entries:
            if 'parse_' in entry.name:
                db_update_timestamp(entry.name)

def main():
    # db_get_current_timeStamp()
    # db_update_new_accounnts()
    # db_update_timestamp()
    #db_update_new_accounnts()
    # update_db_with_crawl_live()
    pass
    

def db_get_current_timeStamp():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    try:
        mycursor.execute("select CURRENT_TIMESTAMP")
        ts=mycursor.fetchall()
        return ts[0][0]
    except:
        print("Can't get current timestamp")
    mycursor.close()
    mydb.close()


def db_uname_alive_create_died():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,Account_Creation_date,died_on_date from INVESTORS_TAG where is_alive=0"""
    # refining search
    get_usernames_query="""SELECT user_name,Account_Creation_date,died_on_date,lifetime,MIN(id) as id FROM INVESTORS_TAG where is_alive=0 GROUP BY user_name"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_uname_alive_create_current():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,Account_Creation_date,died_on_date from INVESTORS_TAG where is_alive=0"""
    # refining search
    get_usernames_query="""SELECT user_name,Account_Creation_date,recent_crawl_date,MIN(id) as id FROM INVESTORS_TAG where is_alive=1 GROUP BY user_name"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_update_lifetime(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET lifetime = %s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['lifetime'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Exception as error:
        print(error)
    mycursor.close()
    mydb.close()

def db_update_current_lifetime(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET current_lifetime = %s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['current_lifetime'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()


def db_get_postCap_desc():
    '''
    get present username,post_caption and account  description
    '''
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,Account_Creation_date,died_on_date from INVESTORS_TAG where is_alive=0"""
    # refining search
    get_usernames_posts_query="""SELECT user_name,Post_Caption,account_desc FROM INVESTORS_TAG"""
    try:
        mycursor.execute(get_usernames_posts_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_fix_saninitised_input(file):
    '''
    Insert sanitised post caption and account description
    '''
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET Post_Caption= %s,account_desc=%s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['Post_Caption'],account[p]['account_desc'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()

def db_get_uname_Alive_lifetime():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    get_uname_alive_life="""SELECT user_name,current_lifetime,num_of_posts,num_followers,MIN(id) as id FROM INVESTORS_TAG where suspicious_followers=0 GROUP BY user_name"""
    try:
        mycursor.execute(get_uname_alive_life)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_update_suspicious_followers_value(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET suspicious_followers = %s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['suspicious_followers'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()

def  db_update_account_creation_date(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET Account_Creation_date = %s WHERE user_name=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['Account_Creation_date'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()

def db_update_current_lifetime_version_2(file):
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    update_query="""UPDATE INVESTORS_TAG SET current_lifetime = %s WHERE id=%s"""
    try:
        with open(file) as json_file:
            account=json.load(json_file)
            for i in range(len(account)):
                p=list(account)[i]
                insert_tuple=(account[p]['current_lifetime'],p)
                try:
                    mycursor.execute(update_query,insert_tuple)
                    mydb.commit()
                except Error as error :
                    print("Failed to insert into MySQL table {}".format(error))            
    except Error as error:
        print(error)
    mycursor.close()
    mydb.close()

def db_get_id_account_first_dates():
    '''
    get all id,account_creation,first_crawl dates
    '''
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    get_usernames_query="""SELECT id,Account_Creation_date,first_crawl_date,user_name FROM INVESTORS_TAG where current_lifetime is NULL"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""

def db_get_data_final_with_unique_accounts():
    db_hostname="dmmescam.clkgx0vexrgu.us-east-2.rds.amazonaws.com"
    mydb = connect(host=db_hostname,user="root",passwd="Success123",database="scamdb")
    mycursor=mydb.cursor()
    # get_usernames_query="""SELECT user_name,is_alive from INVESTORS_TAG"""
    #refining serach
    get_usernames_query="""SELECT user_name,Post_Caption,full_name,num_followers,num_following,account_desc,first_crawl_date,is_alive,died_on_date,num_of_posts,suspicious_followers,recent_crawl_date,is_potential_scammer,lifetime,current_lifetime,MIN(id) as id FROM INVESTORS_TAG GROUP BY user_name"""
    try:
        mycursor.execute(get_usernames_query)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return row
    except Error as error:
        print(error)
        mycursor.close()
        mydb.close()
        return ""





if __name__=="__main__":
    main()

